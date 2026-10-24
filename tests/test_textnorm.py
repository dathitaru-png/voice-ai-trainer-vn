"""Tests for Vietnamese transcript normalization and digits-to-words."""

import pytest

from voicetrain.textnorm import normalize, number_to_words


@pytest.mark.parametrize(
    "number,expected",
    [
        (0, "không"),
        (5, "năm"),
        (10, "mười"),
        (11, "mười một"),
        (15, "mười lăm"),
        (20, "hai mươi"),
        (21, "hai mươi mốt"),
        (25, "hai mươi lăm"),
        (101, "một trăm lẻ một"),
        (105, "một trăm lẻ năm"),
        (110, "một trăm mười"),
        (115, "một trăm mười lăm"),
        (1000, "một nghìn"),
        (1001, "một nghìn không trăm lẻ một"),
        (1010, "một nghìn không trăm mười"),
        (2024, "hai nghìn không trăm hai mươi bốn"),
        (9999, "chín nghìn chín trăm chín mươi chín"),
    ],
)
def test_number_to_words(number, expected):
    assert number_to_words(number) == expected


def test_number_to_words_rejects_out_of_range():
    with pytest.raises(ValueError):
        number_to_words(10000)
    with pytest.raises(ValueError):
        number_to_words(-1)


def test_normalize_digits_punctuation_and_case():
    assert normalize("Tôi có 2 con mèo, 15 con chó!") == "tôi có hai con mèo, mười lăm con chó!"
    assert normalize("Hôm nay là ngày 21 tháng 5 .") == "hôm nay là ngày hai mươi mốt tháng năm."


def test_normalize_keeps_diacritics():
    text = normalize("ĐÀO TẠO GIỌNG NÓI TIẾNG VIỆT")
    assert text == "đào tạo giọng nói tiếng việt"


def test_normalize_keeps_large_numbers_as_digits():
    assert normalize("mã số 12345") == "mã số 12345"
