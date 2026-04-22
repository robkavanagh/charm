# Parameters for generating the synthetic time series

import numpy as np

rad_per_deg = np.pi / 180

cos_i = 0.8
beta = 80 * rad_per_deg
phi_0 = 0.3 * 2 * np.pi
theta = 5 * rad_per_deg
phi = 40 * rad_per_deg
F_0 = 1
alpha = 75 * rad_per_deg
dalpha = 5 * rad_per_deg

params = [cos_i, beta, phi_0, theta, phi, F_0, alpha, dalpha]