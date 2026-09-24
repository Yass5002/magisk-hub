import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const modules = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './content/modules' }),
  schema: z.object({
    id: z.string(),
    title: z.string(),
    sidebarTitle: z.string().optional(),
    description: z.string(),
    category: z.string(),
    tier: z.number().default(1),
    searchQueries: z.array(z.string()).default([]),
    prerequisites: z.array(z.string()).default([]),
    conflicts: z.array(z.string()).default([]),
    configPaths: z.array(z.string()).default([]),
    features: z.array(z.string()).default([]),
    faq: z.array(z.object({
      question: z.string(),
      answer: z.string(),
    })).default([]),
  }),
});

export const collections = { modules };
