"""Tests for the 1D CNN fall-detection model.

These tests define the expected contract for ``FallDetectionCNN``
*before* the implementation exists (TDD Red Phase).
"""

import torch

from model import FallDetectionCNN


# ---------------------------------------------------------------------------
# Construction and architecture
# ---------------------------------------------------------------------------

class TestModelConstruction:
    """Verify the model can be instantiated with expected defaults."""

    def test_default_instantiation(self):
        """Model should be creatable with zero arguments (sane defaults)."""
        model = FallDetectionCNN()
        assert model is not None

    def test_custom_input_channels(self):
        """Model should accept a configurable number of mel bins."""
        model = FallDetectionCNN(in_channels=128)
        assert model is not None

    def test_num_classes_default(self):
        """Default output should be 2 classes (fall / non-fall)."""
        model = FallDetectionCNN()
        dummy = torch.randn(1, 64, 32)  # (batch, mels, time)
        out = model(dummy)
        # out: (batch_size, num_classes)
        assert out.shape[-1] == 2


# ---------------------------------------------------------------------------
# Forward pass shapes
# ---------------------------------------------------------------------------

class TestModelForward:
    """Verify the forward pass produces correct output shapes."""

    def test_single_sample(self):
        model = FallDetectionCNN(in_channels=64)
        # x: (batch_size=1, num_mels=64, time_steps=32)
        x = torch.randn(1, 64, 32)
        out = model(x)
        # out: (1, num_classes=2)
        assert out.shape == (1, 2)

    def test_batch(self):
        model = FallDetectionCNN(in_channels=64)
        # x: (batch_size=16, num_mels=64, time_steps=32)
        x = torch.randn(16, 64, 32)
        out = model(x)
        # out: (16, 2)
        assert out.shape == (16, 2)

    def test_output_is_logits(self):
        """Output should be raw logits (not probabilities). Verify they are
        not constrained to [0,1] — CrossEntropyLoss expects raw logits."""
        model = FallDetectionCNN(in_channels=64)
        x = torch.randn(4, 64, 32)
        out = model(x)
        # At least some logits should be negative if they are raw
        # (probabilistic that a randomly-initialised net has all-positive is ~0)
        assert out.min() < 0.0 or out.max() > 1.0, (
            "Outputs look like probabilities, not logits"
        )


# ---------------------------------------------------------------------------
# Device placement
# ---------------------------------------------------------------------------

class TestModelDevice:
    """Ensure model respects explicit device placement."""

    def test_model_parameters_on_cpu(self):
        model = FallDetectionCNN()
        for param in model.parameters():
            assert param.device.type == "cpu"

    def test_forward_on_cpu(self):
        model = FallDetectionCNN(in_channels=64)
        x = torch.randn(2, 64, 32)
        out = model(x)
        assert out.device.type == "cpu"
