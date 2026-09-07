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

// Mirrors byTumStart() in src/lib/dates.ts. Duplicated rather than imported
// because this script runs as plain .mjs outside the Astro/TS pipeline; keep
// the date in step with that module.
const tumLine =
  Date.now() >= new Date(2026, 9, 1).valueOf()
    ? 'M.Sc. student, Technical University of Munich'
    : 'Incoming M.Sc., Technical University of Munich';

// Warm paper --bg, name in Space Grotesk, subtitle, one thin rust rule.
// SVG <text> does not wrap: at 34px the subtitle fits ~60 characters before
// it runs off the 1200px canvas, and ~72 at 28px. Re-run `npm run og` and
// look at the PNG after any wording change.
const svg = `<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
  <rect width="1200" height="630" fill="#F6F3EC"/>
  <text x="96" y="318" font-family="Space Grotesk" font-weight="600" font-size="86" fill="#1E1B16">Leonardo Vanni</text>
  <line x1="98" y1="362" x2="568" y2="362" stroke="#96431C" stroke-width="3"/>
  <text x="96" y="432" font-family="Inter" font-size="34" fill="#5F584A">3D/4D computer vision — dynamic scenes, reliable geometry</text>
  <text x="96" y="486" font-family="Inter" font-size="28" fill="#8A8170">${tumLine}</text>
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
