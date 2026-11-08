---
layout: single
title: Projects & Lectures
permalink: /projects/
description: Independent projects, expository papers, and lectures by Jiayu Ellie Su.
classes: wide
author_profile: true
---

I use this page to collect programming projects, mathematical expositions, and talks I've given. Teaching often makes me examine ideas more carefully, while programming lets me test them and follow questions that would otherwise remain abstract.

{% assign entries = site.projects | sort: "date" | reverse %}
{% assign projects = entries | where: "category", "project" %}
{% assign lectures = entries | where: "category", "lecture" %}

## Projects

Software, mathematical and computational investigations, and expository papers.

{% for entry in projects %}
<article class="creative-entry work-entry">
  <h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
  <p class="creative-entry__meta">{{ entry.kind | escape }} · {% if entry.display_date %}{{ entry.display_date | escape }}{% else %}{{ entry.date | date: "%B %Y" }}{% endif %}</p>
  {% if entry.description %}<p>{{ entry.description | escape }}</p>{% endif %}
  {% if entry.materials %}<p class="work-entry__includes"><strong>Included:</strong> {{ entry.materials | escape }}</p>{% endif %}
  {% if entry.primary_url %}<p class="work-entry__links"><a href="{{ entry.primary_url | relative_url }}">{{ entry.primary_label | escape }}</a>{% if entry.secondary_url %} <span aria-hidden="true">·</span> <a href="{{ entry.secondary_url | relative_url }}">{{ entry.secondary_label | escape }}</a>{% endif %}</p>{% endif %}
</article>
{% endfor %}

## Lectures

Talks I've given for classes, clubs, and math circles, along with their notes or slides.

{% for entry in lectures %}
<article class="creative-entry work-entry">
  <h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
  <p class="creative-entry__meta">Lecture · {% if entry.display_date %}{{ entry.display_date | escape }}{% else %}{{ entry.date | date: "%B %Y" }}{% endif %}{% if entry.setting %} · {{ entry.setting | escape }}{% endif %}</p>
  {% if entry.description %}<p>{{ entry.description | escape }}</p>{% endif %}
  {% if entry.materials %}<p class="work-entry__includes"><strong>Included:</strong> {{ entry.materials | escape }}</p>{% endif %}
  {% if entry.primary_url %}<p class="work-entry__links"><a href="{{ entry.primary_url | relative_url }}">{{ entry.primary_label | escape }}</a></p>{% endif %}
</article>
{% endfor %}
