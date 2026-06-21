# Mini ML Project — Audio-Based Fall Detection

A deliberately tiny project to test the Copilot agent pipeline.

## What it does

Binary classifier that distinguishes **fall** vs. **non-fall** events from
synthetic mel-spectrogram features using a small 1D CNN.

## Structure

```
test-project/
├── src/
│   ├── dataset.py    # Synthetic audio dataset (torch Dataset)
│   ├── model.py      # 1D CNN classifier
│   ├── train.py      # Training loop
│   └── evaluate.py   # Metrics (accuracy, precision, recall, F1)
└── tests/
    ├── test_dataset.py
    └── test_model.py
```

## Quick start

```bash
# Install deps
pip install torch pytest

# Run tests
pytest tests/

# Train on synthetic data
python src/train.py
```

## Design decisions

- **Synthetic data only** — no external datasets, fully self-contained.
- **1D CNN on mel-spectrograms** — a standard lightweight approach for
  short audio classification tasks.
- **No frameworks beyond PyTorch** — explicit training loop, no Lightning.
