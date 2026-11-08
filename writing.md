---
layout: single
title: Writing
permalink: /writing/
description: Poetry, essays, creative prose, and reflections by Jiayu Ellie Su.
classes: wide
author_profile: true
---

This page is still a work in progress and currently includes only a small selection of my writing. I'll be adding more poems, essays, and other pieces over time.

{% assign writing_items = site.writing | sort: "date" | reverse %}
{% assign poetry = writing_items | where: "category", "poetry" %}
{% assign essays = writing_items | where: "category", "essay" %}
{% assign reflections = writing_items | where: "category", "reflection" %}
{% assign creative_prose = writing_items | where: "category", "creative-prose" %}

{% assign books = writing_items | where: "category", "book" %}

{% if books.size > 0 %}
## Book Manuscript

{% for entry in books %}
<article class="creative-entry">
  <h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
  <p class="creative-entry__meta">{{ entry.subtitle | escape }} · Revised manuscript, November 2026</p>
  <p>{{ entry.description | escape }}</p>
  <p><a href="{{ entry.manuscript_pdf | relative_url }}">Read the manuscript (PDF, 84 pages)</a></p>
</article>
{% endfor %}
{% endif %}

## Poetry
{% if poetry.size > 0 %}
{% for entry in poetry %}
<div class="creative-entry">
  <h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
  {% if entry.display_date %}<p class="creative-entry__meta">{{ entry.display_date | escape }}</p>{% elsif entry.date %}<p class="creative-entry__meta">{{ entry.date | date: "%B %Y" }}</p>{% endif %}
  {% if entry.description %}<p>{{ entry.description | escape }}</p>{% endif %}
</div>
{% endfor %}
{% else %}
<p class="creative-empty">Poems will appear here.</p>
{% endif %}

{% if essays.size > 0 %}
## Essays
{% for entry in essays %}
<div class="creative-entry">
  <h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
  {% if entry.date %}<p class="creative-entry__meta">{{ entry.date | date: "%B %Y" }}</p>{% endif %}
  {% if entry.description %}<p>{{ entry.description | escape }}</p>{% endif %}
</div>
{% endfor %}
{% endif %}

{% if creative_prose.size > 0 %}
## Creative Prose
{% for entry in creative_prose %}
<div class="creative-entry">
  <h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
  {% if entry.date %}<p class="creative-entry__meta">{{ entry.date | date: "%B %Y" }}</p>{% endif %}
  {% if entry.description %}<p>{{ entry.description | escape }}</p>{% endif %}
</div>
{% endfor %}
{% endif %}

