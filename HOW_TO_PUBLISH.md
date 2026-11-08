# Updating the website

Add pages to `_research/` (research), `_projects/` (projects, expository papers, and lectures), `_writing/` (writing), and `_music/` (music).

## Projects and lectures

The `/projects/` page has two sections. Use `category: project` for software, computational investigations, and expository papers, or `category: lecture` for talks. Specify `kind:` to distinguish software projects from expository papers. For lectures, also set `setting:` where relevant.

Keep each entry consistent: one-sentence `description:`, `materials:` stating what is included, `primary_label:` and `primary_url:` linking to the PDF, handout, or code. Optional secondary links use `secondary_label:` and `secondary_url:`. Use `display_date:` when a season is more accurate than a month.

The shared `_includes/work-meta.html` renders date, type, contributors, setting, and materials on detail pages. Start from `_templates/project.md`, `_templates/note.md`, or `_templates/lecture.md`.

Put PDFs in `assets/`, and verify their paths. Commit changes to `main`; consult [GitHub Actions](https://github.com/JiayuEllieSu/JiayuEllieSu.github.io/actions) for deploy status. Locally, run `bundle install` and `bundle exec jekyll serve`.

Unfinished pages may be kept in `_drafts/` or `_draft_projects/`. They are not published as pages, but the repository is public.
