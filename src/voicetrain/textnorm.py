"""Vietnamese transcript normalization for speech training data.

Transcripts in a training set must be consistent, or the model learns
spelling noise instead of speech. This module lowercases text, fixes
punctuation spacing, keeps Vietnamese diacritics intact, and spells out
numbers from 0 to 9999 in words, following standard Vietnamese reading
rules (including "mốt", "lăm", "lẻ", and "không trăm").
"""

from __future__ import annotations

import re

_ONES = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]


def _unit_word(unit: int, tens: int) -> str:
    """The word for a units digit, with the "mốt"/"lăm" special cases."""
    if tens >= 2 and unit == 1:
        return "mốt"
    if tens >= 1 and unit == 5:
        return "lăm"
    return _ONES[unit]


def number_to_words(number: int) -> str:
    """Spell out an integer from 0 to 9999 in Vietnamese words."""
    if not 0 <= number <= 9999:
        raise ValueError("number_to_words supports 0 to 9999 only")
    if number == 0:
        return "không"

    thousands, rest = divmod(number, 1000)
    hundreds, tens_units = divmod(rest, 100)
    tens, units = divmod(tens_units, 10)

    parts: list[str] = []
    if thousands:
        parts.append(f"{_ONES[thousands]} nghìn")
    if hundreds:
        parts.append(f"{_ONES[hundreds]} trăm")
    elif thousands and tens_units:
        parts.append("không trăm")

    if tens == 0:
        if units:
            if hundreds or thousands:
                parts.append(f"lẻ {_ONES[units]}")
            else:
                parts.append(_ONES[units])
    elif tens == 1:
        text = "mười"
        if units:
            text += f" {_unit_word(units, tens)}"
        parts.append(text)
    else:
        text = f"{_ONES[tens]} mươi"
        if units:
            text += f" {_unit_word(units, tens)}"
        parts.append(text)
    return " ".join(parts)


_DIGITS = re.compile(r"\d+")
_SPACE_BEFORE_PUNCT = re.compile(r"\s+([,.?!:;])")
_SPACE_AFTER_PUNCT = re.compile(r"([,.?!:;])(?=\S)")
_WHITESPACE = re.compile(r"\s+")


def _spell_digits(match: re.Match[str]) -> str:
    value = int(match.group(0))
    if value > 9999:
        return match.group(0)
    return number_to_words(value)


def normalize(text: str) -> str:
    """Normalize a transcript: lowercase, spell out numbers, fix spacing.

    Diacritics are never stripped: "đào" stays "đào", because stripping
    them would destroy Vietnamese meaning.
    """
    text = text.lower()
    text = _DIGITS.sub(_spell_digits, text)
    text = _SPACE_BEFORE_PUNCT.sub(r"\1", text)
    text = _SPACE_AFTER_PUNCT.sub(r"\1 ", text)
    return _WHITESPACE.sub(" ", text).strip()
