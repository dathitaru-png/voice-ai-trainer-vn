"""Frame-level acoustic features computed from raw PCM, stdlib only.

These are teaching-grade features, not a production front end: frame
energy, zero-crossing rate, and a small pure-Python DFT used to summarize
the magnitude spectrum into energy bands. They are enough to show how a
training pipeline turns waveforms into numbers a model can learn from.
"""

from __future__ import annotations

import math


def frame_energy(frame: list[int]) -> float:
    """Mean squared amplitude of one frame (0.0 for an empty frame)."""
    if not frame:
        return 0.0
    return sum(s * s for s in frame) / len(frame)


def zero_crossing_rate(frame: list[int]) -> float:
    """Fraction of adjacent sample pairs that change sign.

    Returns 0.0 for frames shorter than two samples. Higher values mean
    a noisier or higher-frequency signal.
    """
    if len(frame) < 2:
        return 0.0
    crossings = 0
    for prev, cur in zip(frame, frame[1:]):
        if (prev >= 0) != (cur >= 0) and prev != cur:
            crossings += 1
    return crossings / (len(frame) - 1)


def magnitude_spectrum(frame: list[int]) -> list[float]:
    """Magnitude spectrum of a frame via a naive DFT (bins 0 to n // 2).

    The naive DFT is O(n squared), so it is meant for short teaching
    frames (for example 256 samples), not for long recordings.
    """
    n = len(frame)
    if n == 0:
        return []
    spectrum = []
    for k in range(n // 2 + 1):
        real = 0.0
        imag = 0.0
        for t, sample in enumerate(frame):
            angle = -2.0 * math.pi * k * t / n
            real += sample * math.cos(angle)
            imag += sample * math.sin(angle)
        spectrum.append(math.hypot(real, imag))
    return spectrum


def band_energies(
    frame: list[int],
    sample_rate: int,
    bands: list[tuple[float, float]],
) -> list[float]:
    """Sum squared magnitudes of the spectrum inside each frequency band.

    ``bands`` is a list of (low_hz, high_hz) pairs. Band edges are
    inclusive on the low side and exclusive on the high side.
    """
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    spectrum = magnitude_spectrum(frame)
    n = len(frame)
    energies = [0.0] * len(bands)
    for k, magnitude in enumerate(spectrum):
        freq = k * sample_rate / n if n else 0.0
        for i, (low, high) in enumerate(bands):
            if low <= freq < high:
                energies[i] += magnitude * magnitude
                break
    return energies


def dominant_band(
    frame: list[int],
    sample_rate: int,
    bands: list[tuple[float, float]],
) -> int:
    """Index of the band with the highest energy, or -1 for empty input."""
    if not frame:
        return -1
    energies = band_energies(frame, sample_rate, bands)
    return max(range(len(energies)), key=lambda i: energies[i])
