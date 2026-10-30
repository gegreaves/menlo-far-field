import matplotlib.pyplot as plt
import numpy as np
from src.thz import THzSpectrum

def plot_spectrum(THzSpectrum, freq_range=None):
    fig,(ax_amp,ax_phase) = plt.subplots(2,1, sharex=True)
    ax_amp.plot(THzSpectrum.data["Frequency (THz)"], np.abs(THzSpectrum.data["Spectrum (a.u.)"]))
    ax_amp.set(
     ylabel="Amplitude (a.u.)", title="THz Spectrum", xlim=freq_range
    )
    ax_phase.plot(THzSpectrum.data["Frequency (THz)"], THzSpectrum.unwrapped_phase)
    ax_phase.set(
xlabel="Frequency (THz)", ylabel="Phase (rad)", title="THz Phase", xlim=freq_range
    )
    return(fig,(ax_amp,ax_phase))

def plot_waveform(THzWaveform, time_range=None):
    fig,ax = plt.subplots()
    ax.plot(THzWaveform.data["Time (ps)"], THzWaveform.data["Amplitude (a.u.)"])
    ax.set(xlabel="Time (ps)", ylabel="Amplitude (a.u.)", title="THz Waveform", xlim=time_range
    ) 
    return(fig,ax)