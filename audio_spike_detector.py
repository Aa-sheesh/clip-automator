import librosa
import numpy as np

def detect_audio_spikes(audio_path, clip_window=2):
    """
    Detects audio spikes by peak picking on onset envelope.

    Parameters:
    - audio_path: Path to WAV audio file
    - clip_window: seconds before and after each spike for clip extraction

    Returns:
    - List of (start_sec, end_sec) tuples representing clip time ranges
    """
    y, sr = librosa.load(audio_path, sr=None)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    # Stricter parameters to reduce large intervals and separate spikes
    delta = 0.7       # Increased threshold for peak picking
    wait = 30         # Minimum frames between detected peaks

    peaks = librosa.util.peak_pick(onset_env,
                                  pre_max=3,
                                  post_max=3,
                                  pre_avg=3,
                                  post_avg=3,
                                  delta=delta,
                                  wait=wait)

    times = librosa.frames_to_time(peaks, sr=sr)
    clips = []
    for t in times:
        start = max(0, t - clip_window)
        end = t + clip_window
        clips.append((start, end))

    # Optional: merge overlapping intervals to avoid near-duplicate clips
    merged_clips = []
    for start, end in sorted(clips):
        if merged_clips and start <= merged_clips[-1][1]:
            merged_clips[-1] = (merged_clips[-1][0], max(end, merged_clips[-1][1]))
        else:
            merged_clips.append((start, end))

    return merged_clips
