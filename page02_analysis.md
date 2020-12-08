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
{% if entry[0] contains 'fig'%}
{% if entry[0] contains '1' %}
<center>
{% include_relative fig_html/EDA_fluorescent_labeling.html %}
</center>
{% endif %}
{% if entry[0] contains '2' %}
<center>
{% include_relative fig_html/poisson_microtubule.html %}
</center>
{% endif %}
{% if entry[0] contains '3' %}
![image](fig_html/math.jpg)
{% endif %}
{% if entry[0] contains '4' %}
<center>
{% include_relative fig_html/model_comparison.html %}
</center>
{% endif %}
{% else%}
## {{entry[0]}}
{{entry[1]}}
{% endif %}
{% endfor %}
