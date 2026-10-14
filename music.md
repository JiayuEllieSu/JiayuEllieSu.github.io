---
layout: single
title: Music
permalink: /music/
description: Compositions, recordings, and sheet music by Jiayu Ellie Su.
classes: wide
author_profile: true
---

A place for music I've composed and performed.

{% assign music_items = site.music | sort: "date" | reverse %}
{% assign compositions = music_items | where: "category", "composition" %}
{% assign recordings = music_items | where: "category", "recording" %}
{% assign scores = music_items | where: "category", "sheet-music" %}

## Compositions
{% if compositions.size > 0 %}
{% for entry in compositions %}
<div class="creative-entry">
  <h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
  {% if entry.date %}<p class="creative-entry__meta">{{ entry.date | date: "%B %-d, %Y" }}</p>{% endif %}
  {% if entry.description %}<p>{{ entry.description | escape }}</p>{% endif %}
</div>
{% endfor %}
{% else %}
<p class="creative-empty">Original compositions will appear here.</p>
{% endif %}

## Recordings
{% if recordings.size > 0 %}
{% for entry in recordings %}
<div class="creative-entry">
  <h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
  {% if entry.date %}<p class="creative-entry__meta">{{ entry.date | date: "%B %-d, %Y" }}</p>{% endif %}
  {% if entry.description %}<p>{{ entry.description | escape }}</p>{% endif %}
</div>
{% endfor %}
{% else %}
<p class="creative-empty">Recordings will appear here.</p>
{% endif %}

## Sheet Music
{% if scores.size > 0 %}
{% for entry in scores %}
<div class="creative-entry">
  <h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
  {% if entry.date %}<p class="creative-entry__meta">{{ entry.date | date: "%B %-d, %Y" }}</p>{% endif %}
  {% if entry.description %}<p>{{ entry.description | escape }}</p>{% endif %}
</div>
{% endfor %}
{% else %}
<p class="creative-empty">Scores will appear here.</p>
{% endif %}
