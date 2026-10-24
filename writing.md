---
layout: single
title: Writing
permalink: /writing/
description: Poetry, essays, creative prose, and reflections by Jiayu Ellie Su.
classes: wide
author_profile: true
---

A collection of my poems, essays, and thoughts.

{% assign writing_items = site.writing | sort: "date" | reverse %}
{% assign poetry = writing_items | where: "category", "poetry" %}
{% assign essays = writing_items | where: "category", "essay" %}
{% assign reflections = writing_items | where: "category", "reflection" %}
{% assign creative_prose = writing_items | where: "category", "creative-prose" %}

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

## Essays
{% if essays.size > 0 %}
{% for entry in essays %}
<div class="creative-entry">
  <h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
  {% if entry.date %}<p class="creative-entry__meta">{{ entry.date | date: "%B %Y" }}</p>{% endif %}
  {% if entry.description %}<p>{{ entry.description | escape }}</p>{% endif %}
</div>
{% endfor %}
{% else %}
<p class="creative-empty">Essays will appear here.</p>
{% endif %}

## Creative Prose
{% if creative_prose.size > 0 %}
{% for entry in creative_prose %}
<div class="creative-entry">
  <h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
  {% if entry.date %}<p class="creative-entry__meta">{{ entry.date | date: "%B %Y" }}</p>{% endif %}
  {% if entry.description %}<p>{{ entry.description | escape }}</p>{% endif %}
</div>
{% endfor %}
{% else %}
<p class="creative-empty">Creative prose will appear here.</p>
{% endif %}

## Philosophical Reflections

*Blue to Blue: Death, Consciousness, and What Humanity Invents to Live* is a book of philosophy and poetry I'm currently working on. It explores how humans confront mortality, what makes a self, and how science, religion, and philosophy shape our attempts to understand death and find meaning in life. The manuscript pairs philosophical reflections with poems that approach the same questions through imagery and experience.

The pieces below are excerpts from this work in progress.

{% if reflections.size > 0 %}
{% for entry in reflections %}
<div class="creative-entry">
  <h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
  {% if entry.date %}<p class="creative-entry__meta">{{ entry.date | date: "%B %Y" }}</p>{% endif %}
  {% if entry.description %}<p>{{ entry.description | escape }}</p>{% endif %}
</div>
{% endfor %}
{% else %}
<p class="creative-empty">Reflections will appear here.</p>
{% endif %}
