# Contributing to VoiceTrainer VN

Thanks for helping improve this toolkit. Contributions are welcome from
everyone, including first-time contributors.

## Setup

```bash
git clone https://github.com/dathitaru-png/voice-ai-trainer-vn
cd voice-ai-trainer-vn
python -m venv .venv
source .venv/bin/activate
pip install -e . pytest
python -m pytest
```

## Ground rules

- Keep the standard-library-only promise. New features must not add
  dependencies; if a feature needs one, discuss it in an issue first.
- Keep every example and test dataset fictional or synthetic. Never commit
  real recordings, real voices, or real transcripts.
- Add or update tests for every behavior change, and keep the suite green.
- Write plain, readable code with docstrings. This project is also a
  teaching resource, so clarity beats cleverness.

## Pull requests

1. Fork the repository and create a branch from `main`.
2. Make focused changes with tests.
3. Run `python -m pytest` and confirm the suite passes.
4. Open a pull request describing what changed and why.

## Reporting issues

Use the bug report template for defects and the feature request template
for ideas. Include a minimal reproduction for bugs: input, expected
output, and actual output.

## Code of conduct

Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Be kind and
constructive in issues, reviews, and discussions.
