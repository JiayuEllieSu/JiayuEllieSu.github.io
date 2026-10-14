---
layout: single
title: Projects
permalink: /projects/
description: Projects and explorations by Jiayu Ellie Su.
classes: wide
author_profile: true
---

Projects, experiments, and things I'm learning.

{% assign entries = site.projects | sort: "date" | reverse %}
{% assign projects = entries | where: "category", "project" %}
{% assign notes = entries | where: "category", "note" %}

## Projects
{% if projects.size > 0 %}
{% for entry in projects %}
<article class="creative-entry">
<h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
{% if entry.description %}<p>{{ entry.description | escape }}</p>{% endif %}
</article>
{% endfor %}
{% else %}
<p class="creative-empty">Projects will appear here.</p>
{% endif %}

## Notes & Explorations
{% if notes.size > 0 %}
{% for entry in notes %}
<article class="creative-entry">
<h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
{% if entry.description %}<p>{{ entry.description | escape }}</p>{% endif %}
</article>
{% endfor %}
{% else %}
<p class="creative-empty">Mathematics, physics, and other notes will appear here.</p>
{% endif %}
