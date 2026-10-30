# Notes for updating the website

Add or edit Markdown files in:

- `_research/` for research
- `_projects/` for projects, lectures, and notes
- `_writing/` for essays and poems
- `_music/` for music
- `_posts/` for blog posts

Put PDFs and other files in `assets/`. Use `_templates/` if needed.

Unfinished blog posts can go in `_drafts/`, and unfinished projects in `_draft_projects/`. These aren't published on the website, but the repository itself is public.

Commit changes to `main` to update the website. Check [GitHub Actions](https://github.com/JiayuEllieSu/JiayuEllieSu.github.io/actions) if something doesn't appear.

For local preview: `bundle install` and `bundle exec jekyll serve`.

Fourier lecture notes are in `assets/latex/fourier-series/`; the workflow rebuilds the linked PDF when they change.
