import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    oneLiner: z.string(),
    abstract: z.string(),
    tags: z.array(z.string()),
    role: z.string(),
    collaborators: z.string().optional(),
    status: z.enum(['ongoing', 'completed', 'public']),
    period: z.string(),
    links: z
      .array(
        z.object({
          label: z.string(),
          // Plain string, not z.string().url(): placeholder URLs containing
          // "[PLACEHOLDER" are kept in the content files and skipped at
          // render time instead.
          url: z.string(),
        }),
      )
      .optional(),
    comingSoon: z.string().optional(),
    featured: z.boolean(),
    order: z.number(),
    draft: z.boolean().optional(),
  }),
});

const news = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/news' }),
  schema: z.object({
    date: z.coerce.date(),
    // May contain one inline markdown link; rendered by NewsItem.astro.
    text: z.string(),
  }),
});

const notes = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/notes' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    description: z.string(),
    draft: z.boolean().optional(),
  }),
});

export const collections = { projects, news, notes };
