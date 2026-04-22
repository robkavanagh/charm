# This script samples the inferred posteriors for each parameter and plots the corresponding time series and compares them to the noisy time series initially generated.

import numpy as np
import matplotlib.pyplot as plt
from charm.models import afl
from params import params
import json

rad_per_deg = np.pi / 180

# Rotation phases of time series
npts = 50
phases = np.linspace(0, 1, npts)

# Fitted noisy time series
np.random.seed(0)
flux = afl()(params, phases) + np.random.normal(0, 0.15, size = npts)
err = np.random.uniform(0.1, 0.2, size = npts)

# Load parameter posteriors
posteriors = np.genfromtxt('charm_runs/run1/chains/equal_weighted_post.txt', delimiter = ' ', skip_header = 1)

# Max likelihood parameters
params_max_logL = json.load(open('charm_runs/run1/info/results.json'))['maximum_likelihood']['point']

# Choose random samples from the posteriors
np.random.seed()
nsamples = 1000
samples = posteriors[np.random.choice(posteriors.shape[0], size = nsamples, replace = False)]

# Rotation phases for time series generated from posterior samples
phases_sampled = np.linspace(0, 1, 500)
flux_sampled = np.zeros((nsamples, len(phases_sampled)))

# Compute time series for each posterior sample
for i, sample in enumerate(samples):
	flux_sampled[i] = afl()(sample, phases_sampled)

# Compute percentiles from sampled time series
flux_low, flux_high = np.percentile(flux_sampled, [1, 99], axis = 0)

# Max likelihood time series
flux_max_logL = afl()(params_max_logL, phases_sampled)

plt.errorbar(phases, flux, yerr = err, fmt = 'o', label = 'Time series', zorder = 10, markeredgecolor = 'black', ecolor = 'black', markerfacecolor = 'white', lw = 1.5, markeredgewidth = 1.5)
# plt.scatter(phases, flux, fc = 'white', ec = 'black', lw = 1.5, zorder = 10)
plt.fill_between(phases_sampled, flux_low, flux_high, color = 'xkcd:light red', alpha = 0.2, lw = 0, label = r'$1^\text{st}$ to $99^\text{th}$ percentile')
plt.plot(phases_sampled, flux_max_logL, color = 'xkcd:light red', lw = 2, ls = '--', label = 'Max likelihood')
plt.xlabel('Rotation phase')
plt.ylabel('Stokes V flux density (mJy)')
plt.legend(frameon = False)
plt.tight_layout()
plt.show()