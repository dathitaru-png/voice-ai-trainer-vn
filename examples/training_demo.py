"""Training-run demo: loss and accuracy per epoch on synthetic tones.

This is the same demo the `voicetrain demo` command runs, written out
so readers can follow every step. Run from the repository root:

    python examples/training_demo.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from voicetrain.train import SoftmaxClassifier, make_synthetic_tone_data


def main() -> int:
    features, labels = make_synthetic_tone_data(n_per_class=30, seed=7)
    model = SoftmaxClassifier(n_features=3, n_classes=3)
    model.fit(features, labels, epochs=50, learning_rate=0.5)
    print("Synthetic tone classification (3 classes, clearly fictional data)")
    for epoch, loss in enumerate(model.loss_history, start=1):
        if epoch == 1 or epoch % 10 == 0:
            print(f"  epoch {epoch:>2}: loss {loss:.4f}")
    print(f"final accuracy: {model.score(features, labels):.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
