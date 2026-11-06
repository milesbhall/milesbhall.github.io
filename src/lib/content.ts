import { getCollection } from 'astro:content';

/** Published posts, newest first. Drafts are visible in `astro dev` only. */
export async function getPosts() {
  const posts = await getCollection('blog', ({ data }) =>
    import.meta.env.PROD ? !data.draft : true,
  );
  return posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

/** All projects, newest first. */
export async function getProjects() {
  const projects = await getCollection('projects');
  return projects.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

const MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];

/** "OCT 2026" — projects are dated by month. Uses UTC so the month never shifts. */
export function formatMonth(d: Date) {
  return `${MONTHS[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
}

/** "2026-11-05" */
export function formatDate(d: Date) {
  return d.toISOString().slice(0, 10);
}
