// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { unified } from '@astrojs/markdown-remark';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

export default defineConfig({
  site: 'https://mileshall.com',
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [sitemap()],
  markdown: {
    // remark/rehype pipeline so remark-math + rehype-katex can run.
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [rehypeKatex],
    }),
    // Built-in Shiki highlighting; colours come from CSS variables in global.css.
    shikiConfig: {
      theme: 'css-variables',
      wrap: false,
    },
  },
});
