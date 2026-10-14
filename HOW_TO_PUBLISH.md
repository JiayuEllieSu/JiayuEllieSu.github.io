# Publishing guide

Your homepage and navigation are already set up. **Do not edit the page layouts** when adding content.

## Add a new entry

1. Open the [GitHub repository](https://github.com/JiayuEllieSu/JiayuEllieSu.github.io).
2. Open the appropriate file in `_templates/` and copy its contents.
3. In GitHub choose **Add file → Create new file** and enter a path:
   - `_research/your-title.md` for research
   - `_projects/your-title.md` for projects or notes
   - `_writing/your-title.md` for poetry, essays, or reflections
   - `_music/your-title.md` for compositions, recordings, or scores
   - `_posts/YYYY-MM-DD-your-title.md` for blog posts
4. Paste the template, replace the sample title, date, description, and body, and commit the file. A new page and corresponding index entry will be generated automatically.
5. Check **Actions** for a successful Pages deployment, then visit the relevant section.

**Important:** `_templates/` contains examples only. They do not publish until you create a file in a collection.

## Categories (exact spelling)

- Projects: `project` or `note`
- Writing: `poetry`, `essay`, or `reflection`
- Music: `composition`, `recording`, or `sheet-music`
- Blog: use `categories: [mathematics]`, or other topics of your choice. Keep `author: "Jiayu Ellie Su"` so your post appears in the blog list.

## Upload files

For audio, PDFs, scores, images, or posters, upload to `assets/music/` or another suitable folder in `assets/` and link to them using `{{ '/assets/music/file.mp3' | relative_url }}` in your entry. If a folder does not yet exist, GitHub lets you create it as part of uploading a file.

Only publish files and material that you have permission to share. Don't publish drafts, personal contact information, or private schoolwork unintentionally.

## Editing later

Open the published Markdown file in GitHub, click its pencil icon, edit, and commit. The index updates automatically. Removing an entry's file removes it from the generated index at the next deployment.

## Blog and the original fork

Only posts with `author: "Jiayu Ellie Su"` appear in the main Blog listing. The old author's `_posts/` files still exist in this fork and may be reachable at their direct URLs; review and remove them separately when ready. The existing blog format is preserved.

## Working with ChatGPT

You can also tell ChatGPT, for example, "Add this poem to Writing under Poetry" or "Publish this composition with this audio file." Review the draft, then ask ChatGPT to publish it to the connected GitHub repository.
