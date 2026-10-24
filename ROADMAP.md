# Roadmap

## 0.1.0 — released October 2026

- WAV handling, manifest building, deterministic splits, duration filters
- Vietnamese transcript normalization with digits-to-words (0 to 9999)
- Frame features: energy, zero-crossing rate, DFT band energies
- From-scratch softmax training demo on synthetic tones
- WER/CER evaluation and CLI (validate, normalize, wer, demo)
- Six Vietnamese guides and CI on Python 3.10 to 3.12

## Next

- MFCC-style features built on the existing DFT (still stdlib only)
- Data augmentation helpers: gain, noise, and speed perturbation on WAVs
- A small alignment visualizer for WER errors (substitution, deletion,
  insertion highlighting)
- More Vietnamese normalization rules: dates, times, and common
  abbreviations, with tests for each
- A real-data walkthrough guide using a public, permissively licensed
  Vietnamese speech corpus, without bundling the corpus itself

## Not planned

- A pretrained recognizer or model weights
- Network features, cloud uploads, or API integrations
- Non-stdlib dependencies in the core package
