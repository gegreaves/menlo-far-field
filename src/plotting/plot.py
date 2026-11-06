import matplotlib.pyplot as plt
import numpy as np

def plot_spectrum(THzSpectrum, ax=None, freq_range=None, fit_range = None, normalise=False, **kwargs):
    
    if ax is None:
        fig,(ax_amp,ax_phase) = plt.subplots(2,1, sharex=True)
    else:
        fig = ax[0].figure
        ax_amp = ax[0]
        ax_phase = ax[1]
    amplitude = np.abs(THzSpectrum.data["Spectrum (a.u.)"])
    if normalise:
        amplitude /= np.max(amplitude)
    ax_amp.plot(THzSpectrum.data["Frequency (THz)"], amplitude, **kwargs)
    ax_amp.set(
    ylabel="Amplitude (a.u.)", title="THz Spectrum", xlim=freq_range
    )
    if fit_range is not None:
        ax_phase.plot(THzSpectrum.data["Frequency (THz)"], THzSpectrum.corrected_phase(fit_range), **kwargs)
    else:
        ax_phase.plot(THzSpectrum.data["Frequency (THz)"], THzSpectrum.unwrapped_phase, **kwargs)
    ax_phase.set(
xlabel="Frequency (THz)", ylabel="Phase (rad)", title="THz Phase", xlim=freq_range
    )
    return(fig,(ax_amp,ax_phase))

def plot_waveform(THzWaveform, ax=None, time_range=None, **kwargs):
    
    if ax is None:
        fig,ax = plt.subplots()
    else:
        fig = ax.figure
        ax_amp = ax
        ax_phase = ax
    ax.plot(THzWaveform.data["Time (ps)"], THzWaveform.data["Amplitude (a.u.)"], **kwargs)
    ax.set(xlabel="Time (ps)", ylabel="Amplitude (a.u.)", title="THz Waveform", xlim=time_range
    ) 
    return(fig,ax)

PROPERTY_LABELS = {
    "refractive_index": {'title':"Refractive Index",
                         'ylabel':r"Refractive Index, $n$",
                         'complex': False},
    "extinction_coefficient": {'title':"Extinction Coefficient",
                               'ylabel':r"Extinction Coefficient, $\kappa$",
                               'complex': False},
    "absorption_coefficient": {'title':"Absorption Coefficient",
                               'ylabel':r"Absorption Coefficient, $\alpha$ (cm$^{-1}$)",
                               'complex': False},
    "permittivity": {'title':"Complex Permittivity",
                'ylabel':r"Complex Permittivity, $\epsilon$",
                'complex': True},
    "conductivity": {'title':"Complex Conductivity",
                'ylabel':r"Complex Conductivity, $\sigma$ (S/m)",
                'complex': True}
    }


def plot_optical_properties(OpticalProperties, property = "refractive_index", ax=None, freq_range=None, **kwargs):
    label = kwargs.pop("label", "") # take label out of kwargs so it doesn't get passed to ax.plot() twice
    if ax is None:
        fig,ax = plt.subplots()
    else:
        fig = ax.figure
    if PROPERTY_LABELS[property]['complex']:
        ax.plot(OpticalProperties.frequency, np.real(getattr(OpticalProperties, property)), label=f"{label} - Real", **kwargs)
        ax.plot(OpticalProperties.frequency, np.imag(getattr(OpticalProperties, property)), label=f"{label} - Imaginary", **kwargs)
        ax.legend()
    else:
        ax.plot(OpticalProperties.frequency, getattr(OpticalProperties, property), label=f"{label}", **kwargs)
    labels = PROPERTY_LABELS[property]
    ax.set(
    xlabel = "Frequency (THz)", ylabel=labels['ylabel'], title=labels['title'], xlim=freq_range
    )
    return(fig,ax)