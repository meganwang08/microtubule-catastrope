---
layout: page
title: Analysis
description: Analysis of the plots
img: microtubule_analysis.jpg # Add image post (optional)
caption: "Wikipedia"
permalink: analysis.html
sidebar: true

---

# {{site.data.analysis.title}}
{{site.data.analysis.authors}}

{% for entry in site.data.a %}

{% if entry[0] != 'title' %}
{% if entry[0] != 'authors' %}
## {{entry[0]}}
{{entry[1]}}
{% endif %}
{% endif %}
{% endfor %}
