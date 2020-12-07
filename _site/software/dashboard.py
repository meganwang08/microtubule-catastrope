import itertools
import warnings
import numpy as np
import pandas as pd
import scipy.optimize
import scipy.stats as st
import numba
import tqdm
import bebi103
import holoviews as hv
import iqplot
import panel as pn
from bokeh.layouts import gridplot
try:
    import multiprocess
except:
    import multiprocessing as multiprocess

from bokeh.io import output_file, show
import microtubule_pkg as mt

output_file("interactive_fig1.html")

rg = np.random.default_rng(1284)

lbl_df = pd.read_csv('gardner_time_to_catastrophe_dic_tidy.csv')

labeled = lbl_df.loc[lbl_df["labeled"] == True, "time to catastrophe (s)"].values
unlabeled = lbl_df.loc[lbl_df["labeled"] == False, "time to catastrophe (s)"].values

# Make plots for tubulin concentration data
# taken from HW9.1
df = pd.read_csv('gardner_mt_catastrophe_only_tubulin.csv',comment='#')
df = pd.melt(df, value_vars = ['12 uM', '7 uM', '9 uM', '10 uM', '14 uM'], var_name = 'tubulin concentrations',
        value_name = 'time to catastrophe (s)')
df = df.dropna()
concen = ['12 uM', '7 uM', '9 uM', '10 uM', '14 uM']

def tub_stripbox(conc):
    return iqplot.stripbox(
        title = 'Microtubule Time to Catastrophe against Tubulin Concentration',
        data = df.loc[df['tubulin concentrations'] == conc],
        q = 'time to catastrophe (s)',
        #color_column='year',
        q_axis='x',
        jitter=True,
        whisker_caps=True,
        display_points=False,
        marker_kwargs=dict(alpha=0.5, size=1),
        box_kwargs=dict(fill_color=None, line_color='grey'),
        median_kwargs=dict(line_color='grey'),
        whisker_kwargs=dict(line_color='grey'),
        top_level='box',
        x_axis_label = 'Time to Catastrophe (s)',
        y_axis_label = 'Tubulin Concentrations (uM)'
        )

def conc_ecdf(conc):
    return iqplot.ecdf(
        title = 'Microtubule Time to Catastrophe against Tubulin Concentration',
        data = df.loc[df['tubulin concentrations'] == conc],
        q = 'time to catastrophe (s)',
        cats = ['tubulin concentrations'],
        style = 'staircase',
        x_axis_label = 'Time to Catastrophe (s)'
        )

def tub_ecdf_plots(conc):
    data = list(df.loc[df['tubulin concentrations'] == conc, 'time to catastrophe (s)'])
    mu = np.mean(data)
    var = np.var(data)
    alpha = mu**2 / var
    beta = mu / var
    beta_1, delta_beta, beta_2 = mt.mle_iid_derived(data)

    derived_samples = np.array(
    [rg.exponential(1/beta_1, size=len(data)) + rg.exponential(1/beta_2, size=len(data)) for _ in range(1000)]
    )
    derived = bebi103.viz.predictive_ecdf(
        samples=derived_samples, data=list(data), discrete=True, x_axis_label="Time to Catastrophe (s)"
    )
    derived.title.text = 'Derived ECDF overlay with {} tubulin catastrophe time data'.format(conc)
    return pn.Row(derived)

def lbl_ecdf_confints(lbl_bool):
    if lbl_bool:
        title_mod = 'Labeled'
        palette = ['#0000FF']
    else:
        title_mod = 'Unlabeled'
        palette = ['#FFA500']
    data = lbl_df.loc[lbl_df["labeled"] == lbl_bool, "time to catastrophe (s)"].values

    p = iqplot.ecdf(
        data=lbl_df.loc[lbl_df["labeled"] == lbl_bool, :],
        cats="labeled",
        q="time to catastrophe (s)",
        conf_int=True,
        palette = palette,
        title = 'Wait times for microtubule catastrophe for {} tubulin'.format(title_mod)
    )

    x = np.linspace(0, 2000, 1000)
    lower, upper = mt.dkw_conf_int(x, data, 0.05)

    p.line(x, lower, line_width=2, color=palette[0])
    p.line(x, upper, line_width=2, color=palette[0])
    return p

def lbl_dboard():
    lbl_select = pn.widgets.Select(name="Labeled Tubulin Status", options=[True,False])
    @pn.depends(lbl_select.param.value)
    def lbl_plots(lbl):
        return pn.Row(lbl_ecdf_confints(lbl))
    return pn.Column(lbl_select, lbl_plots)


def conc_dboard():
    conc_select = pn.widgets.Select(name="Concentration of Tubulin", options=concen)
    @pn.depends(conc_select.param.value)
    def tubulin_conc_plots(conc):
        return pn.Column(
            pn.Row(tub_stripbox(conc), pn.Spacer(width=15) ,tub_ecdf_plots(conc)),
        )
    return pn.Column(conc_select, tubulin_conc_plots)


output = pn.Column(conc_dboard())
output.save('dashboard.html', embed=True)
