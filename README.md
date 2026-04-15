# CHARM
CHARM is a framework for characterising magnetic fields via Bayesian inference from radio-emitting objects like stars, brown dwarfs, and planets. Different physical models can be assumed for the magnetic field and its associated emission. It uses the nested sampling algorithm [UltraNest](https://johannesbuchner.github.io/UltraNest/) to explore the complex high-dimensional likelihood space of the chosen model given the time series data, providing probabilistic inferences (posteriors) for each model parameter.

So far, the following model has been implemented:

### Active field line
The model assumes that the emission originates from an **active field line** within a dipolar magnetic field that rotates rigidly with the magnetised object, driven by the electron cyclotron maser instability. 

## Published use cases (as of March 2026)
- Constraining the magnetic geometry of the brown dwarf WISE J112254.72+255022.2 ([Guirado+ 2025](https://doi.org/10.3847/1538-4357/add5f3)).