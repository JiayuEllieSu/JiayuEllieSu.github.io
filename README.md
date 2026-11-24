# Personal website

[jiayuelliesu.github.io](https://jiayuelliesu.github.io)

Built with Jekyll and Minimal Mistakes 4.24.0. I use this site to keep my research, projects, writing, and music in one place.

## Preview locally

Install Ruby, Bundler, and Python 3.10 or later. From the repository root:

```sh
bundle install
bundle exec jekyll build --config _config.yml,_tools/local.yml
python3 -m http.server --bind 127.0.0.1 --directory _site 4000
```

Open http://127.0.0.1:4000. The local configuration uses the same theme version already pinned in Gemfile.lock; GitHub Pages uses the remote theme pinned in _config.yml.

## Link checks

```sh
python3 -m unittest discover -s _tools -p 'test_*.py' -v
python3 _tools/check_links.py _site
python3 _tools/check_links.py _site --external
```

GitHub Actions builds the site and checks internal page links, HTML anchors, and linked files on pushes and pull requests. External links are also checked weekly and on manual workflow runs. HTTP 404 and 410 fail the check; blocked requests, rate limits and transient network errors are reported as warnings.

## Repository structure

- `_research/`, `_projects/`, `_writing/`, `_music/`: published entries.
- `assets/`: PDFs, lecture sources, styles, and scripts.
- `_includes/`, `_layouts/`, `_sass/`: custom theme overrides only; unchanged theme files come from the pinned upstream theme.
- `_templates/`, `_drafts/`, `_draft_projects/`: reusable page templates and unpublished drafts.
- `_tools/`, `.github/workflows/`: local configuration, link checks, and PDF build automation.

See [HOW_TO_PUBLISH.md](HOW_TO_PUBLISH.md) for editing guidance.

## Citations

GPT-6 was used in the editing of my website.
