---
layout: single
title: "String Quartet in D Major"
date: 2025-12-01
category: composition
description: "One of my first polished compositions, completed in December 2025."
classes: wide
author_profile: true
---

**Composer:** Jiayu Ellie Su

**Completed:** December 2025

One of my first polished compositions, this string quartet was completed in December 2025.

{% assign audio_path = '/assets/music/string-quartet-in-d-major.mp3' %}
{% assign audio_file = site.static_files | where: "path", audio_path | first %}
{% if audio_file %}
<audio controls preload="metadata" style="width: 100%;">
  <source src="{{ audio_path | relative_url }}" type="audio/mpeg">
  Your browser does not support audio playback.
</audio>

[Listen or download the MP3]({{ audio_path | relative_url }})
{% else %}
*Recording will be available here soon.*
{% endif %}
