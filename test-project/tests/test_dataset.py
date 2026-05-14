"""Tests for the synthetic fall-detection dataset.

These tests define the expected contract for ``FallDetectionDataset``
*before* the implementation exists (TDD Red Phase).
"""

import torch
from torch.utils.data import DataLoader

from dataset import FallDetectionDataset


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

class TestDatasetConstruction:
    """Verify the dataset can be instantiated with expected defaults."""

    def test_default_length(self):
        """Dataset should contain 200 samples by default."""
        ds = FallDetectionDataset()
        assert len(ds) == 200

    def test_custom_length(self):
        """Caller should be able to request a specific number of samples."""
        ds = FallDetectionDataset(num_samples=64)
        assert len(ds) == 64

    def test_default_num_mels(self):
        """Each spectrogram should have 64 mel bins by default."""
        ds = FallDetectionDataset()
        spectrogram, _ = ds[0]
        # spectrogram: (num_mels, time_steps)
        assert spectrogram.shape[0] == 64

    def test_custom_num_mels(self):
        ds = FallDetectionDataset(num_mels=128)
        spectrogram, _ = ds[0]
        assert spectrogram.shape[0] == 128

    def test_default_time_steps(self):
        """Default time dimension should be 32 frames."""
        ds = FallDetectionDataset()
        spectrogram, _ = ds[0]
        # spectrogram: (num_mels, time_steps)
        assert spectrogram.shape[1] == 32


# ---------------------------------------------------------------------------
# Data types and label range
# ---------------------------------------------------------------------------

class TestDatasetOutput:
    """Verify tensor types and label values returned by __getitem__."""

    def test_spectrogram_is_float_tensor(self):
        ds = FallDetectionDataset()
        spectrogram, _ = ds[0]
        assert isinstance(spectrogram, torch.Tensor)
        assert spectrogram.dtype == torch.float32

    def test_label_is_long_tensor(self):
        """Labels should be integer tensors (0 or 1) for CrossEntropyLoss."""
        ds = FallDetectionDataset()
        _, label = ds[0]
        assert isinstance(label, torch.Tensor)
        assert label.dtype == torch.long

    def test_labels_are_binary(self):
        """All labels should be either 0 (non-fall) or 1 (fall)."""
        ds = FallDetectionDataset(num_samples=100)
        labels = torch.tensor([ds[i][1] for i in range(len(ds))])
        assert labels.min() >= 0
        assert labels.max() <= 1

    def test_both_classes_present(self):
        """Dataset should contain at least one sample of each class."""
        ds = FallDetectionDataset(num_samples=100)
        labels = torch.tensor([ds[i][1] for i in range(len(ds))])
        assert (labels == 0).any(), "No non-fall samples found"
        assert (labels == 1).any(), "No fall samples found"


# ---------------------------------------------------------------------------
# DataLoader compatibility
# ---------------------------------------------------------------------------

class TestDataLoaderIntegration:
    """Ensure the dataset works with torch DataLoader (batching, shuffling)."""

    def test_dataloader_batch_shape(self):
        ds = FallDetectionDataset(num_samples=32, num_mels=64, time_steps=32)
        loader = DataLoader(ds, batch_size=8, shuffle=False)
        batch_x, batch_y = next(iter(loader))
        # batch_x: (batch_size, num_mels, time_steps)
        assert batch_x.shape == (8, 64, 32)
        # batch_y: (batch_size,)
        assert batch_y.shape == (8,)
