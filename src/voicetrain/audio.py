"""WAV audio handling with the Python standard library only.

VoiceTrainer VN works with plain PCM WAV files, the format most recording
tools and datasets use for speech. All helpers here are offline and
dependency free.
"""

from __future__ import annotations

import math
import struct
import wave
from dataclasses import dataclass


class WavError(ValueError):
    """Raised when a WAV file is missing, corrupt, or unsupported."""


@dataclass(frozen=True)
class WavInfo:
    """Metadata of a PCM WAV file."""

    channels: int
    sample_width: int  # bytes per sample: 1, 2, or 4
    frame_rate: int
    n_frames: int

    @property
    def duration(self) -> float:
        """Length of the audio in seconds."""
        if self.frame_rate <= 0:
            return 0.0
        return self.n_frames / self.frame_rate


_SUPPORTED_WIDTHS = {1, 2, 4}


def read_wav_info(path: str) -> WavInfo:
    """Read only the header of a WAV file, without loading samples."""
    try:
        with wave.open(path, "rb") as wav:
            channels = wav.getnchannels()
            width = wav.getsampwidth()
            rate = wav.getframerate()
            frames = wav.getnframes()
    except (wave.Error, EOFError, OSError) as exc:
        raise WavError(f"cannot read WAV file {path!r}: {exc}") from exc
    if width not in _SUPPORTED_WIDTHS:
        raise WavError(f"unsupported sample width {width} in {path!r}")
    if channels < 1 or rate <= 0:
        raise WavError(f"invalid WAV header in {path!r}")
    return WavInfo(channels, width, rate, frames)


def read_wav(path: str) -> tuple[WavInfo, list[int]]:
    """Read a mono PCM WAV file and return its info and signed samples.

    Multi-channel files are downmixed to mono by averaging channels, so
    every downstream step can assume a single channel.
    """
    info = read_wav_info(path)
    try:
        with wave.open(path, "rb") as wav:
            raw = wav.readframes(info.n_frames)
    except (wave.Error, EOFError, OSError) as exc:
        raise WavError(f"cannot read WAV file {path!r}: {exc}") from exc

    fmt_char = {1: "B", 2: "h", 4: "i"}[info.sample_width]
    count = len(raw) // info.sample_width
    values = list(struct.unpack(f"<{count}{fmt_char}", raw[: count * info.sample_width]))
    if info.sample_width == 1:
        # 8-bit WAV samples are unsigned; shift to signed range.
        values = [v - 128 for v in values]
    if info.channels > 1:
        frames = []
        for i in range(0, len(values) - info.channels + 1, info.channels):
            frames.append(sum(values[i : i + info.channels]) // info.channels)
        values = frames
    return info, values


def write_wav(
    path: str,
    samples: list[int],
    sample_rate: int,
    channels: int = 1,
    sample_width: int = 2,
) -> WavInfo:
    """Write signed 16-bit (or 8/32-bit) PCM samples to a WAV file."""
    if sample_width not in _SUPPORTED_WIDTHS:
        raise WavError(f"unsupported sample width {sample_width}")
    fmt_char = {1: "B", 2: "h", 4: "i"}[sample_width]
    if sample_width == 1:
        values = [max(0, min(255, s + 128)) for s in samples]
    else:
        limit = (1 << (8 * sample_width - 1)) - 1
        values = [max(-limit - 1, min(limit, s)) for s in samples]
    raw = struct.pack(f"<{len(values)}{fmt_char}", *values)
    with wave.open(path, "wb") as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(sample_width)
        wav.setframerate(sample_rate)
        wav.writeframes(raw)
    return WavInfo(channels, sample_width, sample_rate, len(samples) // channels)


def rms(samples: list[int]) -> float:
    """Root-mean-square energy of a sample list; 0.0 for empty input."""
    if not samples:
        return 0.0
    return math.sqrt(sum(s * s for s in samples) / len(samples))


def is_silent(samples: list[int], threshold: float = 1.0) -> bool:
    """True when the RMS energy is at or below the silence threshold."""
    return rms(samples) <= threshold


def chunk(samples: list[int], frame_size: int, hop: int | None = None) -> list[list[int]]:
    """Split samples into fixed-length frames.

    ``hop`` defaults to ``frame_size`` (non-overlapping frames). The final
    partial frame is dropped, keeping every frame the same length.
    """
    if frame_size <= 0:
        raise ValueError("frame_size must be positive")
    if hop is None:
        hop = frame_size
    if hop <= 0:
        raise ValueError("hop must be positive")
    frames = []
    start = 0
    while start + frame_size <= len(samples):
        frames.append(samples[start : start + frame_size])
        start += hop
    return frames
