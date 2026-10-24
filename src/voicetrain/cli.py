"""Command line interface for VoiceTrainer VN.

Subcommands:
  validate <manifest>   Check WAV files, durations, and transcripts.
  normalize <text>      Normalize one transcript to training format.
  wer <ref> <hyp>       Print WER and CER for two transcripts.
  demo                  Run the synthetic training demo end to end.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from . import __version__
from .audio import WavError, read_wav_info
from .dataset import filter_by_duration, load_manifest
from .eval import cer, wer
from .textnorm import normalize
from .train import SoftmaxClassifier, make_synthetic_tone_data


def _cmd_validate(args: argparse.Namespace) -> int:
    items = load_manifest(args.manifest)
    problems = []
    checked = 0
    for item in items:
        checked += 1
        if not item.transcript.strip():
            problems.append({"audio": item.audio, "problem": "empty transcript"})
        if not os.path.exists(item.audio):
            problems.append({"audio": item.audio, "problem": "file missing"})
            continue
        try:
            info = read_wav_info(item.audio)
        except WavError as exc:
            problems.append({"audio": item.audio, "problem": str(exc)})
            continue
        if not args.min_duration <= info.duration <= args.max_duration:
            problems.append(
                {
                    "audio": item.audio,
                    "problem": f"duration {info.duration:.2f}s out of range",
                }
            )
    summary = {"checked": checked, "problems": len(problems), "details": problems}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not problems else 1


def _cmd_normalize(args: argparse.Namespace) -> int:
    print(normalize(args.text))
    return 0


def _cmd_wer(args: argparse.Namespace) -> int:
    result = {"wer": wer(args.reference, args.hypothesis), "cer": cer(args.reference, args.hypothesis)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def _cmd_demo(args: argparse.Namespace) -> int:
    features, labels = make_synthetic_tone_data(n_per_class=30, seed=7)
    model = SoftmaxClassifier(n_features=3, n_classes=3)
    model.fit(features, labels, epochs=args.epochs, learning_rate=0.5)
    for epoch, loss in enumerate(model.loss_history, start=1):
        print(f"epoch {epoch}: loss {loss:.4f}")
    print(f"final accuracy: {model.score(features, labels):.2f}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="voicetrain", description="Voice AI training pipeline toolkit")
    parser.add_argument("--version", action="version", version=f"voicetrain {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="validate a dataset manifest")
    validate.add_argument("manifest", help="path to the JSONL manifest")
    validate.add_argument("--min-duration", type=float, default=0.0)
    validate.add_argument("--max-duration", type=float, default=60.0)
    validate.set_defaults(func=_cmd_validate)

    norm = sub.add_parser("normalize", help="normalize a transcript")
    norm.add_argument("text", help="raw transcript text")
    norm.set_defaults(func=_cmd_normalize)

    wer_cmd = sub.add_parser("wer", help="compute WER and CER")
    wer_cmd.add_argument("reference", help="reference transcript")
    wer_cmd.add_argument("hypothesis", help="hypothesis transcript")
    wer_cmd.set_defaults(func=_cmd_wer)

    demo = sub.add_parser("demo", help="run the synthetic training demo")
    demo.add_argument("--epochs", type=int, default=50)
    demo.set_defaults(func=_cmd_demo)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
