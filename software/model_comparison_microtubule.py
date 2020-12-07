#9.1
import itertools
import warnings
import numpy as np
import pandas as pd
import scipy.optimize
import scipy.stats as st
import numba
import tqdm
import bebi103
import iqplot
from bokeh.layouts import gridplot
try:
    import multiprocess
except:
    import multiprocessing as multiprocess

from bokeh.io import output_file, show
import microtubule_pkg as mt

output_file("model_comparison.html")

rg = np.random.default_rng(1284)

df = pd.read_csv('gardner_mt_catastrophe_only_tubulin.csv',comment='#')
df = pd.melt(df, value_vars = ['12 uM', '7 uM', '9 uM', '10 uM', '14 uM'], var_name = 'tubulin concentrations',
        value_name = 'time to catastrophe (s)')
df = df.dropna()
concen = ['12 uM', '7 uM', '9 uM', '10 uM', '14 uM']

#stripbox
stripbox = iqplot.stripbox(
    title = 'Microtubule Time to Catastrophe against Tubulin Concentration',
    data = df,
    cats = ['tubulin concentrations'],
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

ecdf = iqplot.ecdf(
    title = 'Microtubule Time to Catastrophe against Tubulin Concentration',
    data = df,
    q = 'time to catastrophe (s)',
    cats = ['tubulin concentrations'],
    style = 'staircase',
    x_axis_label = 'Time to Catastrophe (s)'
)

def extract_by_column(val_col, val, extract_col):
    '''this function extracts the specified column and turns into a list'''
    temp_df = df.loc[df[val_col] == val][extract_col]
    lst = temp_df.to_list()
    return lst

list_12uM = extract_by_column('tubulin concentrations', '12 uM', 'time to catastrophe (s)')
list_7uM = extract_by_column('tubulin concentrations', '7 uM', 'time to catastrophe (s)')
list_9uM = extract_by_column('tubulin concentrations', '9 uM', 'time to catastrophe (s)')
list_10uM = extract_by_column('tubulin concentrations', '10 uM', 'time to catastrophe (s)')
list_14uM = extract_by_column('tubulin concentrations', '14 uM', 'time to catastrophe (s)')

bs_reps_12 = mt.draw_parametric_bs_reps_mle(
    mt.mle_iid_gamma, mt.gen_gamma, list_12uM, args=(), size=10000, n_jobs=4, progress_bar=True
)

conf_int = np.percentile(bs_reps_12, [2.5, 97.5], axis=0)
print('alpha= {}, {}'.format(conf_int[0][0], conf_int[1][0]))
print('beta= {}, {}'.format(conf_int[0][1], conf_int[1][1]))

mu = np.mean(list_12uM)
var = np.var(list_12uM)
alpha = mu**2 / var
beta = mu / var
print("Comparing confidence intervals to plug in estimates: alpha = {}, beta = {}".format(alpha, beta))

beta_1, delta_beta, beta_2 = mt.mle_iid_derived(list_12uM)
print('beta_1 MLE = {}'.format(beta_1))
print('delta_beta MLE = {}'.format(delta_beta))
print('beta_2 MLE = {}'.format(beta_2))

derived_bs_reps_microtubule = mt.draw_parametric_bs_reps_mle(
    mt.mle_iid_derived,
    mt.gen_samples,
    list_12uM,
    args=(),
    size=10000,
    progress_bar=True,
    n_jobs=4
)

poisson_conf_int = np.percentile(derived_bs_reps_microtubule, [2.5, 97.5], axis=0)
print('12 uM beta_1= [{}, {}]'.format(poisson_conf_int[0][0], poisson_conf_int[1][0]))
print('12 uM beta_2= [{}, {}]'.format(poisson_conf_int[0][2], poisson_conf_int[1][2]))

derived_samples = np.array(
    [rg.exponential(1/beta_1, size=len(list_12uM)) + rg.exponential(1/beta_2, size=len(list_12uM)) for _ in range(100000)]
)

gamma_samples = np.array(
    [rg.gamma(alpha, scale=1/beta, size=len(list_12uM)) for _ in range(100000)]
)

#graphs
derived = bebi103.viz.predictive_ecdf(
    samples=derived_samples, data=list_12uM, discrete=True, x_axis_label="Time to Catastrophe (s)"
)
derived.title.text = 'Derived Model from HW5.2 Predictive ECDF overlay with 12uM tubulin catastrophe time data'

gamma = bebi103.viz.predictive_ecdf(
    samples=gamma_samples, data=list_12uM, discrete=True, x_axis_label="Time to Catastrophe (s)"
)
gamma.title.text = 'Gamma Model from HW5.2 Predictive ECDF overlay with 12uM tubulin catastrophe time data'

der_diff = bebi103.viz.predictive_ecdf(
    samples=derived_samples, data=list_12uM, diff='ecdf', discrete=True, x_axis_label="Time to Catastrophe (s)"
)
der_diff.title.text = 'Difference between Predictive ECDF of model from HW5.2 and measured ECDF'

gamma_diff = bebi103.viz.predictive_ecdf(
    samples=gamma_samples, data=list_12uM, diff='ecdf', discrete=True, x_axis_label="Time to Catastrophe (s)"
)
gamma_diff.title.text = 'Difference between Predictive ECDF of Gamma model and measured ECDF'

mle_1 = mt.mle_iid_gamma(list_12uM)
mle_2 = mt.mle_iid_derived(list_12uM)

s = pd.Series(
    index=["alpha", "beta", "beta_1", "delta_beta", "beta_2"],
    data=np.concatenate((mle_1, mle_2)),
)

s["log_like_gamma"] = mt.log_like_iid_gamma(s[["alpha", "beta"]],list_12uM)
s["log_like_der"] = mt.log_like_iid_derived(s[["beta_1", "delta_beta"]],list_12uM)

s["AIC_1"] = -2 * (s['log_like_gamma'] - 2)
s["AIC_2"] = -2 * (s['log_like_der'] - 2)

AIC_max = max(s[['AIC_1', 'AIC_2']])
numerator = np.exp(-(s.loc['AIC_2'] - AIC_max)/2)
denominator = numerator + np.exp(-(s['AIC_1'] - AIC_max)/2)
s['w_single'] = numerator / denominator

print(s)

df_mle = pd.DataFrame(
    columns=["tubulin concentration (uM)", "parameter", "mle", "conf_int_low", "conf_int_high"]
)

# Perform MLE for each tubulin concentration
for concentration in tqdm.tqdm(concen):
    mle = mt.mle_iid_gamma(df.loc[df['tubulin concentrations'] == concentration]['time to catastrophe (s)'].values)
    bs_reps = mt.draw_parametric_bs_reps_mle(
        mt.mle_iid_gamma, mt.gen_gamma, df.loc[df['tubulin concentrations'] == concentration]['time to catastrophe (s)'].values,
        args=(), size=10000, n_jobs=4, progress_bar=False)
    conf_int = np.percentile(bs_reps, [2.5, 97.5], axis=0)

    sub_df = pd.DataFrame(
        {
            "tubulin concentration (uM)": [concentration] * 2,
            "parameter": ["alpha", "beta"],
            "mle": mle,
            "conf_int_low": conf_int[0, :],
            "conf_int_high": conf_int[1, :],
        }
    )
    df_mle = df_mle.append(sub_df)

sub_df = df_mle.loc[df_mle["parameter"] == "alpha", :]
summaries = [
    {"estimate": est, "conf_int": conf, "label": label}
    for est, conf, label in zip(
        sub_df["mle"].values,
        sub_df[["conf_int_low", "conf_int_high"]].values,
        sub_df["tubulin concentration (uM)"],
    )
]

p1 = bebi103.viz.confints(
    summaries,
    x_axis_label="alpha",
    y_axis_label="Tubulin Concentrations (uM)",
    title="95% Conf. Ints of MLE of Alpha of Microtubule Catastrophe Modeled by Gamma Dist."
    )

sub_df = df_mle.loc[df_mle["parameter"] == "beta", :]
summaries = [
    {"estimate": est, "conf_int": conf, "label": label}
    for est, conf, label in zip(
        sub_df["mle"].values,
        sub_df[["conf_int_low", "conf_int_high"]].values,
        sub_df["tubulin concentration (uM)"],
    )
]
p2 = bebi103.viz.confints(
    summaries,
    x_axis_label="beta",
    y_axis_label="Tubulin Concentrations (uM)",
    title="95% Conf. Ints of MLE of Beta of Microtubule Catastrophe Modeled by Gamma Dist."
    )

grid = gridplot([[stripbox, ecdf],[derived,gamma],[der_diff,gamma_diff], [p1,p2]])
show(grid)
