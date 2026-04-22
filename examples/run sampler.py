# This script generates a noisy time series from a sample set of parameters, then runs the sampler to infer the posteriors for each parameter.

import numpy as np
from charm.models import afl
from charm.functions import sampler
from params import params

# Fix seed for reproducibility
np.random.seed(0)

# Generate noisy time series from sample parameters
npts = 50
phases = np.random.uniform(0, 1, npts)
flux = afl()(params, phases) + np.random.normal(0, 0.15, size = npts)
err = np.random.uniform(0.1, 0.2, size = npts)

# Create instance of the model
model = afl()

# Adjust prior ranges
i = np.where(model.params['names'] == 'F_0')[0][0]
model.params[i]['upper'] = 5

# Run the sampler
sampler(model, (phases, flux, err), nsteps = 300)