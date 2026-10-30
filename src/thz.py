import pandas as pd
import numpy as np

class THzWaveform:
    def __init__(self, data):
        self.data = data

    @classmethod
    def from_file(cls, file_path):
        data = pd.read_csv(file_path, skiprows=7, delimiter="\t", names=["Time (ps)", "Amplitude (a.u.)"])
        return cls(data)

    def fft(self):
        # Perform FFT on the waveform data
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


class THzSpectrum:
    def __init__(self, data):
        self.data = data

    @classmethod
    def from_file(cls, file_path):
        data = pd.read_csv(file_path, delimiter="\t", skiprows=7, names=["Frequency (THz)", "Spectrum (a.u.)"])
        data['Spectrum (a.u.)'] = 10**(data['Spectrum (a.u.)']/20) # This is 20, not 10, because the software uses the power convention for db.
        return cls(data)

    @property
    def amplitude_db(self):
        return 20 * np.log10(np.abs(self.amplitude))

    @property
    def unwrapped_phase(self):
        return np.unwrap(np.angle(self.data['Spectrum (a.u.)']))
    
    def normalise(self,reference: "THzSpectrum"):
        normalised_data = pd.DataFrame({
            "Frequency (THz)": self.data["Frequency (THz)"],
            "Spectrum (a.u.)": self.data["Spectrum (a.u.)"] / reference.data["Spectrum (a.u.)"]
        })
        return THzSpectrum(normalised_data)

