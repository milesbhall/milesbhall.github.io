import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { getPosts } from '../../lib/content';

export async function GET(context: APIContext) {
  const posts = await getPosts(); // drafts already excluded in production
  return rss({
    title: 'Miles Hall: Writing',
    description: 'Writing by Miles Hall on math, computer science, and research.',
    site: context.site!,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.date,
      categories: post.data.tags,
      link: `/writing/${post.id}/`,
    })),
    customData: '<language>en-us</language>',
  });
}
