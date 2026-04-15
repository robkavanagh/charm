import numpy as np

def make_log_likelihood(model, data):

	phases, flux, err = data

	def log_likelihood(params):
		return -0.5 * (np.log(2 * np.pi * err ** 2) + ((flux - model(params, phases)) / err) ** 2).sum()
	
	return log_likelihood