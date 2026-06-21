#!/usr/bin/env python3
"""Unit tests for the deterministic parts of the effectiveness audit.

Covers Layer 1 (static scorers), Layer 2 (the nearest-description router), and
Layer 3's verdict logic — the last with a *mocked* agent runner, so the whole
ablation pipeline (sandbox build, leave-one-out removal, assertion checks,
KEEP/CUT verdict) is exercised without launching a single ``claude`` process.

Run:  python tools/test_audit.py          (or: python -m unittest -v tools/test_audit.py)
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # make the tools/ modules importable
import validate_claude_setup as vcs  # noqa: E402
import _ablation  # noqa: E402


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _make_setup(tmp: Path) -> Path:
    """A minimal but realistic setup: CLAUDE.md + two skills."""
    _write(tmp / "CLAUDE.md",
           "# Demo\nBest result: F2 = 0.9552 on 241 clips. Optimize for recall.\n"
           "Audio is 16 kHz mono. Deploy to the ESP32-S3.\n")
    _write(tmp / ".claude" / "skills" / "audio-prep" / "SKILL.md",
           "---\nname: audio-prep\ndescription: >-\n"
           "  Canonical 16 kHz mono log-Mel spectrogram preprocessing with librosa.\n"
           "  USE WHEN writing preprocessing or feature extraction.\n---\n\nBody.\n")
    _write(tmp / ".claude" / "skills" / "edge-deploy" / "SKILL.md",
           "---\nname: edge-deploy\ndescription: >-\n"
           "  ESP32-S3 quantize/prune/export with TFLite-Micro and PSRAM budgeting.\n"
           "  USE WHEN exporting a model or checking on-device fit.\n---\n\n"
           "We beat F2 = 0.9552 on 241 clips, so it ships.\n")  # deliberate brief echo
    return tmp


# --------------------------------------------------------------------------- #
# Layer 1 — primitives
# --------------------------------------------------------------------------- #
class TestPrimitives(unittest.TestCase):
    def test_jaccard(self):
        self.assertAlmostEqual(vcs._jaccard({"a", "b"}, {"b", "c"}), 1 / 3)
        self.assertEqual(vcs._jaccard(set(), {"a"}), 0.0)

    def test_estimate_tokens(self):
        self.assertEqual(vcs._estimate_tokens("abcd"), 1)
        self.assertGreater(vcs._estimate_tokens("x" * 40), 9)

    def test_distinctive_only_real_figures(self):
        for good in ("0.9552", "99.2", "5.6", "241"):
            self.assertTrue(vcs._distinctive(good), good)
        for noise in ("1.", "2.", "16", "96", "3", "notebook-to-src", "esp32"):
            self.assertFalse(vcs._distinctive(noise), noise)

    def test_trigger_score(self):
        self.assertEqual(vcs._trigger_score("USE WHEN exporting a model to the ESP32-S3 device"), 1.0)
        self.assertLess(vcs._trigger_score("a helper"), 1.0)

    def test_stem_is_router_only(self):
        self.assertEqual(vcs._stem("exporting"), "export")
        self.assertEqual(vcs._stem("models"), "model")
        self.assertEqual(vcs._stem("is"), "is")  # too short to strip


# --------------------------------------------------------------------------- #
# Layer 1 — audit() on a real (temp) setup
# --------------------------------------------------------------------------- #
class TestAudit(unittest.TestCase):
    def test_flags_brief_echo_and_scores(self):
        with tempfile.TemporaryDirectory() as d:
            root = _make_setup(Path(d))
            a = vcs.audit(root)
            self.assertFalse(a.skipped)
            self.assertEqual(a.error, "")
            self.assertGreater(a.budget_tokens, 0)
            self.assertTrue(0 <= a.score <= 100)
            # the edge-deploy skill copies CLAUDE.md figures -> must be flagged
            echoed = " ".join(p for p, _ in a.sharpen)
            self.assertIn("edge-deploy", echoed)
            # audio-prep does NOT echo figures -> must not be flagged for echo
            self.assertNotIn("audio-prep", echoed)

    def test_file_path_is_skipped(self):
        # A glob that also matches a file (e.g. README.md) must be skipped, not fail.
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "README.md"
            f.write_text("not a setup", encoding="utf-8")
            a = vcs.audit(f)
            self.assertTrue(a.skipped)

    def test_empty_dir_is_valid_but_zero_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            a = vcs.audit(Path(d))  # treated as an empty .claude/ (same as validate())
            self.assertEqual(a.error, "")
            self.assertEqual(a.budget_breakdown.get("n_blocks"), 0)


# --------------------------------------------------------------------------- #
# Layer 2 — nearest-description router
# --------------------------------------------------------------------------- #
class TestRouting(unittest.TestCase):
    def setUp(self):
        self.skills = [
            vcs.Block("skill", "audio-prep", "16 kHz mono log-Mel spectrograms librosa preprocessing"),
            vcs.Block("skill", "edge-deploy", "ESP32-S3 quantize export tflite psram flash on-device"),
        ]

    def test_routes_to_right_skill(self):
        self.assertEqual(
            vcs._predict_skill("resample to 16 kHz and build log-Mel spectrograms", self.skills),
            "audio-prep")
        self.assertEqual(
            vcs._predict_skill("export and quantize the model for the ESP32-S3", self.skills),
            "edge-deploy")

    def test_unrelated_prompt_routes_nowhere(self):
        self.assertIsNone(vcs._predict_skill("schedule a meeting tomorrow", self.skills))


# --------------------------------------------------------------------------- #
# Layer 3 — ablation verdict logic, with a MOCKED agent runner
# --------------------------------------------------------------------------- #
class TestAblationVerdict(unittest.TestCase):
    def test_keep_load_bearing_block_cut_the_decoy(self):
        with tempfile.TemporaryDirectory() as d:
            root = _make_setup(Path(d))
            claude, claude_md = _ablation._setup_paths(root)
            blocks = _ablation._enumerate_blocks(claude)
            conditions = _ablation._conditions(blocks)
            tasks = [{
                "id": "needs-audio-prep",
                "prompt": "how do I preprocess?",
                "assertions": [{"type": "output_contains", "value": "magic"}],
            }]

            # Fake agent: only "succeeds" (says the magic word) when audio-prep is
            # present in the sandbox it was handed. So removing audio-prep should
            # drop the pass-rate (KEEP); removing edge-deploy should not (CUT).
            def fake_run(prompt, workdir):
                if (Path(workdir) / ".claude" / "skills" / "audio-prep" / "SKILL.md").exists():
                    return "the magic answer"
                return "no idea"

            orig = _ablation._run_claude
            _ablation._run_claude = fake_run
            try:
                results = _ablation._execute(conditions, tasks, claude, claude_md, repeats=1)
                _, cut = _ablation._verdict(results, blocks, root, tasks, 1)
            finally:
                _ablation._run_claude = orig

            self.assertEqual(results["full"]["needs-audio-prep"], 1.0)
            self.assertEqual(results["no-setup"]["needs-audio-prep"], 0.0)
            self.assertEqual(results["skill:audio-prep"]["needs-audio-prep"], 0.0)
            self.assertEqual(results["skill:edge-deploy"]["needs-audio-prep"], 1.0)
            self.assertIn("skill:edge-deploy", cut)          # dead weight for this task
            self.assertNotIn("skill:audio-prep", cut)        # load-bearing


if __name__ == "__main__":
    unittest.main(verbosity=2)
