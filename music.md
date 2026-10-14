---
layout: single
title: Music
permalink: /music/
description: Musical background and compositions by Jiayu Ellie Su.
classes: wide
author_profile: true
---

## My Musical Background

Music has been a part of my life for as long as I can remember. I began learning piano at five and violin at six, before switching from violin to cello at eleven. Along the way, I also had chances to learn the recorder, clarinet, and ukulele at school.

For years, most of my musical experience centered on performing. I worked through Level 8 piano repertoire with the Royal Conservatory of Music, won awards at piano competitions, and performed at Carnegie Hall several times. On cello, I have played in school, youth, and chamber orchestras, including as a section leader and soloist. These experiences gave me different ways of thinking about melody, harmony, and what each instrument contributes to an ensemble.

I became increasingly interested in writing music of my own. In ninth grade, I took a composition class that went beyond the AP Music Theory curriculum, which gave me the chance to explore more advanced ideas in harmony and composition. After years of learning and performing music written by other people, I found it especially exciting to start putting my own musical ideas together. Composition now feels like a way to bring together what I've learned from piano, violin, cello, and music theory.

## Compositions

{% assign music_items = site.music | sort: "date" | reverse %}
{% assign compositions = music_items | where: "category", "composition" %}
{% assign scores = music_items | where: "category", "sheet-music" %}
{% if compositions.size > 0 %}
{% for entry in compositions %}
<div class="creative-entry">
  <h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
  {% if entry.date %}<p class="creative-entry__meta">{{ entry.date | date: "%B %Y" }}</p>{% endif %}
  {% if entry.description %}<p>{{ entry.description | escape }}</p>{% endif %}
</div>
{% endfor %}
{% else %}
<p class="creative-empty">Original compositions will appear here.</p>
{% endif %}

## Sheet Music
{% if scores.size > 0 %}
{% for entry in scores %}
<div class="creative-entry">
  <h3><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></h3>
  {% if entry.date %}<p class="creative-entry__meta">{{ entry.date | date: "%B %Y" }}</p>{% endif %}
  {% if entry.description %}<p>{{ entry.description | escape }}</p>{% endif %}
</div>
{% endfor %}
{% else %}
<p class="creative-empty">Scores will appear here as I add them.</p>
{% endif %}
