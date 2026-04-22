import numpy as np

class ring:
	
	def __init__(self):
		
		self.params = np.array([
			('cos_i', -1, 1, False, 'dimensionless'),
			('beta', 0, np.pi, False, 'radians'),
			('phi_0', 0, 1, True, 'dimensionless'),
			('theta', 0, 0.5 * np.pi, False, 'radians'),
			('F_0', 0, 1, False, 'flux units'),
			('alpha', 0, 0.5 * np.pi, False, 'radians'),
			('dalpha', 0, 0.5 * np.pi, False, 'radians')], 
			dtype = [('names', 'U10'), ('lower', float), ('upper', float), ('wrapped?', bool), ('units', 'U10')])

	def __call__(self, params, phases):

		cos_i, beta, phi_0, theta, F_0, alpha, dalpha = params

		# Rotation phases
		phi_rot_arr = phi_0 + 2 * np.pi * phases

		# Cone
		alpha_min = alpha - dalpha / 2
		alpha_max = alpha + dalpha / 2
		cos_alpha_min = np.cos(alpha_min)
		cos_alpha_max = np.cos(alpha_max)

		# Fixed values over rotation
		sin_i = np.sin(np.arccos(cos_i))
		sin_beta = np.sin(beta)
		cos_beta = np.cos(beta)
		cos_theta = np.cos(theta)
		denom = (1 + 3 * cos_theta ** 2) ** 0.5
		A = 3 * np.sin(theta) * cos_theta / denom
		C = (3 * cos_theta ** 2 - 1) / denom
		
		frac = np.zeros((len(phases), 2))

		# Loop over rotation phases
		for i, phi_rot in enumerate(phi_rot_arr):

			# Values that vary over rotation
			cos_phi_rot = np.cos(phi_rot)
			D = - sin_i * np.sin(phi_rot)
			E = sin_i * cos_beta * cos_phi_rot - cos_i * sin_beta
			F = sin_i * sin_beta * cos_phi_rot + cos_i * cos_beta
			G = A * D
			H = A * E
			I = C * F

			# Min/max longitude
			phi_a = np.arctan(G / H)
			phi_b = phi_a + np.pi

			# Min/max beam angle for Northern ring
			gamma_a = np.arccos(G * np.sin(phi_a) + H * np.cos(phi_a) + I)
			gamma_b = np.arccos(G * np.sin(phi_b) + H * np.cos(phi_b) + I)

			# Determine which is min and max
			if gamma_a > gamma_b:
				phi_max = phi_a
				phi_min = phi_b
				gamma_max_N = gamma_a
				gamma_min_N = gamma_b

			else:
				phi_max = phi_b
				phi_min = phi_a
				gamma_max_N = gamma_b
				gamma_min_N = gamma_a

			# Peaks are at same longitudes for Southern hemisphere
			gamma_min_S = np.arccos(G * np.sin(phi_min) + H * np.cos(phi_min) - I)
			gamma_max_S = np.arccos(G * np.sin(phi_max) + H * np.cos(phi_max) - I)

			# Beam angle range
			J_min_N = I - cos_alpha_min
			J_max_N = I - cos_alpha_max
			J_min_S = - I - cos_alpha_min
			J_max_S = - I - cos_alpha_max


			##################################################
			# Compute fraction visible from each hemisphere
			##################################################

			for j in np.arange(2):

				# Set values for hemisphere
				gamma_min = [gamma_min_N, gamma_min_S][j]
				gamma_max = [gamma_max_N, gamma_max_S][j]
				J_min = [J_min_N, J_min_S][j]
				J_max = [J_max_N, J_max_S][j]

				# No overlap
				if (alpha_max < gamma_min) | (gamma_max < alpha_min): continue

				# At least partial overlap
				else:

					# Partial overlap lower
					if (alpha_min < gamma_min): partial_lower = True

					else:
						phi_min_a = - 2 * np.arctan(G / (J_min - H) + ((G ** 2 + H ** 2 - J_min ** 2) / (J_min - H) ** 2) ** 0.5)
						phi_min_b = - 2 * np.arctan(G / (J_min - H) - ((G ** 2 + H ** 2 - J_min ** 2) / (J_min - H) ** 2) ** 0.5)
						partial_lower = False
					
					# Partial overlap upper
					if (gamma_max < alpha_max): partial_upper = True

					else:
						phi_max_a = - 2 * np.arctan(G / (J_max - H) + ((G ** 2 + H ** 2 - J_max ** 2) / (J_max - H) ** 2) ** 0.5)
						phi_max_b = - 2 * np.arctan(G / (J_max - H) - ((G ** 2 + H ** 2 - J_max ** 2) / (J_max - H) ** 2) ** 0.5)
						partial_upper = False

					# All longitudes visible
					if (partial_lower == True) & (partial_upper == True): frac[i, j] = 1

					if (partial_lower == True) & (partial_upper == False): 

						dphi_1 = np.arccos(np.cos(phi_max_a - phi_min))
						dphi_2 = np.arccos(np.cos(phi_max_a - phi_min))
						frac[i, j] = (dphi_1 + dphi_2) / (2 * np.pi)

					if (partial_lower == False) & (partial_upper == True): 

						dphi_1 = np.arccos(np.cos(phi_min_a - phi_max))
						dphi_2 = np.arccos(np.cos(phi_min_a - phi_max))
						frac[i, j] = (dphi_1 + dphi_2) / (2 * np.pi)

					if (partial_lower == False) & (partial_upper == False): 

						# Slopes
						dgamma_min_a = (H * np.sin(phi_min_a) - G * np.cos(phi_min_a)) * (1 - cos_alpha_min ** 2) ** - 0.5
						dgamma_min_b = (H * np.sin(phi_min_b) - G * np.cos(phi_min_b)) * (1 - cos_alpha_min ** 2) ** - 0.5
						dgamma_max_a = (H * np.sin(phi_max_a) - G * np.cos(phi_max_a)) * (1 - cos_alpha_max ** 2) ** - 0.5
						dgamma_max_b = (H * np.sin(phi_max_b) - G * np.cos(phi_max_b)) * (1 - cos_alpha_max ** 2) ** - 0.5

						phi_arr = np.array([phi_min_a, phi_min_b, phi_max_a, phi_max_b])
						dgamma_arr = np.array([dgamma_min_a, dgamma_min_b, dgamma_max_a, dgamma_max_b])

						# Identify pair based on slopes
						phi_1_1, phi_1_2 = phi_arr[np.sign(dgamma_arr) == 1.0]
						phi_2_1, phi_2_2 = phi_arr[np.sign(dgamma_arr) == - 1.0]

						dphi_1 = np.arccos(np.cos(phi_1_1 - phi_1_2))
						dphi_2 = np.arccos(np.cos(phi_2_1 - phi_2_2))
						frac[i, j] = (dphi_1 + dphi_2) / (2 * np.pi)

		frac_N, frac_S = frac.T

		lc = F_0 * (frac_N - frac_S)

		return lc