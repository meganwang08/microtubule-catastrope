#2.2
import numpy as np
import pandas as pd
import bokeh.io
from bokeh.io import output_file, show
import bokeh.plotting
import random
import microtubule_pkg as mt

output_file("EDA_fluorescent_labeling.html")

df = pd.read_csv('gardner_time_to_catastrophe_dic_tidy.csv', comment = '#')
labeled_df = df.loc[df['labeled'] == True]
unlabeled_df = df.loc[df['labeled'] == False]

x_lab,y_lab = mt.ecdf_vals(labeled_df['time to catastrophe (s)'])
x_unlab,y_unlab = mt.ecdf_vals(unlabeled_df['time to catastrophe (s)'])

p = bokeh.plotting.figure(plot_width=400, plot_height=400,
                          x_axis_label = 'time to catastrophe (s)',
                          y_axis_label = 'Cumulative Distribution')
p.circle(x_lab,y_lab, legend_label ='labeled')
p.circle(x_unlab,y_unlab, color = 'red', legend_label ='unlabeled')

p.legend.location = 'bottom_right'
show(p)
