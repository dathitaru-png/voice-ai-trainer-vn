"""Dataset manifests and deterministic splits for speech training data.

A manifest is a JSONL file: one JSON object per line with an ``audio``
path, a ``transcript`` string, and a ``duration`` in seconds. Keeping the
manifest separate from the audio files makes datasets auditable without
moving large files around.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Utterance:
    """One training example: an audio file and its transcript."""

    audio: str
    transcript: str
    duration: float


def build_manifest(utterances: list[Utterance], path: str) -> int:
    """Write utterances to a JSONL manifest. Returns the number written."""
    with open(path, "w", encoding="utf-8") as handle:
        for item in utterances:
            record = {
                "audio": item.audio,
                "transcript": item.transcript,
                "duration": item.duration,
            }
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return len(utterances)


def load_manifest(path: str) -> list[Utterance]:
    """Load a JSONL manifest, skipping blank lines."""
    items: list[Utterance] = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            items.append(
                Utterance(
                    audio=record["audio"],
                    transcript=record["transcript"],
                    duration=float(record["duration"]),
                )
            )
    return items


def split(
    items: list[Utterance],
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    seed: int = 42,
) -> dict[str, list[Utterance]]:
    """Deterministically split items into train, validation, and test sets.

    The same seed always produces the same split, and the three sets are
    disjoint. The remaining share after train and validation goes to test.
    """
    if not 0.0 < train_ratio < 1.0 or not 0.0 <= val_ratio < 1.0:
        raise ValueError("ratios must be in range and train_ratio below 1.0")
    if train_ratio + val_ratio >= 1.0:
        raise ValueError("train_ratio + val_ratio must be below 1.0")
    shuffled = list(items)
    random.Random(seed).shuffle(shuffled)
    n = len(shuffled)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)
    return {
        "train": shuffled[:n_train],
        "validation": shuffled[n_train : n_train + n_val],
        "test": shuffled[n_train + n_val :],
    }


def filter_by_duration(
    items: list[Utterance], min_duration: float = 0.0, max_duration: float = 60.0
) -> list[Utterance]:
    """Keep only utterances whose duration falls inside [min, max]."""
    return [item for item in items if min_duration <= item.duration <= max_duration]
