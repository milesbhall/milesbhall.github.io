import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

/**
 * Blog posts live in src/content/blog/*.md.
 * The file name becomes the URL: my-post.md -> /writing/my-post
 */
const blog = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string().min(1),
    description: z.string().min(1),
    date: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

/**
 * Projects live in src/content/projects/*.md.
 * The file name becomes the URL: my-project.md -> /projects/my-project
 */
const projects = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: './src/content/projects' }),
  schema: z.object({
    name: z.string().min(1),
    /** One sentence. */
    description: z.string().min(1),
    /** What it was built for, e.g. a hackathon. */
    event: z.string().min(1),
    award: z.string().optional(),
    /** Used for sorting (newest first). Only month + year are displayed. */
    date: z.coerce.date(),
    team: z.string().min(1),
    /** Path under /public, e.g. /images/projects/foo.svg */
    thumbnail: z.string().startsWith('/'),
    links: z
      .array(
        z.object({
          label: z.string().min(1),
          url: z.url(),
        }),
      )
      .default([]),
  }),
});

export const collections = { blog, projects };
