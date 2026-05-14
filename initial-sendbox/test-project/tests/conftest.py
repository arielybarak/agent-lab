"""Shared pytest fixtures for the fall-detection test suite."""

import sys
from pathlib import Path

import pytest
import torch

# Ensure `src/` is importable when running pytest from test-project/.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

SEED = 42


@pytest.fixture(autouse=True)
def seed_everything():
    """Set deterministic seeds before every test for reproducibility."""
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(SEED)
