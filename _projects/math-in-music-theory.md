---
layout: single
title: "Math in Music Theory"
date: 2026-01-14
category: note
description: "A Math Club lecture I gave on January 14, 2026, to an audience of approximately 15 people, exploring mathematical structures underlying music."
classes: wide
author_profile: true
---

**Presented:** January 14, 2026, School Math Club  
**Audience:** Approximately 15 people  
**Format:** Approximately 20-minute lecture, 17 slides

I gave a Math Club lecture on the mathematical ideas underlying music theory, drawing on my interests in both mathematics and music. The talk explored how the frequencies of sound waves translate into musical pitch, why octaves and semitones are naturally described using logarithms, and how pitch classes, transposition, and inversion can be modeled using arithmetic modulo 12.

I also discussed the circle of fifths, frequency ratios and consonance, the overlap of harmonics, and how Fourier series help explain why instruments playing the same pitch can have different timbres.

{% assign slides_path = '/assets/math-in-music-theory.pdf' %}
{% assign slides = site.static_files | where: "path", slides_path | first %}
{% if slides %}
[View the lecture slides (PDF)]({{ slides_path | relative_url }})
{% else %}
*Lecture slides will be available here soon.*
{% endif %}
