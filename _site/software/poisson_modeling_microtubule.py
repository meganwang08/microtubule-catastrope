#5.2
import numpy as np
import pandas as pd
import bokeh.io
from bokeh.io import output_file, show
import bokeh.plotting
from bokeh.layouts import gridplot
import random
import math
import iqplot
import microtubule_pkg as mt

output_file("poisson_microtubule.html")

rg = np.random.default_rng(3232)

def draw_model(beta_1, beta_2, size=1):
    return rg.exponential(1/beta_1, size=size) + rg.exponential(1/beta_2, size=size)


n_samples = 150
p = None

p = bokeh.plotting.figure(
    frame_height=250,
    frame_width=400,
    x_axis_label="time to catastrophe × β₁",
    y_axis_label="ECDF",
)

beta_ratio = [0.1, 0.5, 1, 5, 10]

catastrophe_times = np.concatenate(
    [draw_model(1, br, size=n_samples) for br in beta_ratio]
)
beta_ratios = np.concatenate([[br] * n_samples for br in beta_ratio])
df = pd.DataFrame(
    data={"β₂/β₁": beta_ratios, "time to catastrophe × β₁": catastrophe_times}
)

p = iqplot.ecdf(
    df,
    q="time to catastrophe × β₁",
    cats="β₂/β₁",
    palette=bokeh.palettes.Blues7[1:-1][::-1],
)
p.legend.title = "β₂/β₁"

t_exp = np.sort(draw_model(1, 3, size=n_samples))



t = np.linspace(0, 10, 200)
cdf = mt.cdf_func(t, 1, 3)

q= iqplot.ecdf(t_exp, x_axis_label="time to catastrophe × β₁",)

q.line(t, cdf, line_width=2, color="orange")

grid = gridplot([[p,q]])
show(grid)
