# CHARM
CHARM is a framework for characterising magnetic fields via Bayesian inference from radio-emitting objects like stars, brown dwarfs, and planets. It uses the nested sampling algorithm [UltraNest](https://johannesbuchner.github.io/UltraNest/) to explore the complex high-dimensional likelihood space of a chosen model given a time series dataset, providing probabilistic inferences (posteriors) for each model parameter. 

Different physical models can be assumed for the magnetic field and its associated emission. So far, the following models have been implemented:

### `afl`
This model assumes that emission originates from an **active field line** within a dipolar magnetic field that rotates rigidly with the object, driven by the electron cyclotron maser instability. For more details, see [Kavanagh+ 2024](https://doi.org/10.1051/0004-6361/202452094).

## Installation
CHARM is written in Python, and is installable via ```pip```: 
```
pip install git+https://github.com/robkavanagh/charm.git
```
Its dependencies are NumPy (>2.42), UltraNest (>4.5), and h5py (>3.16). The latter is required for UltraNest to utilise the HDF5 data format for writing the sampler results efficiently.

## Model configuration
Once CHARM is installed, you can import the model that you want to extract the parameters for given your data as:
```python
from charm.models import afl
```
You can then create an instance of the imported model:
```python
model = afl()
```
Each model parameter has a set of properties that are needed for the sampler, and can be accessed as follows:
```python
print(model.params['names'])
>>> ['cos_i' 'beta' 'phi_0' 'alpha' 'dalpha' 'theta_B' 'phi_B' 'F']
```
The other properties are `'lower'` and `'upper'`, which are the lower and upper parameter limits (the _prior_ range), and `'wrapped?'`, which sets if the parameter is periodic. Currently, flat priors are assumed for all model parameters. The prior ranges can be adjusted as follows:
```python
i = np.where(model.params['names'] == 'F')[0][0]
model.params[i]['upper'] = 10
```
Note that CHARM models can be used independently of the sampler, such as for forecasting the time-series for a given set of parameters (see `examples/plot AFL time series.py`).

## Running the sampler
Once the model parameters are configured for your purposes, you are ready to run the sampler to extract the underlying model parameters. For a time series of flux densities (`flux`) and associated errors (`err`) measured at different rotation phases (`phases`), the sampler can be run as follows:
```python
from charm.functions import sampler

sampler(model, (phases, flux, err))
```
`sampler` is effectively a wrapper for UltraNest's `ReactiveNestedSampler` function, constructing the likelihood and prior transform functions required for UltraNest in the background. The following parameters can also be set for `sampler`:

- `nsteps`: The number of steps to run the sampler for. Ideally you should increase this value until the results converge on a single set of parameters (default = `10`).
- `log_dir`: The directory where the sampler results are stored (default = `'charm_runs'`).
- `resume`: Determines what happens when the sampler is re-run. By default, this is set to `'subfolder'`, which creates a new sub-directory within `log_dir` for every run (`run1`, `run2`, etc.). See the [ReactiveNestedSampler API](https://johannesbuchner.github.io/UltraNest/ultranest.html#ultranest.integrator.ReactiveNestedSampler) for details. 
- `viz_callback`: See the [API for ReactiveNestedSampler.run](https://johannesbuchner.github.io/UltraNest/ultranest.html#ultranest.integrator.ReactiveNestedSampler.run) (default = `False`).
- `show_status`: See the [API for ReactiveNestedSampler.run](https://johannesbuchner.github.io/UltraNest/ultranest.html#ultranest.integrator.ReactiveNestedSampler.run) (default = `True`).

The script `examples/extract afl parameters/run sampler.py` shows an example of running the sampler on synthetic time series data. When UltraNest has finished, by default you will find the results within the directory the sampler was run from in `charm_runs/run1` for the first run, and subsequent runs in `charm_runs/run2` etc.

## Visualising the results
Given the high-dimensional and probabilistic nature of the extracted parameters, a corner plot is best suited to visualise the results from `sampler`. The script `examples/extract afl parameters/plot corner.py` can be run to plot the corner plot for the results from `run sampler.py`. The model parameters used to generate the synthetic data will be shown in blue, and should lie close to the peak of the 2D histograms (shown in dark red).

## Use cases
As of April 2026, CHARM has been used in the following works:
- Forecasting the detection yields of brown dwarfs for different build configurations of the [Square Kilometre Array](https://www.skao.int) (Kavanagh+ in review).
- Constraining the magnetic geometry of the brown dwarf WISE J112254.72+255022.2 ([Guirado+ 2025](https://doi.org/10.3847/1538-4357/add5f3)).
