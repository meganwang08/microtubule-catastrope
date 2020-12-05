#5.2
import numpy as np
import pandas as pd
import bokeh.io
from bokeh.io import output_file, show
import bokeh.plotting
import bokeh_catplot
from bokeh.layouts import gridplot
import random
import math
import microtubule_pkg as mt

output_file("poisson_microtubule.html")

rg = np.random.default_rng(3232)
b_pairs = [[1,9],[5,5],[8,2]]

catastrophe_simulation = mt.catastrophe_sim(b_pairs)

ecdf_0 = bokeh_catplot.ecdf(catastrophe_simulation[0], x_axis_label='time', y_axis_label='Percentile 1/B1', title="Microtubule Poisson Simulation b1 = {}, b2 = {}".format(b_pairs[0][0], b_pairs[0][1]) )
ecdf_1 = bokeh_catplot.ecdf(catastrophe_simulation[1], x_axis_label='time', y_axis_label='Percentile 1/B1', title="Microtubule Poisson Simulation b1 = {}, b2 = {}".format(b_pairs[1][0], b_pairs[1][1]) )
ecdf_2 = bokeh_catplot.ecdf(catastrophe_simulation[2], x_axis_label='time', y_axis_label='Percentile 1/B1', title="Microtubule Poisson Simulation b1 = {}, b2 = {}".format(b_pairs[2][0], b_pairs[2][1]) )

t = np.array(range(150))
x = np.linspace(0,20,150)

plots = []
for n in range(3):
    p = bokeh.plotting.figure(plot_width=400, plot_height=400, x_axis_label='time', y_axis_label='Percentile 1/B1', title="Multivariate Normal Overlay. b1 = {}, b2 = {}".format(b_pairs[n][0], b_pairs[n][1]))
    data = mt.ecdf_vals(catastrophe_simulation[n])
    p.circle(data[0], data[1])
    p.line(x, mt.cdf_func(x, 1, 9))
    plots.append(p)

grid = gridplot([[ecdf_0, ecdf_1, ecdf_2], [plots[0], plots[1], plots[2]]])
show(grid)
