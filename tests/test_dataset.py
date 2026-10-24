"""Tests for dataset manifests, deterministic splits, and duration filters."""

from voicetrain.dataset import Utterance, build_manifest, filter_by_duration, load_manifest, split


def _items(n=20):
    return [Utterance(audio=f"utt_{i:02d}.wav", transcript=f"câu {i}", duration=0.5 + i * 0.1) for i in range(n)]


def test_manifest_round_trip(tmp_path):
    path = str(tmp_path / "manifest.jsonl")
    items = _items(5)
    assert build_manifest(items, path) == 5
    loaded = load_manifest(path)
    assert loaded == items


def test_splits_are_deterministic_and_disjoint():
    items = _items(100)
    first = split(items, seed=42)
    second = split(items, seed=42)
    assert first == second
    assert len(first["train"]) == 80
    assert len(first["validation"]) == 10
    assert len(first["test"]) == 10
    all_audios = (
        [u.audio for u in first["train"]]
        + [u.audio for u in first["validation"]]
        + [u.audio for u in first["test"]]
    )
    assert len(set(all_audios)) == 100


def test_split_rejects_bad_ratios():
    import pytest

    with pytest.raises(ValueError):
        split(_items(10), train_ratio=0.9, val_ratio=0.2)


def test_duration_filter_drops_out_of_range():
    items = _items(10)  # durations 0.5 .. 1.4
    kept = filter_by_duration(items, min_duration=0.8, max_duration=1.1)
    assert [u.audio for u in kept] == ["utt_03.wav", "utt_04.wav", "utt_05.wav", "utt_06.wav"]
    assert filter_by_duration(items, min_duration=5.0) == []
