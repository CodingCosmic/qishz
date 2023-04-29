import math
import numpy as np
import matplotlib.pyplot as plt
from pyaudio import PyAudio


def calculate_biased_frequency(frequency, probability=0.0168):
    theta = 2 * math.acos(math.sqrt(1 - probability))
    bias_factor = math.sin(theta / 2) ** 2
    return frequency * bias_factor


def harmonic_resonator_calculator(frequency):
    harmonics = [frequency * n for n in range(1, 6)]
    subharmonics = [frequency / n for n in range(1, 6)]

    biased_harmonics = [calculate_biased_frequency(h) for h in harmonics]
    biased_subharmonics = [calculate_biased_frequency(sh) for sh in subharmonics]

    return harmonics, subharmonics, biased_harmonics, biased_subharmonics


def generate_carrier_wave(frequency, duration=1, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
    carrier_wave = np.sin(2 * np.pi * frequency * t)
    return carrier_wave


def play_carrier_wave(carrier_wave, sample_rate=44100):
    p = PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sample_rate,
                    output=True)

    stream.write(carrier_wave.tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()


def plot_carrier_wave(carrier_wave, sample_rate=44100):
    t = np.linspace(0, len(carrier_wave) / sample_rate, num=len(carrier_wave))
    plt.plot(t, carrier_wave)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Carrier Wave')
    plt.show()


def detect_anomalies(data, threshold=2):
    mean = np.mean(data)
    std_dev = np.std(data)
    anomalies = []

    for i, value in enumerate(data):
        z_score = (value - mean) / std_dev
        if np.abs(z_score) > threshold:
            anomalies.append((i, value))

    return anomalies


input_frequency = float(input("Enter the frequency in Hz (0 to 300 GHz): "))
input_frequency *= 1e9 if input_frequency <= 300 else 300e9

harmonics, subharmonics, biased_harmonics, biased_subharmonics = harmonic_resonator_calculator(input_frequency)

print("\nHarmonics:")
for i, h in enumerate(harmonics):
    print(f"Harmonic {i + 1}: {h:.2f} Hz (biased: {biased_harmonics[i]:.2f} Hz)")

print("\nSubharmonics:")
for i, sh in enumerate(subharmonics):
    print(f"Subharmonic {i + 1}: {sh:.2f} Hz (biased: {biased_subharmonics[i]:.2f} Hz)")

carrier_wave = generate_carrier_wave(input_frequency)
plot_carrier_wave(carrier_wave)

sensor_data = np.random.rand(1000)  # Replace this with your actual sensor data
anomalies = detect_anomalies(sensor_data)

print("\nAnomalies detected:")
for index, value in anomalies:
    print
