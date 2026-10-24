"""Build a tiny synthetic dataset: a few WAV tones plus a JSONL manifest.

All audio is generated, not recorded: pure sine tones at different
frequencies stand in for utterances, and the transcripts are fictional
Vietnamese sentences. Run from the repository root:

    python examples/build_synthetic_dataset.py --out synthetic_dataset
"""

from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from voicetrain.audio import write_wav
from voicetrain.dataset import Utterance, build_manifest
from voicetrain.textnorm import normalize

SAMPLE_RATE = 8000

# Fictional transcripts, one per tone. They describe the tone, so the
# dataset stays obviously synthetic.
TRANSCRIPTS = [
    "xin chào mọi người",
    "hôm nay trời đẹp quá",
    "tôi đang học trí tuệ nhân tạo",
    "giọng nói là dữ liệu quý",
    "hãy nói chậm và rõ ràng",
    "đây là bản ghi thử nghiệm",
]


def sine_tone(freq_hz: float, duration: float, amplitude: int = 12000) -> list[int]:
    """Generate a pure sine tone at the given frequency."""
    count = int(SAMPLE_RATE * duration)
    return [
        int(amplitude * math.sin(2.0 * math.pi * freq_hz * t / SAMPLE_RATE))
        for t in range(count)
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a synthetic voice dataset")
    parser.add_argument("--out", default="synthetic_dataset", help="output directory")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    utterances: list[Utterance] = []
    for i, transcript in enumerate(TRANSCRIPTS):
        freq = 300.0 + 120.0 * i
        samples = sine_tone(freq, duration=1.0)
        name = f"utt_{i:02d}.wav"
        path = os.path.join(args.out, name)
        info = write_wav(path, samples, SAMPLE_RATE)
        utterances.append(
            Utterance(audio=path, transcript=normalize(transcript), duration=info.duration)
        )
    manifest = os.path.join(args.out, "manifest.jsonl")
    count = build_manifest(utterances, manifest)
    print(f"wrote {count} utterances to {manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
