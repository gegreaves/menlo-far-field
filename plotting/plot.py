import matplotlib.pyplot as plt
import numpy as np
from src.thz import THzSpectrum

def plot_spectrum(THzSpectrum, ax=None, freq_range=None, style_path="plotting/styles/thz.mplstyle", **kwargs):
    with plt.style.context(style_path):
        if ax is None:
            fig,(ax_amp,ax_phase) = plt.subplots(2,1, sharex=True)
        else:
            fig = ax[0].figure
            ax_amp = ax[0]
            ax_phase = ax[1]
        ax_amp.plot(THzSpectrum.data["Frequency (THz)"], np.abs(THzSpectrum.data["Spectrum (a.u.)"]), **kwargs)
        ax_amp.set(
        ylabel="Amplitude (a.u.)", title="THz Spectrum", xlim=freq_range
        )
        ax_phase.plot(THzSpectrum.data["Frequency (THz)"], THzSpectrum.unwrapped_phase, **kwargs)
        ax_phase.set(
    xlabel="Frequency (THz)", ylabel="Phase (rad)", title="THz Phase", xlim=freq_range
        )
    return(fig,(ax_amp,ax_phase))

def plot_waveform(THzWaveform, ax=None, time_range=None, style_path="plotting/styles/thz.mplstyle", **kwargs):
    with plt.style.context(style_path):
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