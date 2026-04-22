# This script creates a corner plot of the inferred posteriors for each parameter (shown in red) and compares them to the true values used to generate the synthetic time series (shown in blue).

import numpy as np
import matplotlib.pyplot as plt
from corner import corner
from params import params

rad_per_deg = np.pi / 180

data = np.genfromtxt('charm_runs/run1/chains/equal_weighted_post.txt', delimiter = ' ', names = True)
data_reshaped = data.view(np.float64).reshape(len(data), -1)
param_names = data.dtype.names

fig = plt.figure(figsize = (7, 6))
corner(data_reshaped, fig = fig, labels = param_names, truths = params, truth_color = 'xkcd:cerulean', plot_datapoints = False, plot_density = False, max_n_ticks = 3, color = 'xkcd:light red', labelpad = 0.5, levels = (0.16, 0.5, 0.84), fill_contours = True, contour_kwargs = {'linewidths': 0}, smooth = 1, rasterized = True, rotation = 0)

plt.subplots_adjust(left = 0.1, bottom = 0.1, wspace = 0.25, hspace = 0.25)
# plt.savefig('corner plot.png', dpi = 300)
plt.show()