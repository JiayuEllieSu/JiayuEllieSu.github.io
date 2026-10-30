# Publishing guide

This site uses Jekyll collections. Add a Markdown file with YAML front matter to the appropriate directory, then commit. The index pages list entries automatically.

## Add an entry

1. Open the [repository](https://github.com/JiayuEllieSu/JiayuEllieSu.github.io).
2. Copy a suitable starter file from `_templates/`.
3. Create a Markdown file in the appropriate directory:
   - `_research/your-title.md` for research
   - `_projects/your-title.md` for published projects, notes, and lectures
   - `_draft_projects/your-title.md` for unfinished projects (not shown on the website)
   - `_writing/your-title.md` for poetry, essays, or reflections
   - `_music/your-title.md` for compositions and scores
   - `_posts/YYYY-MM-DD-your-title.md` for published blog posts
   - `_drafts/your-title.md` for unfinished blog posts
4. Replace the template title, date, description, and body. Commit the file.
5. Check the website and the repository's Actions tab after deployment.

Unfinished blog posts in `_drafts/` and unfinished projects in `_draft_projects/` remain in the repository but do not appear on the public site. Since this is a public GitHub repository, their source files are still publicly readable on GitHub.

## Categories

- Projects: `project` or `note`
- Writing: `poetry`, `essay`, or `reflection`
- Music: `composition`, `recording`, or `sheet-music`
- Blog: `categories: [mathematics]` or another appropriate category. Use `author: "Jiayu Ellie Su"` because the blog index filters by author.

## PDFs, music, and other files

Upload public assets into a clearly named folder inside `assets/`, preferably:

- `assets/papers/` for PDFs and lecture notes
- `assets/music/` for future audio and scores

Link with a relative URL, for example:

```liquid
[Read the paper]({{ '/assets/papers/example.pdf' | relative_url }})
```

The existing Fourier series lecture PDF is built from `assets/latex/fourier-series/` by a GitHub Actions workflow. Editing the LaTeX source triggers a PDF rebuild.

With this site's Kramdown/KaTeX renderer, use `$...$` for inline mathematics **inside a paragraph**, and `$` delimiters on their own lines for display equations. Don't automatically replace inline `$` with single-dollar delimiters.

## Local preview

```sh
bundle install
bundle exec jekyll serve
```

Generated dependencies, build caches, and the output directory are excluded from version control.

## Update or unpublish a page

Edit its Markdown source and commit. To unpublish a draft blog post without discarding the writing, move it to `_drafts/`. To unpublish an unfinished project entry, move its file from `_projects/` to `_draft_projects/`. These files remain visible in this public GitHub repository. Do not commit private information, unpublished research results, or work without permission to share.
