"""Tests for acoustic features, the training loop, WER/CER, and the CLI."""

import math

import pytest

from voicetrain.cli import main as cli_main
from voicetrain.eval import cer, per_utterance_report, wer
from voicetrain.features import band_energies, dominant_band, frame_energy, zero_crossing_rate
from voicetrain.train import SoftmaxClassifier, make_synthetic_tone_data

SAMPLE_RATE = 8000
BANDS = [(0.0, 500.0), (500.0, 1000.0), (1000.0, 2000.0), (2000.0, 4000.0)]


def _sine(freq, duration=0.5, amplitude=12000):
    count = int(SAMPLE_RATE * duration)
    return [int(amplitude * math.sin(2 * math.pi * freq * t / SAMPLE_RATE)) for t in range(count)]


def test_frame_energy_and_silence():
    assert frame_energy([0] * 100) == 0.0
    assert frame_energy([3, 4]) == pytest.approx(12.5)
    assert frame_energy([]) == 0.0


def test_zero_crossing_rate_orders_by_frequency():
    low = _sine(200.0)
    high = _sine(2000.0)
    assert zero_crossing_rate(low) < zero_crossing_rate(high)
    assert zero_crossing_rate([0] * 100) == 0.0
    assert zero_crossing_rate([5]) == 0.0


def test_dominant_band_detects_pure_tone():
    frame = _sine(440.0)[:256]
    assert dominant_band(frame, SAMPLE_RATE, BANDS) == 0
    frame_high = _sine(1500.0)[:256]
    assert dominant_band(frame_high, SAMPLE_RATE, BANDS) == 2
    energies = band_energies(frame, SAMPLE_RATE, BANDS)
    assert len(energies) == 4
    assert energies[0] == max(energies)


def test_training_loop_decreases_loss_and_beats_chance():
    features, labels = make_synthetic_tone_data(n_per_class=30, seed=7)
    model = SoftmaxClassifier(n_features=3, n_classes=3)
    model.fit(features, labels, epochs=50, learning_rate=0.5)
    assert model.loss_history[-1] < model.loss_history[0]
    assert model.score(features, labels) > 0.8  # chance is 1/3


def test_wer_hand_computed_values():
    assert wer("hello world", "hello world") == 0.0
    assert wer("a b c", "a c") == pytest.approx(1 / 3)
    assert wer("a b c", "a x c") == pytest.approx(1 / 3)  # one substitution
    assert wer("a b", "a b c d") == pytest.approx(1.0)  # two insertions / 2 words
    assert wer("", "") == 0.0


def test_cer_hand_computed_values():
    assert cer("hello world", "hello world") == 0.0
    # "helloworld" vs "helloword": one deletion over 10 characters.
    assert cer("hello world", "hello word") == pytest.approx(0.1)
    report = per_utterance_report([("a b", "a b")])
    assert report[0]["wer"] == 0.0 and report[0]["cer"] == 0.0


def test_cli_normalize_and_wer(capsys):
    assert cli_main(["normalize", "Tôi có 2 con mèo."]) == 0
    assert capsys.readouterr().out.strip() == "tôi có hai con mèo."
    assert cli_main(["wer", "a b c", "a c"]) == 0
    out = capsys.readouterr().out
    assert "0.333" in out


def test_cli_demo_runs(capsys):
    assert cli_main(["demo", "--epochs", "5"]) == 0
    out = capsys.readouterr().out
    assert "epoch 1: loss" in out
    assert "final accuracy" in out


def test_cli_validate_on_synthetic_manifest(tmp_path, capsys):
    from voicetrain.audio import write_wav
    from voicetrain.dataset import Utterance, build_manifest

    wav = str(tmp_path / "utt.wav")
    write_wav(wav, _sine(440.0, duration=0.5), SAMPLE_RATE)
    manifest = str(tmp_path / "manifest.jsonl")
    build_manifest([Utterance(audio=wav, transcript="xin chào", duration=0.5)], manifest)
    assert cli_main(["validate", manifest]) == 0
    out = capsys.readouterr().out
    assert '"problems": 0' in out

    missing = str(tmp_path / "missing.jsonl")
    build_manifest([Utterance(audio=str(tmp_path / "nope.wav"), transcript="x", duration=1.0)], missing)
    assert cli_main(["validate", missing]) == 1
