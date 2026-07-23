"""Pytest discovery root for course-factory's deterministic tool layer.

Adds ../tools to sys.path so tests can `import instantiate`, `import progress`, etc. without
packaging the tools as an installed module (repo convention: stdlib + pytest only, no build step).
"""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))
