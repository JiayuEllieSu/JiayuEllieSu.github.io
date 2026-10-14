---
layout: single
title: "Fluids & Hydrostatics: A Mini-Lecture"
date: 2025-10-01
category: note
description: "A mini-lecture I gave at my school's Physics Club in October 2025 to an audience of approximately 20 students."
classes: wide
author_profile: true
---

**Presented:** October 2025, School Physics Club  
**Audience:** Approximately 20 students

I gave a mini-lecture on fluids and hydrostatics at my school's Physics Club, introducing fundamental concepts in fluid mechanics and working through conceptual questions and problems with an audience of around 20 students.

The accompanying five-page handout covers pressure and hydrostatic equilibrium, Pascal's principle, continuity and Bernoulli's equation, and buoyancy. It also includes conceptual checks and challenge problems, including the pressure jump across a soap bubble.

{% assign handout_path = '/assets/Fluids__hydrostatis.pdf' %}
{% assign handout = site.static_files | where: "path", handout_path | first %}
{% if handout %}
[View the lecture handout (PDF)]({{ handout_path | relative_url }})
{% else %}
*Lecture handout coming soon.*
{% endif %}
