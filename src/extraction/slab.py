import numpy as np

from thz import OpticalProperties


def extract_properties(THzSpectrum, thickness, fit_range=None):
    """
    Extracts optical properties from a THz spectrum.
    Formulae are consisent with Fourier convention used
    (i.e E(w) = integral E(t) exp(-i*w*t) dt,
    so a positive time delay produces a negative phase shift)
    """
    frequency = THzSpectrum.data["Frequency (THz)"].values
    phase = THzSpectrum.unwrapped_phase
    if fit_range is not None:
        phase = THzSpectrum.corrected_phase(fit_range)
    n = (1-2.998e8 / (2 * np.pi * frequency * 1e12 * thickness) * phase)
    kappa = (2.998e8
             / (2 * np.pi * frequency * 1e12 * thickness)
             * (np.log((4 * n)/(n+1)**2)-np.log(
                 np.abs(THzSpectrum.data["Spectrum (a.u.)"].values)
                 )))
    alpha = 4 * np.pi * frequency * 1e12 * kappa / 2.998e8 / 100  # (in cm^-1)
    epsilon = n**2 - kappa**2 + 1j * 2 * n * kappa
    return OpticalProperties(frequency=frequency,
                             refractive_index=n,
                             extinction_coefficient=kappa,
                             absorption_coefficient=alpha,
                             permittivity=epsilon)
