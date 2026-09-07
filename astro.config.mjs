// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { unified } from '@astrojs/markdown-remark';
import tailwindcss from '@tailwindcss/vite';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// https://astro.build/config
export default defineConfig({
  site: 'https://leonardovanni.com',
  integrations: [mdx(), sitemap()],
  // Old routes folded into the simplified nav (static meta-refresh pages).
  redirects: {
    '/projects/': '/research/',
    '/teaching/': '/experience/',
  },
  markdown: {
    // Build-time math: $...$ / $$...$$ -> KaTeX HTML (CSS imported once in global.css).
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [rehypeKatex],
    }),
    shikiConfig: { theme: 'github-light' },
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
