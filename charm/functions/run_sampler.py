from ultranest import ReactiveNestedSampler
from ultranest.stepsampler import SliceSampler, generate_mixture_random_direction
from charm.functions.make_log_likelihood import make_log_likelihood
from charm.functions.make_log_prior_transform import make_log_prior_transform

def run_sampler(model, data, nsteps = 10, log_dir = 'run'):

	phases, flux, err = data

	log_likelihood = make_log_likelihood(model, (phases, flux, err))
	log_prior_transform = make_log_prior_transform(model)

	sampler = ReactiveNestedSampler(model.param_names, log_likelihood, transform = log_prior_transform, wrapped_params = model.params.wrapped, log_dir = log_dir, resume = 'overwrite')
	sampler.stepsampler = SliceSampler(nsteps = nsteps, generate_direction = generate_mixture_random_direction)
	sampler.run(viz_callback = False, show_status = True)