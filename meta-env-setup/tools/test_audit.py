#!/usr/bin/env python3
"""Unit tests for the deterministic parts of the effectiveness audit.

Covers Layer 1 (static scorers), Layer 2 (the nearest-description router), and
Layer 3's verdict logic — the last with a *mocked* agent runner, so the whole
ablation pipeline (sandbox build, leave-one-out removal, assertion checks,
KEEP/CUT verdict) is exercised without launching a single ``claude`` process.

Run:  python tools/test_audit.py          (or: python -m unittest -v tools/test_audit.py)
"""

import json
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


# --------------------------------------------------------------------------- #
# scaffold_claude_setup import subcommand
# --------------------------------------------------------------------------- #
sys.path.insert(0, str(Path(__file__).resolve().parent))
import scaffold_claude_setup as scs  # noqa: E402


class TestScaffolderImport(unittest.TestCase):
    def test_import_copies_all_files_and_skips_existing(self):
        with tempfile.TemporaryDirectory() as src_d, tempfile.TemporaryDirectory() as dst_d:
            src = Path(src_d)
            dst = Path(dst_d) / "dest"
            # Build a minimal fake .claude/ in src
            (src / ".claude" / "skills" / "my-skill").mkdir(parents=True)
            (src / ".claude" / "skills" / "my-skill" / "SKILL.md").write_text("---\nname: my-skill\ndescription: test\n---\n")
            (src / ".claude" / "commands" / "my-cmd.md").parent.mkdir(parents=True)
            (src / ".claude" / "commands" / "my-cmd.md").write_text("---\ndescription: cmd\n---\n")
            (src / ".claude" / "settings.json").write_text("{}")
            (src / "CLAUDE.md").write_text("# Project\nHello.\n")
            # Also put a backlog doc in the .claude/ dir
            (src / ".claude" / "setup-backlog.md").write_text("# Backlog\n- item 1\n")

            args = scs.build_parser().parse_args(["import", str(src), "--dir", str(dst)])
            rc = scs.cmd_import(args)
            self.assertEqual(rc, 0)

            # Files copied
            self.assertTrue((dst / ".claude" / "skills" / "my-skill" / "SKILL.md").is_file())
            self.assertTrue((dst / ".claude" / "commands" / "my-cmd.md").is_file())
            self.assertTrue((dst / "CLAUDE.md").is_file())
            # Backlog discovered inside .claude/
            self.assertTrue((dst / ".claude" / "setup-backlog.md").is_file())

    def test_import_force_overwrites(self):
        with tempfile.TemporaryDirectory() as src_d, tempfile.TemporaryDirectory() as dst_d:
            src = Path(src_d)
            dst = Path(dst_d) / "dest"
            (src / ".claude" / "settings.json").parent.mkdir(parents=True)
            (src / ".claude" / "settings.json").write_text('{"v":1}')
            (src / "CLAUDE.md").write_text("# v1\n")

            # Import once
            scs.cmd_import(scs.build_parser().parse_args(["import", str(src), "--dir", str(dst)]))
            # Modify source
            (src / ".claude" / "settings.json").write_text('{"v":2}')
            (src / "CLAUDE.md").write_text("# v2\n")

            # Without --force: skips
            scs.cmd_import(scs.build_parser().parse_args(["import", str(src), "--dir", str(dst)]))
            self.assertIn('"v":1', (dst / ".claude" / "settings.json").read_text())

            # With --force: overwrites
            scs.cmd_import(scs.build_parser().parse_args(["import", str(src), "--dir", str(dst), "--force"]))
            self.assertIn('"v":2', (dst / ".claude" / "settings.json").read_text())

    def test_import_accepts_dotclaude_path_directly(self):
        with tempfile.TemporaryDirectory() as src_d, tempfile.TemporaryDirectory() as dst_d:
            src = Path(src_d)
            (src / ".claude" / "settings.json").parent.mkdir(parents=True)
            (src / ".claude" / "settings.json").write_text("{}")
            (src / "CLAUDE.md").write_text("# X\n")

            dst = Path(dst_d) / "dest"
            args = scs.build_parser().parse_args(["import", str(src / ".claude"), "--dir", str(dst)])
            rc = scs.cmd_import(args)
            self.assertEqual(rc, 0)
            self.assertTrue((dst / ".claude" / "settings.json").is_file())


