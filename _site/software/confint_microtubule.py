#6.1
import numpy as np
import pandas as pd
import bokeh.io
import bokeh.plotting
from bokeh.layouts import gridplot
import iqplot
import scipy.stats
from numba import jit
import numba
from bokeh.io import output_file, show
import microtubule_pkg as mt

output_file("poisson_microtubule.html")

df = pd.read_csv('gardner_time_to_catastrophe_dic_tidy.csv')
lbl_df = df.loc[df['labeled'] == True]
lbl_times = lbl_df["time to catastrophe (s)"]
unlbl_df = df.loc[df['labeled'] == False]
unlbl_times = unlbl_df["time to catastrophe (s)"]



# Observed test statistic 
ks_obs = mt.ks_stat(labeled, unlabeled)  
#Draw permuation replicates
 ks_reps = mt.draw_perm_reps_ks(labeled, unlabeled, size=n_reps)
  # Compute p-value 
p_ks = (np.abs(ks_reps) > ks_obs).sum() / n_reps  
print("p =", p_ks)


overlay = iqplot.ecdf(
        data=df,
        q="time to catastrophe (s)",
        cats="labeled",
        q_axis="x",
        palette=['blue', 'orange'],
        order=None,
        p=None,
        title = 'Wait times for catastrophe with labeled and unlabeled tubulin',
        show_legend=True,
        tooltips=None,
        complementary=False,
        kind="collection",
        style="dots",
        conf_int=True,
        ptiles=[2.5, 97.5],
        n_bs_reps=10000,
        click_policy="hide",
        marker="circle",
    )

labeled = iqplot.ecdf(
        data=lbl_df,
        q="time to catastrophe (s)",
        q_axis="x",
        palette=['blue'],
        order=None,
        p=None,
        title = 'Wait times for microtubule catastrophe for labeled tubulin',
        show_legend=True,
        tooltips=None,
        complementary=False,
        kind="collection",
        style="dots",
        conf_int=True,
        ptiles=[2.5, 97.5],
        n_bs_reps=10000,
        click_policy="hide",
        marker="circle",
    )
unlabeled = iqplot.ecdf(
        data=unlbl_df,
        q="time to catastrophe (s)",
        q_axis="x",
        palette=['orange'],
        order=None,
        p=None,
        title = 'Wait times for microtubule catastrophe for unlabeled tubulin',
        show_legend=True,
        tooltips=None,
        complementary=False,
        kind="collection",
        style="dots",
        conf_int=True,
        ptiles=[2.5, 97.5],
        n_bs_reps=10000,
        click_policy="hide",
        marker="circle",
    )

data_labeled = df.loc[df["labeled"] == True, "time to catastrophe (s)"].values

p = iqplot.ecdf(
    data=df.loc[df["labeled"] == True, :],
    cats="labeled",
    q="time to catastrophe (s)",
    conf_int=True,
    title = 'Unlabeled Tubulin with Upper and Lower Bound'
)

x = np.linspace(0, 2000, 1000)
lower, upper = mt.dkw_conf_int(x, data_labeled, 0.05)

p.line(x, lower, line_width=2)
p.line(x, upper, line_width=2)

data_unlabeled = df.loc[df["labeled"] == False, "time to catastrophe (s)"].values

q = iqplot.ecdf(
    data=df.loc[df["labeled"] == False, :],
    cats="labeled",
    q="time to catastrophe (s)",
    conf_int=True,
    palette=["orange"],
    title = 'Unlabeled Tubulin with Upper and Lower Bound'
)

x = np.linspace(0, 2000, 1000)
lower, upper = mt.dkw_conf_int(x, data_unlabeled, 0.05)

q.line(x, lower, line_width=2, color="orange")
q.line(x, upper, line_width=2, color="orange")

grid = gridplot([[overlay, labeled, unlabeled], [p, q, None]])
show(grid)
