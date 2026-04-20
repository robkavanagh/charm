# Parameters for generating the synthetic time series for the example

import numpy as np

rad_per_deg = np.pi / 180

cos_i = 0.8
beta = 80 * rad_per_deg
phase_0 = 0.3 * 2 * np.pi
alpha = 75 * rad_per_deg
dalpha = 5 * rad_per_deg
theta_B = 5 * rad_per_deg
phi_B = 40 * rad_per_deg
F = 1

params = [cos_i, beta, phase_0, alpha, dalpha, theta_B, phi_B, F]