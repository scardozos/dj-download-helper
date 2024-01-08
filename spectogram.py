import librosa
import numpy as np
import librosa.display
#from matplotlib import use
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure

# use("TkAgg")

def load_audio(file_path, sample_rate=44100):
    audio, sr = librosa.load(file_path, sr=sample_rate, mono=False)
    return audio, sr

def calculate_spectrogram(audio, sample_rate):
    mono_audio = librosa.to_mono(audio)
    stft = librosa.stft(mono_audio)
    spectrogram = librosa.amplitude_to_db(np.abs(stft), ref=np.max, top_db=120)
    return spectrogram

def calculate_stereo_image(audio):
    left_channel = audio[0, :]
    right_channel = audio[1, :]
    stereo_image = left_channel - right_channel
    return stereo_image

def time_ticks(x, _):
    hours, remainder = divmod(int(x), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

if __name__ == "__main__":
    file_path = "sample-song.mp3"
    audio, sample_rate = load_audio(file_path)

    spectrogram = calculate_spectrogram(audio, sample_rate)
    stereo_image = calculate_stereo_image(audio)

    # Set the minimum decibels and maximum frequency for the spectrogram
    min_decibels = -120
    max_frequency = 22000

    # Generate time values for each sample in the stereo image
    duration = len(audio[0]) / sample_rate

    time_values = np.arange(0, len(stereo_image)) / sample_rate

    # Plot the spectrogram and stereo image as subplots
    plt.figure(figsize=(12, 8))

    # Plot the Spectrogram
    plt.subplot(2, 1, 1)
    librosa.display.specshow(spectrogram, sr=sample_rate, x_axis="time", y_axis="hz", vmin=min_decibels, vmax=0)
    plt.title("Spectrogram")
    plt.colorbar(format='%+2.0f dB')
    plt.ylim(0, max_frequency)
    plt.yticks(np.arange(0, max_frequency + 2000, 2000), ['0', '2k', '4k', '6k', '8k', '10k', '12k', '14k', '16k', '18k', '20k', '22k'])

    # Plot the Stereo Image
    plt.subplot(2, 1, 2)
    # Plot stereo image with time values
    plt.plot(time_values, stereo_image)
    plt.title("Stereo Image")
    plt.xlabel('Time (s)')
    plt.xticks(np.arange(0, duration + 1, 60), [time_ticks(x, None) for x in np.arange(0, duration + 1, 60)])

    # Adjust layout and display the plot
    plt.margins(x=0)  # Set x-axis margin to zero
    plt.subplots_adjust(left=0.1, right=0.9)  # Adjust left and right margins

    plt.tight_layout()
    plt.show()