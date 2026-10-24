"""Tests for WAV handling, RMS, silence detection, and chunking."""

import math
import os

import pytest

from voicetrain.audio import WavError, chunk, is_silent, read_wav, read_wav_info, rms, write_wav

SAMPLE_RATE = 8000


def _sine(freq=440.0, duration=1.0, amplitude=12000):
    count = int(SAMPLE_RATE * duration)
    return [int(amplitude * math.sin(2 * math.pi * freq * t / SAMPLE_RATE)) for t in range(count)]


def test_wav_metadata_and_duration(tmp_path):
    path = str(tmp_path / "tone.wav")
    info = write_wav(path, _sine(duration=0.5), SAMPLE_RATE)
    assert info.frame_rate == SAMPLE_RATE
    assert info.channels == 1
    assert info.sample_width == 2
    assert info.duration == pytest.approx(0.5, abs=1e-6)
    header = read_wav_info(path)
    assert header == info


def test_wav_round_trip_preserves_samples(tmp_path):
    path = str(tmp_path / "tone.wav")
    samples = _sine(duration=0.25)
    write_wav(path, samples, SAMPLE_RATE)
    _, loaded = read_wav(path)
    assert loaded == samples


def test_rms_of_sine_and_silence():
    silence = [0] * 800
    assert rms(silence) == 0.0
    assert is_silent(silence)
    tone = _sine(amplitude=12000)
    # RMS of a sine wave is amplitude / sqrt(2).
    assert rms(tone) == pytest.approx(12000 / math.sqrt(2), rel=0.01)
    assert not is_silent(tone)


def test_chunking_drops_partial_tail():
    samples = list(range(1000))
    frames = chunk(samples, frame_size=256)
    assert len(frames) == 3
    assert all(len(f) == 256 for f in frames)
    assert frames[0] == list(range(256))
    overlapped = chunk(samples, frame_size=256, hop=128)
    assert len(overlapped) == 6


def test_invalid_wav_raises(tmp_path):
    bad = tmp_path / "notaudio.wav"
    bad.write_text("this is not a wav file")
    with pytest.raises(WavError):
        read_wav_info(str(bad))
    with pytest.raises(WavError):
        write_wav(str(tmp_path / "x.wav"), [1, 2], SAMPLE_RATE, sample_width=3)


def test_chunk_rejects_bad_sizes():
    with pytest.raises(ValueError):
        chunk([1, 2, 3], frame_size=0)
    with pytest.raises(ValueError):
        chunk([1, 2, 3], frame_size=2, hop=0)
