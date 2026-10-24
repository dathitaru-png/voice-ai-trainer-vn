"""A small, honest training loop: softmax classification by gradient descent.

This module exists to teach the training loop itself: forward pass,
cross-entropy loss, gradient step, and per-epoch reporting. It is not a
speech recognizer. The demo trains on synthetic tone features, where the
classes are separable by construction, so the loop can be verified
end to end without a real dataset.
"""

from __future__ import annotations

import math
import random


def _softmax(logits: list[float]) -> list[float]:
    top = max(logits)
    exps = [math.exp(value - top) for value in logits]
    total = sum(exps)
    return [value / total for value in exps]


def _normalize_features(features: list[list[float]]) -> tuple[list[list[float]], list[float], list[float]]:
    """Z-score normalize each feature column; returns (normalized, means, stds)."""
    if not features:
        return [], [], []
    n_cols = len(features[0])
    means = []
    stds = []
    for col in range(n_cols):
        values = [row[col] for row in features]
        mean = sum(values) / len(values)
        var = sum((v - mean) ** 2 for v in values) / len(values)
        means.append(mean)
        stds.append(math.sqrt(var) if var > 0 else 1.0)
    normalized = [
        [(row[col] - means[col]) / stds[col] for col in range(n_cols)] for row in features
    ]
    return normalized, means, stds


class SoftmaxClassifier:
    """Multiclass logistic regression trained by full-batch gradient descent."""

    def __init__(self, n_features: int, n_classes: int) -> None:
        self.weights = [[0.0] * n_features for _ in range(n_classes)]
        self.bias = [0.0] * n_classes
        self.loss_history: list[float] = []
        self.means: list[float] = []
        self.stds: list[float] = []

    def predict_proba(self, features: list[float]) -> list[float]:
        """Class probabilities for one feature vector."""
        logits = []
        for c in range(len(self.bias)):
            total = self.bias[c]
            for w, x in zip(self.weights[c], features):
                total += w * x
            logits.append(total)
        return _softmax(logits)

    def predict(self, features: list[float]) -> int:
        """The most likely class index for one feature vector."""
        probs = self.predict_proba(features)
        return max(range(len(probs)), key=lambda i: probs[i])

    def fit(
        self,
        features: list[list[float]],
        labels: list[int],
        epochs: int = 50,
        learning_rate: float = 0.5,
    ) -> "SoftmaxClassifier":
        """Train on normalized features; records cross-entropy loss per epoch."""
        if len(features) != len(labels):
            raise ValueError("features and labels must have the same length")
        if not features:
            raise ValueError("cannot train on empty data")
        normalized, self.means, self.stds = _normalize_features(features)
        n_classes = len(self.bias)
        n = len(normalized)
        for _ in range(epochs):
            grad_w = [[0.0] * len(normalized[0]) for _ in range(n_classes)]
            grad_b = [0.0] * n_classes
            loss = 0.0
            for x, y in zip(normalized, labels):
                probs = self.predict_proba(x)
                loss -= math.log(max(probs[y], 1e-12))
                for c in range(n_classes):
                    error = probs[c] - (1.0 if c == y else 0.0)
                    grad_b[c] += error
                    for j in range(len(x)):
                        grad_w[c][j] += error * x[j]
            for c in range(n_classes):
                self.bias[c] -= learning_rate * grad_b[c] / n
                for j in range(len(self.weights[c])):
                    self.weights[c][j] -= learning_rate * grad_w[c][j] / n
            self.loss_history.append(loss / n)
        return self

    def score(self, features: list[list[float]], labels: list[int]) -> float:
        """Accuracy on feature vectors (normalized with training statistics)."""
        if not features:
            return 0.0
        if not self.means or not self.stds:
            raise ValueError("call fit() before score()")
        correct = 0
        for row, label in zip(features, labels):
            normalized = [(row[j] - self.means[j]) / self.stds[j] for j in range(len(row))]
            if self.predict(normalized) == label:
                correct += 1
        return correct / len(features)


def make_synthetic_tone_data(
    n_per_class: int = 30, seed: int = 7
) -> tuple[list[list[float]], list[int]]:
    """Synthetic band-energy features for three tone classes.

    Class 0 centers energy in the low band, class 1 in the mid band, and
    class 2 in the high band, with small random jitter. This data is
    fictional and exists only to exercise the training loop.
    """
    rng = random.Random(seed)
    centers = [
        [0.8, 0.15, 0.05],
        [0.15, 0.7, 0.15],
        [0.05, 0.15, 0.8],
    ]
    features: list[list[float]] = []
    labels: list[int] = []
    for label, center in enumerate(centers):
        for _ in range(n_per_class):
            row = [max(0.01, c + rng.uniform(-0.1, 0.1)) for c in center]
            total = sum(row)
            features.append([v / total for v in row])
            labels.append(label)
    return features, labels
