import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def visualize_onset_peaks(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    delta = 0.7
    wait = 30

    peaks = librosa.util.peak_pick(onset_env,
                                  pre_max=3,
                                  post_max=3,
                                  pre_avg=3,
                                  post_avg=3,
                                  delta=delta,
                                  wait=wait)

    times = librosa.frames_to_time(np.arange(len(onset_env)), sr=sr)
    peak_times = librosa.frames_to_time(peaks, sr=sr)

    plt.figure(figsize=(14, 5))
    plt.plot(times, onset_env, label='Onset strength envelope')
    plt.vlines(peak_times, 0, onset_env.max(), color='r', alpha=0.9, linestyle='--', label='Detected peaks')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Onset strength')
    plt.title('Audio Onset Envelope and Detected Peaks')
    plt.legend()
    plt.savefig("onset_peaks_plot.png")
    print("Plot saved as onset_peaks_plot.png")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python visualize_onset_peaks.py path_to_audio.wav")
    else:
        visualize_onset_peaks(sys.argv[1])
