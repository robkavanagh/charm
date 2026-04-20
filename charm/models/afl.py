import numpy as np

class afl:

	def __init__(self):

		# Parameter properties
		self.params = np.array([
			('cos_i', 0, 1, False),
			('beta', 0, 0.5 * np.pi, False),
			('phi_0', 0, 2 * np.pi, True),
			('alpha', 0, 0.5 * np.pi, False),
			('dalpha', 0, 0.5 * np.pi, False),
			('theta_B', 0, 0.5 * np.pi, False),
			('phi_B', 0, 2 * np.pi, True),
			('F', 0, 1, False)], 
			dtype = [('names', 'U10'), ('lower', float), ('upper', float), ('wrapped?', bool)])

	def __call__(self, params, phases):

		cos_i, beta, phi_0, alpha, dalpha, theta_B, phi_B, F = params

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
		cos_theta_B = np.cos(theta_B)
		cos_phi_B = np.cos(phi_B)

		# Compute the beam angle from each hemisphere
		denom = (1 + 3 * cos_theta_B ** 2) ** 0.5
		a = 3 * np.sin(theta_B) * cos_theta_B / denom
		b = (3 * cos_theta_B ** 2 - 1) / denom
		c = - sin_i * np.sin(phi_B)
		d = sin_i * cos_beta * cos_phi_B
		e = - cos_i * sin_beta * cos_phi_B
		T_1 = a * c
		T_2 = a * d
		T_3 = b * f
		T_4 = a * e
		T_5 = b * g
		gamma_N = np.arccos(T_1 * sin_phi_rot + (T_2 + T_3) * cos_phi_rot + (T_4 + T_5))
		gamma_S = np.arccos(T_1 * sin_phi_rot + (T_2 - T_3) * cos_phi_rot + (T_4 - T_5))

		return F * (np.exp(- 0.5 * ((gamma_N - alpha) / dalpha) ** 2) - np.exp(- 0.5 * ((gamma_S - alpha) / dalpha) ** 2))