import numpy as np

def make_log_prior_transform(model):

	lower_vals, upper_vals = model.params['lower'], model.params['upper']

	def log_prior_transform(cube):

		params = cube.copy()

		for i, (lower, upper) in enumerate(zip(lower_vals, upper_vals)):
			params[i] = cube[i] * (upper - lower) + lower

		return params

	return log_prior_transform