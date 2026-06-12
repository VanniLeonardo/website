/**
 * Generates public/og-default.png (1200x630) from the self-hosted fonts.
 * Run once (or after changing the design): npm run og
 *
 * Fontsource ships woff2 only, so the fonts are decompressed to TTF
 * (wawoff2) and handed to resvg as files — this resvg-js version supports
 * fontFiles/fontDirs, not in-memory buffers. Static instances are used
 * because resvg renders variable fonts incorrectly.
 */
import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const wawoff2 = require('wawoff2');
const { Resvg } = require('@resvg/resvg-js');

const root = new URL('..', import.meta.url);

const fontDir = await mkdtemp(join(tmpdir(), 'og-fonts-'));

async function toTtf(relPath, outName) {
  const woff2 = await readFile(new URL(relPath, root));
  const ttfPath = join(fontDir, outName);
  await writeFile(ttfPath, Buffer.from(await wawoff2.decompress(woff2)));
  return ttfPath;
}

const spaceGrotesk = await toTtf(
  'node_modules/@fontsource/space-grotesk/files/space-grotesk-latin-600-normal.woff2',
  'space-grotesk-600.ttf',
);
const inter = await toTtf(
  'node_modules/@fontsource/inter/files/inter-latin-400-normal.woff2',
  'inter-400.ttf',
);

// Dark navy --bg, name in Space Grotesk, subtitle, one thin accent line.
const svg = `<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
  <rect width="1200" height="630" fill="#0A0F1C"/>
  <text x="96" y="318" font-family="Space Grotesk" font-weight="600" font-size="86" fill="#E6EAF2">Leonardo Vanni</text>
  <line x1="98" y1="362" x2="568" y2="362" stroke="#7AA7E8" stroke-width="3"/>
  <text x="96" y="432" font-family="Inter" font-size="34" fill="#94A3B8">3D Computer Vision · Geometric Learning</text>
</svg>`;

const resvg = new Resvg(svg, {
  font: {
    fontFiles: [spaceGrotesk, inter],
    loadSystemFonts: false,
    defaultFontFamily: 'Space Grotesk',
  },
});

const png = resvg.render().asPng();
await writeFile(fileURLToPath(new URL('public/og-default.png', root)), png);
await rm(fontDir, { recursive: true, force: true });
console.log(`Wrote public/og-default.png (${(png.length / 1024).toFixed(1)} KB)`);
