import pandas as pd
import numpy as np
from plotting.plot import plot_waveform
from plotting.plot import plot_spectrum
from plotting.plot import plot_optical_properties
import read_data

class THzWaveform:
    def __init__(self, data, metadata=None):
        self.data = data
        self.metadata = metadata

    @classmethod
    def from_file(cls, file_path):
        data = pd.read_csv(file_path, skiprows=7, delimiter="\t", names=["Time (ps)", "Amplitude (a.u.)"])
        metadata = read_data.read_header(file_path)
        return cls(data,metadata)

    def fft(self):
        # Perform FFT on the waveform data
        # Fourier convention:
        # E(w) = integral E(t) exp(-i*w*t) dt
        #
        # Therefore, a positive time delay tau produces:
        # E_delayed(w) = E(w) exp(-i*w*tau) (i.e. a negative phase shift)
        time = self.data["Time (ps)"].values
        amplitude = self.data["Amplitude (a.u.)"].values
        n = len(time)
        dt = np.mean(np.diff(time)) * 1e-12  # Convert ps to seconds
        freq = np.fft.fftfreq(n, d=dt)
        fft_amplitude = np.fft.fft(amplitude)

        # mask for positive values only
        mask = freq >= 0
        fft_amplitude = fft_amplitude[mask]
        freq = freq[mask]

        # Create a DataFrame for the spectrum
        spectrum_data = pd.DataFrame({
            "Frequency (THz)": freq * 1e-12,  # Convert Hz to THz
            "Spectrum (a.u.)": fft_amplitude
        })
        
        return THzSpectrum(spectrum_data)

    def plot(self, ax=None, time_range=None, style_path="plotting/styles/thz.mplstyle", **kwargs):
        return plot_waveform(self, ax=ax, time_range=time_range, style_path=style_path, **kwargs)


class THzSpectrum:
    def __init__(self, data, metadata=None):
        self.data = data
        self.metadata = metadata

    @classmethod
    def from_file(cls, file_path):
        data = pd.read_csv(file_path, delimiter="\t", skiprows=7, names=["Frequency (THz)", "Spectrum (a.u.)"])
        data['Spectrum (a.u.)'] = 10**(data['Spectrum (a.u.)']/20) # This is 20, not 10, because the software uses the power convention for db.
        metadata = read_data.read_header(file_path)
        return cls(data, metadata)

    @property
    def amplitude_db(self):
        return 20 * np.log10(np.abs(self.amplitude))

    @property
    def unwrapped_phase(self):
        return np.unwrap(np.angle(self.data['Spectrum (a.u.)']))

    def corrected_phase(self, fit_range):
        # Fit a linear function to the unwrapped phase in the specified frequency range
        freq = self.data["Frequency (THz)"].values
        phase = self.unwrapped_phase
        mask = (freq >= fit_range[0]) & (freq <= fit_range[1])
        coeffs = np.polyfit(freq[mask], phase[mask], 1)
        linear_fit = np.polyval(coeffs, freq)

        # Subtract the linear fit from the unwrapped phase to correct it
        corrected_phase = phase - coeffs[1] # Subtract the intercept to correct the phase
        return corrected_phase
    
    def normalise(self,reference: "THzSpectrum"):
        normalised_data = pd.DataFrame({
            "Frequency (THz)": self.data["Frequency (THz)"],
            "Spectrum (a.u.)": self.data["Spectrum (a.u.)"] / reference.data["Spectrum (a.u.)"]
        })
        return THzSpectrum(normalised_data)

    def plot(self, ax=None, freq_range=None, style_path="plotting/styles/thz.mplstyle", **kwargs):
        return plot_spectrum(self, ax=ax, freq_range=freq_range, style_path=style_path, **kwargs)


class OpticalProperties:
    def __init__(self, frequency = None, refractive_index=None, extinction_coefficient=None, absorption_coefficient=None, permittivity=None):
        self.frequency = frequency
        self.refractive_index = refractive_index
        self.extinction_coefficient = extinction_coefficient
        self.absorption_coefficient = absorption_coefficient
        self.permittivity = permittivity
        self.conductivity = None

    def plot(self, property = "refractive_index", ax=None, freq_range=None, style_path="plotting/styles/thz.mplstyle", **kwargs):
        return plot_optical_properties(self, property=property, ax=ax, freq_range=freq_range, style_path=style_path, **kwargs)
