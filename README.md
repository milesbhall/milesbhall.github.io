# mileshall.com

Personal site and blog. Static [Astro](https://astro.build) site, deployed to GitHub Pages
by `.github/workflows/deploy.yml` on every push to `main`.

```sh
npm install
npm run dev      # http://localhost:4321 (drafts visible)
npm run build    # production build in dist/ (drafts excluded)
```

## Publish a blog post

1. Copy `src/content/blog/_template.md` to `src/content/blog/my-post.md`.
   The file name becomes the URL: `/writing/my-post/`.
2. Fill in `title`, `description`, `date`, `tags`, and set `draft: false`.
3. Commit and push to `main`. The workflow rebuilds the site, RSS feed, and sitemap.

Math uses `$inline$` and `$$display$$` (KaTeX). Fenced code blocks are highlighted.

## Add a project

Add `src/content/projects/my-project.md` (URL: `/projects/my-project/`) with front matter:
`name`, `description`, `event`, `award`, `date`, `team`, `thumbnail`, and `links`
(see the existing files). Put the thumbnail in `public/images/projects/`.
Projects sort newest first by `date`.

## Resume

Replace `public/resume.pdf`. The `/resume/` page embeds it automatically.

## Design tokens

All colours, fonts, and spacing are CSS variables at the top of `src/styles/global.css`.
