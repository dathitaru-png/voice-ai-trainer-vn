"""Word error rate (WER) and character error rate (CER) evaluation.

WER is the standard speech-recognition metric: the word-level edit
distance (substitutions + deletions + insertions) divided by the number
of words in the reference. CER is the same idea at character level, with
spaces removed so spacing choices do not dominate the score.
"""

from __future__ import annotations


def _levenshtein(a: list[str], b: list[str]) -> int:
    """Edit distance between two token sequences."""
    prev = list(range(len(b) + 1))
    for i, token_a in enumerate(a, start=1):
        cur = [i]
        for j, token_b in enumerate(b, start=1):
            cost = 0 if token_a == token_b else 1
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost))
        prev = cur
    return prev[-1]


def wer(reference: str, hypothesis: str) -> float:
    """Word error rate of a hypothesis against a reference transcript."""
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    if not ref_words:
        return 0.0 if not hyp_words else 1.0
    return _levenshtein(ref_words, hyp_words) / len(ref_words)


def cer(reference: str, hypothesis: str) -> float:
    """Character error rate, computed with spaces removed."""
    ref_chars = list(reference.replace(" ", ""))
    hyp_chars = list(hypothesis.replace(" ", ""))
    if not ref_chars:
        return 0.0 if not hyp_chars else 1.0
    return _levenshtein(ref_chars, hyp_chars) / len(ref_chars)


def per_utterance_report(pairs: list[tuple[str, str]]) -> list[dict[str, object]]:
    """WER and CER for each (reference, hypothesis) pair."""
    report = []
    for reference, hypothesis in pairs:
        report.append(
            {
                "reference": reference,
                "hypothesis": hypothesis,
                "wer": wer(reference, hypothesis),
                "cer": cer(reference, hypothesis),
            }
        )
    return report
