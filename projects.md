---
layout: single
title: Projects & Notes
permalink: /projects/
description: Projects and explorations by Jiayu Ellie Su.
classes: wide
author_profile: true
---

A collection of projects, lecture notes, and things I've explored outside of my formal research. I've always loved teaching and sharing what I've learned with others, whether through giving lectures, explaining concepts, or simply discussing ideas. I find that preparing to teach something often helps me understand it more deeply myself. I also enjoy programming, both as a way to experiment with ideas and as an opportunity to build things from scratch. Most of these projects began with something I was curious about, whether that meant working through a proof, implementing an algorithm, or exploring a topic well enough to explain it to someone else.

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
