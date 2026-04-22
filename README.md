# CHARM
CHARM is a framework for characterising magnetic fields via Bayesian inference from radio-emitting objects like stars, brown dwarfs, and planets. It utilises the nested sampling algorithm [UltraNest](https://johannesbuchner.github.io/UltraNest/) to explore the complex high-dimensional likelihood space of a chosen model given a time series dataset, providing probabilistic inferences (posteriors) for each model parameter. 

## Installation
CHARM is written in Python, and is installable via ```pip```: 
```
pip install git+https://github.com/robkavanagh/charm.git
```
Its dependencies are NumPy (>2.42), UltraNest (>4.5), and h5py (>3.16). The latter is required for UltraNest to utilise the HDF5 data format for writing the sampler results efficiently.

## Available models
Different physical models can be adopted for the origin of the emission in the magnetic field. So far, the following models have been implemented, all of which assume a dipolar magnetic field structure:

### `afl`
This model assumes that emission originates from an **active field line** (AFL) that rotates rigidly with the object. The parameters of this model are as follows:

- `cos_i`: Cosine of the inclination angle of the rotation axis from the line of sight
- `beta`: Angle between the rotation and magnetic axes
- `phi_0`: Rotation phase at `phases = 0` (see below)
- `theta`: Magnetic co-latitude of the emission cone on the AFL
- `phi`: Magnetic longitude of the AFL
- `F_0`: Flux density of the AFL 
- `alpha`: Opening angle of the emission cone
- `dalpha`: Thickness of the emission cone

For more details, see [Kavanagh+ 2024](https://doi.org/10.1051/0004-6361/202452094). See the sketch below also for a visual representation:

<p align='center'>
<img width="50%" src="assets/sketch afl.png" />
</p>


### `ring`
This model assumes that the emission comes from auroral rings centered above the two magnetic poles. Its parameters are:

- `cos_i`: Same as for `afl`
- `beta`: Same as for `afl`
- `phi_0`: Same as for `afl`
- `theta`: Magnetic co-latitude of the Northern auroral ring
- `F_0`: Flux density of each auroral ring
- `alpha`: Same as for `afl`
- `dalpha`: Same as for `afl`

It is described in more detail in [Bloot+ 2024](https://doi.org/10.1051/0004-6361/202348065). See the sketch below also:

<p align='center'>
<img width="50%" src="assets/sketch ring.png" />
</p>

## Model configuration
Once CHARM is installed, you can import the model that you want to extract the parameters for given your data as:
```python
from charm.models import afl
```
You can then create an instance of the imported model:
```python
model = afl()
```
Each model parameter has a set of informative properties for the sampler and user, which can be accessed as follows:
```python
print(model.params['names'])
>>> ['cos_i' 'beta' 'phi_0' 'theta' 'phi' 'F_0' 'alpha' 'dalpha']
```
The other properties are:
- `'lower'` and `'upper'`: the lower and upper parameter limits (the _prior_ range)
- `'wrapped?'`: sets if the parameter is periodic
- `'units'`: the units of each parameter

Currently, flat priors are assumed for all model parameters. The prior ranges can be adjusted as follows:
```python
i = np.where(model.params['names'] == 'F_0')[0][0]
model.params[i]['upper'] = 10
```
Note that CHARM models can be used independently of the sampler, such as for forecasting the time-series for a given set of parameters.

## Running the sampler
Once the model parameters are configured for your purposes, you are all set to extract the magnetic field parameters of an assumed model. For a time series of flux densities (`flux`) and associated errors (`err`) measured at different rotation phases (`phases`), the sampler can be run as follows:
```python
from charm.functions import sampler

sampler(model, (phases, flux, err))
```
`sampler` is effectively a wrapper for UltraNest's `ReactiveNestedSampler` function, constructing the likelihood and prior transform functions required for UltraNest in the background. The following parameters can also be set for `sampler`:

- `nsteps`: The number of steps to run the sampler for. Ideally you should increase this value until the results converge on a single set of parameters (default = `10`).
- `log_dir`: The directory where the sampler results are stored (default = `'charm_runs'`).
- `resume`: Determines what happens when the sampler is re-run. By default, this is set to `'subfolder'`, which creates a new sub-directory within `log_dir` for every run (`run1`, `run2`, etc.). See the [ReactiveNestedSampler API](https://johannesbuchner.github.io/UltraNest/ultranest.html#ultranest.integrator.ReactiveNestedSampler) for details. 
- `viz_callback` and `show_status`: See the [API for ReactiveNestedSampler.run](https://johannesbuchner.github.io/UltraNest/ultranest.html#ultranest.integrator.ReactiveNestedSampler.run) (default values are `False` and `True` respectively).

The script `examples/run sampler.py` shows an example of applying the sampler to synthetic time series data using the `afl` model. When UltraNest has finished, by default you will find the results within the directory where you ran the sampler in `charm_runs/run1` for the first run. Subsequent runs will be written to `charm_runs/run2` etc.

## Visualising the results
Given the high-dimensional and probabilistic nature of the extracted parameters, a corner plot is best suited to visualise the results from `sampler`. The script `examples/plot corner.py` can be run to generate a corner plot for the results from `run sampler.py`. This should produce a figure showing the posteriors for each parameter as red contours with the parameters used to generate the synthetic time series overlaid in blue:

<p align='center'>
<img width="50%" src="assets/example corner plot.png" />
</p>

The sampler should converge on parameters close to those used to synthesise (i.e., the blue lines should lie close to the peak of the 1D histograms above each column). Note that while `ultranest` comes bundled with the package `corner`, you will also need to install `scipy` in order to smooth the contours in the script provided.

You can also use the script `examples/plot posterior time series.py` to sample the posteriors and plot the corresponding time series to compare it to the original data:

<p align='center'>
<img width="50%" src="assets/example posterior time series.png" />
</p>

Finally, you can also visualise the 3D geometry of the magnetic field using the script `examples/plot 3D geometry.py`. This shows the rotation axis, magnetic axis, and magnetic precession relative to the line of sight:

<p align='center'>
<img width="50%" src="assets/example 3D geometry.png" />
</p>

## Parallelisation
CHARM can be parallelised easily using `MPI` and the Python package `mpi4py`. Once installed, simply import `mpi4py` in `script.py` where you call `sampler` and then run
```
mpiexec -np n python script.py
```
where `n` is the number of processors you wish to use. See [here](https://johannesbuchner.github.io/UltraNest/performance.html#parallelisation) for more details.

## Use cases
As of April 2026, CHARM has been used in the following works:
- Forecasting the detection yields of brown dwarfs for different build configurations of the [Square Kilometre Array](https://www.skao.int) (Kavanagh+ in press).
- Constraining the magnetic geometry of the brown dwarf WISE J112254.72+255022.2 ([Guirado+ 2025](https://doi.org/10.3847/1538-4357/add5f3)).
