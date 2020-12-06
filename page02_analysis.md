---
layout: page
title: Analysis
description: Analysis of the plots
img: microtubule_long.png # Add image post (optional)
caption: "Peter Mindek (2019)"
permalink: analysis.html
sidebar: true
---

---


# {{site.data.analysis.title}}
{{site.data.analysis.authors}}

{% for entry in site.data.analysis %}

{% if entry[0] != 'title' %}
{% if entry[0] != 'authors' %}
## {{entry[0]}}
{{entry[1]}}
{% endif %}
{% endif %}
{% endfor %}
