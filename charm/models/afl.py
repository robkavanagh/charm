import numpy as np

class afl:

	def __init__(self):

		# Parameter properties
		self.params = np.array([
			('cos_i', 0, 1, False, 'dimensionless'),
			('beta', 0, 0.5 * np.pi, False, 'radians'),
			('phi_0', 0, 2 * np.pi, True, 'radians'),
			('theta', 0, 0.5 * np.pi, False, 'radians'),
			('phi', 0, 2 * np.pi, True, 'radians'),
			('F_0', 0, 1, False, 'flux units'),
			('alpha', 0, 0.5 * np.pi, False, 'radians'),
			('dalpha', 0, 0.5 * np.pi, False, 'radians')], 
			dtype = [('names', 'U10'), ('lower', float), ('upper', float), ('wrapped?', bool), ('units', 'U10')])

	def __call__(self, params, phases):

		cos_i, beta, phi_0, theta, phi, F_0, alpha, dalpha = params

		# Rotation phase
		phi_rot = phi_0 + 2 * np.pi * phases

		# Repeated terms
		sin_i = np.sin(np.arccos(cos_i))
		sin_beta = np.sin(beta)
		cos_beta = np.cos(beta)
		sin_phi_rot = np.sin(phi_rot)
		cos_phi_rot = np.cos(phi_rot)
		f = sin_i * sin_beta
		g = cos_i * cos_beta

		# Repeated terms
		cos_theta = np.cos(theta)
		cos_phi = np.cos(phi)

		# Compute the beam angle from each hemisphere
		denom = (1 + 3 * cos_theta ** 2) ** 0.5
		a = 3 * np.sin(theta) * cos_theta / denom
		b = (3 * cos_theta ** 2 - 1) / denom
		c = - sin_i * np.sin(phi)
		d = sin_i * cos_beta * cos_phi
		e = - cos_i * sin_beta * cos_phi
		T_1 = a * c
		T_2 = a * d
		T_3 = b * f
		T_4 = a * e
		T_5 = b * g
		gamma_N = np.arccos(T_1 * sin_phi_rot + (T_2 + T_3) * cos_phi_rot + (T_4 + T_5))
		gamma_S = np.arccos(T_1 * sin_phi_rot + (T_2 - T_3) * cos_phi_rot + (T_4 - T_5))

		return F_0 * (np.exp(- 0.5 * ((gamma_N - alpha) / dalpha) ** 2) - np.exp(- 0.5 * ((gamma_S - alpha) / dalpha) ** 2))