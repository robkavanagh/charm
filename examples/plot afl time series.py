# Example of using one of the CHARM models for time series forecasting.

# The time series should resemble the orange curve shown in Figure 3 of Kavanagh+ (2024) [https://doi.org/10.1051/0004-6361/202452094]

import numpy as np
import matplotlib.pyplot as plt
from charm.models import afl

rad_per_deg = np.pi / 180

cos_i = 0
beta = 90 * rad_per_deg
phase_0 = 0.8018124225050983 * 2 * np.pi
alpha = 69.79564815422037 * rad_per_deg
dalpha = 3.8338590224344298 * rad_per_deg
theta_B = 27.58757149969154 * rad_per_deg
phi_B = 127.4106800805469 * rad_per_deg
F = 2.030777274838066
params = [cos_i, beta, phase_0, alpha, dalpha, theta_B, phi_B, F]

phases = np.linspace(0, 1, 1000)
flux = afl()(params, phases)

plt.plot(phases, flux)
plt.xlabel('Rotation phase')
plt.ylabel('Stokes V flux density (mJy)')
plt.show()