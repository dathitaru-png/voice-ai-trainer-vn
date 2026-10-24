# VoiceTrainer VN

**An offline, dependency-free Python toolkit for training voice AI: dataset preparation, acoustic features, a teaching training loop, and WER/CER evaluation.**

VoiceTrainer VN helps Vietnamese builders and students:

1. **Prepare** speech datasets: WAV validation, JSONL manifests, deterministic train/validation/test splits, and Vietnamese transcript normalization (including digits-to-words from 0 to 9999).
2. **Extract** frame-level acoustic features with the standard library only: frame energy, zero-crossing rate, and a small DFT-based band-energy summary.
3. **Learn** the training loop itself: a from-scratch softmax classifier trained by gradient descent on synthetic tone features, with per-epoch loss reporting.
4. **Evaluate** recognizers honestly: word error rate (WER) and character error rate (CER) with per-utterance reports.

> Tóm tắt tiếng Việt: Bộ công cụ Python mã nguồn mở, không phụ thuộc bên ngoài,
> hỗ trợ toàn bộ pipeline đào tạo voice AI: chuẩn bị dữ liệu (WAV, manifest,
> chuẩn hoá bản ghi tiếng Việt), trích xuất đặc trưng âm thanh, vòng lặp huấn
> luyện minh hoạ, và đánh giá bằng WER/CER. Chạy offline hoàn toàn, không cần
> API key.

## Scope, stated honestly

VoiceTrainer VN is a **pipeline toolkit, not a pretrained speech model**.
It does not ship a recognizer, does not claim state-of-the-art accuracy,
and its training demo runs on synthetic tones precisely so the loop can be
verified without a real dataset. If you need a production recognizer, use
this toolkit to prepare and evaluate data, then train a real model with a
framework of your choice.

## Status

Brand-new project, v0.1.0, launched October 2026. No usage metrics are
claimed: no users, downloads, or stars are reported anywhere in this
repository, because none exist yet.

## Why this project exists

Voice AI tutorials usually jump straight to a big framework and a
pretrained model, hiding the pipeline that matters most: clean data,
consistent transcripts, meaningful features, and honest evaluation. For
Vietnamese builders, the gap is wider — transcript rules, diacritics, and
digits-to-words are rarely handled well. VoiceTrainer VN fills that gap
with a small, readable, fully tested core that anyone can audit and run
anywhere, using only the Python standard library.

## Quick start

```bash
pip install -e .
python examples/build_synthetic_dataset.py   # tiny synthetic WAV dataset
voicetrain validate synthetic_dataset/manifest.jsonl
voicetrain normalize "Tôi có 2 con mèo."
voicetrain wer "xin chào mọi người" "xin chào mọi"
voicetrain demo                              # synthetic training run
```

```python
from voicetrain import normalize, wer, read_wav, frame_energy

print(normalize("Tôi có 2 con mèo."))  # tôi có hai con mèo.
print(wer("xin chào mọi người", "xin chào mọi"))  # 0.25
```

## Guides

Vietnamese guides live in `guides/`:

1. Pipeline đào tạo voice AI — tổng quan
2. Thu thập và chuẩn hoá dữ liệu
3. Đặc trưng âm thanh
4. Vòng lặp huấn luyện
5. Đánh giá bằng WER/CER
6. Checklist trước khi train thật

## Development

```bash
pip install -e . pytest
python -m pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup and pull-request steps,
[SECURITY.md](SECURITY.md) for private vulnerability reporting, and
[ROADMAP.md](ROADMAP.md) for what comes next.

## License

MIT. See [LICENSE](LICENSE).
