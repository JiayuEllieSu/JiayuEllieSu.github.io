---
layout: single
title: Writing
permalink: /writing/
description: Poetry, essays, and reflections by Jiayu Ellie Su.
classes: wide
author_profile: true
---

A collection of my poems, essays, and thoughts.

{% assign writing_items = site.writing | sort: "date" | reverse %}
{% assign poetry = writing_items | where: "category", "poetry" %}
{% assign essays = writing_items | where: "category", "essay" %}
{% assign reflections = writing_items | where: "category", "reflection" %}

## Poetry
{% if poetry.size > 0 %}
{% for entry in poetry %}
<div class="creative-entry">
  <h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
  {% if entry.date %}<p class="creative-entry__meta">{{ entry.date | date: "%B %-d, %Y" }}</p>{% endif %}
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
  {% if entry.date %}<p class="creative-entry__meta">{{ entry.date | date: "%B %-d, %Y" }}</p>{% endif %}
  {% if entry.description %}<p>{{ entry.description | escape }}</p>{% endif %}
</div>
{% endfor %}
{% else %}
<p class="creative-empty">Essays will appear here.</p>
{% endif %}

## Philosophical Reflections
{% if reflections.size > 0 %}
{% for entry in reflections %}
<div class="creative-entry">
  <h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
  {% if entry.date %}<p class="creative-entry__meta">{{ entry.date | date: "%B %-d, %Y" }}</p>{% endif %}
  {% if entry.description %}<p>{{ entry.description | escape }}</p>{% endif %}
</div>
{% endfor %}
{% else %}
<p class="creative-empty">Reflections will appear here.</p>
{% endif %}
