# Jiayu Ellie Su's personal website

The source for [jiayuelliesu.github.io](https://jiayuelliesu.github.io), a Jekyll website using the Minimal Mistakes theme.

## Content

- `_research/`: research project pages
- `_projects/`: projects, mathematics and physics notes, and lectures
- `_writing/`: writing and poetry
- `_music/`: compositions and music pages
- `_posts/`: published blog posts
- `_drafts/`: unfinished posts, not published by default
- `assets/`: PDFs, audio, stylesheets, and other public assets

Pages such as `projects.md` and `music.md` automatically list their respective collections. See [HOW_TO_PUBLISH.md](HOW_TO_PUBLISH.md) for instructions.

## Preview locally

Install Ruby and Bundler, then run:

```sh
bundle install
bundle exec jekyll serve
```

Open `http://localhost:4000`. Locally installed Ruby gems and generated site files belong outside version control and are ignored by `.gitignore`.

## Fourier series lecture notes

The source is in `assets/latex/fourier-series/`. The workflow in `.github/workflows/build-fourier-lecture.yml` compiles it and publishes `assets/papers/fourier-series-lecture-notes.pdf` when the LaTeX sources change. Keep the resulting PDF checked in because the Projects page links to it.

## Publishing safety

Only add documents and media that can be shared publicly. The personal writing, research, music, and site styling are intentionally retained in this repository.
