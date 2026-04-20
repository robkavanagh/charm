import numpy as np
import matplotlib.pyplot as plt
from corner import corner
from params import params

rad_per_deg = np.pi / 180

data = np.genfromtxt('charm_runs/run1/chains/equal_weighted_post.txt', delimiter = ' ', names = True)
data_reshaped = data.view(np.float64).reshape(len(data), -1)
param_names = data.dtype.names

# Compute 1st and 99th percentile in case chains contain outliers
ranges = [tuple(np.percentile(data_reshaped[:, i], [1, 99]).tolist()) for i in range(len(param_names))]

fig = plt.figure(figsize = (8, 8))
corner(data_reshaped, fig = fig, labels = param_names, truths = params, truth_color = 'xkcd:sky blue', plot_datapoints = False, plot_density = False, max_n_ticks = 3, color = 'xkcd:light red', labelpad = 0.25, levels = (0.16, 0.5, 0.84), fill_contours = True, contour_kwargs = {'linewidths': 0}, smooth = 1, range = ranges)

plt.subplots_adjust(left = 0.1, bottom = 0.1, wspace = 0.1, hspace = 0.1)
plt.show()