import numpy as np
import matplotlib.pyplot as plt
from charm.models import afl
from charm.functions import sampler
from params import params

# Rotation phases of time series
npts = 50
phases = np.linspace(0, 1, npts)

# Generate noisy time series from sample parameters
np.random.seed(0)
flux = afl()(params, phases) + np.random.normal(0, 0.15, size = npts)
err = np.random.uniform(0.1, 0.2, size = npts)

# Create instance of the model
model = afl()

# Adjust prior ranges
i = np.where(model.params['names'] == 'F')[0][0]
model.params[i]['upper'] = 5

# Run the sampler
sampler(model, (phases, flux, err), nsteps = 100)