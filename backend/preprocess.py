import librosa
import soundfile as sf
import numpy as np


TARGET_SR = 48000


def preprocess_audio(audio_path):
    """
    Load and preprocess audio for CLAP.

    Returns:
        waveform (np.ndarray)
        sample_rate (int)
    """

    # Load audio
    audio, sr = librosa.load(
        audio_path,
        sr=TARGET_SR,
        mono=True
    )

    # Trim silence
    audio, _ = librosa.effects.trim(audio)

    # Normalize loudness
    peak = np.max(np.abs(audio))

    if peak > 0:
        audio = audio / peak

    return audio, TARGET_SR