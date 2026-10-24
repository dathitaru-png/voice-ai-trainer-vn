# Changelog

All notable changes follow [Keep a Changelog](https://keepachangelog.com/)
and semantic versioning.

## [Unreleased]

## [0.1.0] - 2026-10-24

### Added
- WAV handling with the stdlib `wave` module: metadata, duration, RMS,
  silence detection, and fixed-length frame chunking
- Dataset manifests (JSONL) with deterministic train/validation/test
  splits and duration filtering
- Vietnamese transcript normalization: lowercase, punctuation spacing,
  diacritic-safe handling, and digits-to-words for 0 to 9999
- Frame features: energy, zero-crossing rate, and a pure-Python DFT
  magnitude spectrum with band-energy summaries
- From-scratch softmax training loop demo on synthetic tone classes
- WER and CER evaluation with per-utterance reports
- CLI: `voicetrain validate`, `normalize`, `wer`, and `demo`
- Six Vietnamese guides covering the full training pipeline
- Test suite, CI workflow, and maintainer documentation
