"""VoiceTrainer VN: an offline, stdlib-only pipeline toolkit for voice AI training."""

from .audio import WavInfo, chunk, is_silent, read_wav, read_wav_info, rms, write_wav
from .dataset import Utterance, build_manifest, filter_by_duration, load_manifest, split
from .eval import cer, per_utterance_report, wer
from .features import band_energies, dominant_band, frame_energy, magnitude_spectrum, zero_crossing_rate
from .textnorm import normalize, number_to_words
from .train import SoftmaxClassifier, make_synthetic_tone_data

__version__ = "0.1.0"

__all__ = [
    "WavInfo",
    "Utterance",
    "band_energies",
    "build_manifest",
    "cer",
    "chunk",
    "dominant_band",
    "filter_by_duration",
    "frame_energy",
    "is_silent",
    "load_manifest",
    "magnitude_spectrum",
    "make_synthetic_tone_data",
    "normalize",
    "number_to_words",
    "per_utterance_report",
    "read_wav",
    "read_wav_info",
    "rms",
    "split",
    "SoftmaxClassifier",
    "wer",
    "write_wav",
    "zero_crossing_rate",
    "__version__",
]