# --------------------------------------------------------------------------- #
# Layer 1b — staleness check (--stale --repo)
# --------------------------------------------------------------------------- #
class TestStalePrimitives(unittest.TestCase):
    def test_identifier_nouns_keeps_code_ignores_prose(self):
        nouns = vcs._identifier_nouns(
            "Call render_mesh and _filled_glyphs_to_dxf; the STROKE_TAPER_DEG flag; "
            "MotionConfig lives in engine.py. This is plain English prose."
        )
        self.assertIn("render_mesh", nouns)
        self.assertIn("filled_glyphs_to_dxf", nouns)   # leading underscore stripped
        self.assertIn("STROKE_TAPER_DEG", nouns)
        self.assertIn("MotionConfig", nouns)
        self.assertIn("engine.py", nouns)
        # plain English words are NOT identifiers (they'd grep-hit anything)
        self.assertNotIn("plain", nouns)
        self.assertNotIn("English", nouns)

    def test_is_stale_thresholds(self):
        repo = {"alive_one", "alive_two"}
        # 2+ dead -> stale
        flag, dead = vcs._is_stale({"dead_a", "dead_b", "alive_one"}, repo)
        self.assertTrue(flag)
        self.assertEqual(dead, ["dead_a", "dead_b"])
        # 1 dead of 3 (33%) -> fresh
        flag, _ = vcs._is_stale({"dead_a", "alive_one", "alive_two"}, repo)
        self.assertFalse(flag)
        # 1 dead of 2 (50%) -> stale
        flag, _ = vcs._is_stale({"dead_a", "alive_one"}, repo)
        self.assertTrue(flag)


def _make_stale_fixture(tmp: Path) -> tuple[Path, Path]:
    """A fake repo + a setup whose blocks partly reference removed code."""
    repo = tmp / "repo"
    _write(repo / "engine.py",
           "def render_mesh(x):\n    FILLED_CONTOUR = 1\n    return _filled_glyphs_to_dxf(x)\n")
    setup = tmp / "setup"
    _write(setup / "CLAUDE.md", "# Demo\nMesh engine.\n")
    # fresh: every identifier it cites exists in engine.py
    _write(setup / ".claude" / "skills" / "fresh-skill" / "SKILL.md",
           "---\nname: fresh-skill\ndescription: >-\n  Mesh via render_mesh. USE WHEN rendering.\n---\n"
           "Use render_mesh in engine.py; the FILLED_CONTOUR flag matters.\n")
    # stale: cites removed functions/constants
    _write(setup / ".claude" / "skills" / "stale-skill" / "SKILL.md",
           "---\nname: stale-skill\ndescription: >-\n  Old path. USE WHEN skeletonizing.\n---\n"
           "Call skeletonize_image and BOOLEAN_UNION from old_module.py.\n")
    # pooled + stale: must still be scanned
    _write(setup / ".claude" / "tools-pool" / "skills" / "frontend" / "pooled-stale" / "SKILL.md",
           "---\nname: pooled-stale\ndescription: >-\n  Parked. USE WHEN tapering.\n---\n"
           "Uses taper_extrude with DRAFT_ANGLE_DEG.\n")
    return setup, repo


