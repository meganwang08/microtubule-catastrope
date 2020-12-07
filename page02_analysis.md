---
layout: page
title: Analysis
description: Analysis of the plots
img: microtubule_analysis.jpg # Add image post (optional)
caption: "Wikipedia"
permalink: analysis.html
sidebar: true

---


{% for entry in site.data.analysis %}

{% if entry[0] != 'title' %}
{% if entry[0] != 'authors' %}
## {{entry[0]}}
{{entry[1]}}
{% endif %}
{% endif %}
{% endfor %}
