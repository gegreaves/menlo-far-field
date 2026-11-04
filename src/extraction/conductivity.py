import numpy as np

epsilon_0 = 8.854187817e-12  # Vacuum permittivity in F/m

def from_permittivity(properties, background_permittivity=1.0):
    """
    Calculate the effective conductivity from the complex permittivity.

    Parameters:
    frequency (array-like): Frequency values in Hz.
    permittivity (array-like): Complex permittivity values.

    Returns:
    array-like: Effective conductivity values in S/m.
    """
    # Convert frequency to angular frequency
    omega = 2 * np.pi * properties.frequency * 1e12  # Convert THz to Hz

    # Calculate conductivity
    sigma = -1j*omega * (properties.permittivity - background_permittivity) * epsilon_0

    return sigma