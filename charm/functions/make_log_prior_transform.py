import numpy as np

def make_log_prior_transform(model):

	ranges = model.params.ranges

	def log_prior_transform(cube):

		params = cube.copy()

		for i, (lower, upper) in enumerate(ranges):
			params[i] = cube[i] * (upper - lower) + lower

		return params

	return log_prior_transform