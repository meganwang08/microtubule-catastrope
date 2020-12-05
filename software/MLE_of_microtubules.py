import itertools
import warnings
import numpy as np
import pandas as pd
import scipy.optimize
import scipy.stats as st
import numba
import tqdm
import bebi103
from bokeh.layouts import gridplot
try:
    import multiprocess
except:
    import multiprocessing as multiprocess

from bokeh.io import output_file, show
import microtubule_pkg as mt

output_file("MLE_confint.html")

rg = np.random.default_rng(1284)

tubulin_df = pd.read_csv('gardner_time_to_catastrophe_dic_tidy.csv',comment='#')
tubulin_df = tubulin_df.drop('Unnamed: 0', 1)
labeled_df = tubulin_df[tubulin_df.labeled != False]
time_to_cat = labeled_df['time to catastrophe (s)'].to_numpy()
cat_time_mle_gamma = mt.mle_iid_gamma(time_to_cat)
print('MLE alpha = {} and the MLE of beta = {}'.format(cat_time_mle_gamma[0], cat_time_mle_gamma[1]))
bs_reps = mt.draw_bs_reps_mle(
    mt.mle_iid_gamma, time_to_cat, size=10000, progress_bar=True)
gamma_conf_int = np.percentile(bs_reps, [2.5, 97.5], axis=0)
print('mean time to catastrophe'.format(np.mean(time_to_cat)))
print('alpha= {}, {}'.format(gamma_conf_int[0][0], gamma_conf_int[1][0]))
print('beta= {}, {}'.format(gamma_conf_int[0][1], gamma_conf_int[1][1]))

#Compare our confidence intervals to the plug-in estimates of the data
mu = np.mean(time_to_cat)
var = np.var(time_to_cat)
alpha = mu**2 / var
beta = mu / var
print("Comparing confidence intervals to plug in estimates: alpha = {}, beta = {}".format(alpha, beta))

#Part B MLE for the parameters 𝛽1 and 𝛽2 and conf_int
bs_reps_microtubule = mt.draw_parametric_bs_reps_mle(
    mt.mle_iid_derived,
    mt.gen_samples,
    time_to_cat,
    args=(),
    size=10000,
    progress_bar=True,
    n_jobs=4
)

poisson_CI = np.percentile(bs_reps_microtubule, [2.5, 97.5], axis=0)
print('beta_1 = [{}, {}]'.format(poisson_CI[0][0], poisson_CI[1][0]))
print('beta_2 = [{}, {}]'.format(poisson_CI[0][2], poisson_CI[1][2]))

all_data_gamma = [{'label': 'beta_1',
  'estimate': np.mean(bs_reps[0]),
  'conf_int': np.array(gamma_conf_int[0])},
 {'label': 'beta_2',
  'estimate': np.mean(bs_reps[1]),
  'conf_int': np.array(gamma_conf_int[1])}]

q = bebi103.viz.confints(
    all_data_gamma,
    x_axis_label='Gamma distribution of microtubule catastrophe',
    y_axis_label='beta',
    title='',
)


all_data_poisson = [{'label': 'beta_1',
  'estimate': np.mean(bs_reps_microtubule[0]),
  'conf_int': np.array(poisson_CI[0])},
 {'label': 'beta_2',
  'estimate': np.mean(bs_reps_microtubule[1]),
  'conf_int': np.array(poisson_CI[1])}]

p = bebi103.viz.confints(
    all_data_poisson,
    x_axis_label='Poisson distribution of microtubule catastrophe',
    y_axis_label='beta',
    title='',
)

grid = gridplot([[q,p]])
show(grid)