class TestStaleScan(unittest.TestCase):
    def test_flags_removed_code_keeps_fresh_and_scans_pool(self):
        with tempfile.TemporaryDirectory() as d:
            setup, repo = _make_stale_fixture(Path(d))
            findings, err = vcs.stale(setup, str(repo))
            self.assertEqual(err, "")
            by_name = {Path(f.path).parent.name: f for f in findings}
            self.assertEqual(by_name["fresh-skill"].verdict, "fresh")
            self.assertEqual(by_name["stale-skill"].verdict, "stale-suspect")
            # the pooled block is scanned and flagged, with pooled=True
            self.assertEqual(by_name["pooled-stale"].verdict, "stale-suspect")
            self.assertTrue(by_name["pooled-stale"].pooled)
            self.assertFalse(by_name["stale-skill"].pooled)

    def test_missing_repo_reports_error(self):
        with tempfile.TemporaryDirectory() as d:
            setup, _ = _make_stale_fixture(Path(d))
            findings, err = vcs.stale(setup, str(Path(d) / "does-not-exist"))
            self.assertEqual(findings, [])
            self.assertIn("not found", err)


# --------------------------------------------------------------------------- #
# transcript miner
# --------------------------------------------------------------------------- #
import mine_transcripts as mt  # noqa: E402


def _event(cmd: str) -> str:
    return json.dumps({
        "type": "assistant", "timestamp": "2026-06-10T22:40:13.939Z",
        "message": {"content": [{"type": "tool_use", "name": "Bash", "input": {"command": cmd}}]},
    })


class TestMinerPrimitives(unittest.TestCase):
    def test_slug_matches_claude_code_layout(self):
        self.assertEqual(mt.slug_for(Path("/home/barak/book_generator_tom")),
                         "-home-barak-book-generator-tom")

    def test_normalize_clusters_variants(self):
        a = mt.normalize_cmd('curl -s "https://a/logs" 2>/dev/null | python3 -c "x"')
        b = mt.normalize_cmd('curl -s "https://b/logs" 2>/dev/null | python3 -c "y"')
        self.assertEqual(a, b)  # different URLs/strings collapse to one template

    def test_redact_hides_secrets(self):
        red = mt._redact('curl -H "Authorization: Bearer hf_ABCDEFGH1234567890" https://x')
        self.assertNotIn("hf_ABCDEFGH1234567890", red)
        self.assertIn("<REDACTED>", red)

    def test_is_throwaway(self):
        self.assertTrue(mt.is_throwaway('python3 -c "import json"'))
        self.assertTrue(mt.is_throwaway("cat <<'EOF' > /tmp/x.py"))
        self.assertFalse(mt.is_throwaway("pytest tests/"))


class TestMinerScan(unittest.TestCase):
    def test_clusters_repeats_flags_deploy_and_redacts(self):
        with tempfile.TemporaryDirectory() as d:
            tdir = Path(d)
            # a secret-bearing log pull, repeated 3x (varied host) -> one cluster, printed
            lines = [
                _event(f'curl -H "Authorization: Bearer hf_TOPSECRET1234567" "https://api{n}/logs/run"')
                for n in "abc"
            ] + [
                _event('python3 -c "print(1)"'),   # throwaway
                _event("git push origin main"),     # deploy
            ]
            (tdir / "s.jsonl").write_text("\n".join(lines), encoding="utf-8")

            r = mt.mine(tdir, None)
            self.assertEqual(r["n_files"], 1)
            # the three curl variants collapse into one cluster of 3
            self.assertEqual(max(r["bash"].values()), 3)
            # the python -c one-liner is flagged throwaway
            self.assertGreaterEqual(sum(r["throwaway"].values()), 1)
            # git push counts as a deploy; the log pulls count as waits
            self.assertGreaterEqual(r["n_deploy"], 1)
            self.assertGreaterEqual(r["n_wait"], 3)

            report = mt.render_markdown(tdir, tdir, r, min_repeats=3)
            self.assertIn("<REDACTED>", report)          # redaction reaches the output
            self.assertNotIn("hf_TOPSECRET1234567", report)

    def test_missing_dir_is_empty_report_not_crash(self):
        with tempfile.TemporaryDirectory() as d:
            missing = Path(d) / "nope"
            r = mt.mine(missing, None)
            self.assertEqual(r["n_files"], 0)
            report = mt.render_markdown(missing, missing, r, min_repeats=3)
            self.assertIn("No transcripts found", report)


if __name__ == "__main__":
    unittest.main(verbosity=2)
