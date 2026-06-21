# CrashTech 2026 Hackathon — AI-Assisted Hardware Engineering: Case Study

## The setup

A Claude Code workspace purpose-built for a **24-hour hardware hackathon**: DE10-Lite FPGA
(SystemVerilog / Quartus) + ESP32 (C++ / PlatformIO) communicating over UART, with some
challenges adding KiCad PCB design. The constraint that shaped everything: **tight token budget
(Claude Pro)**, so the AI setup had to be deliberately economical.

## Key design decisions

**Division of labor between two AI tools:**
GitHub Copilot handled bulk/boilerplate generation (rote edits, scaffolding). Claude was reserved
for hard reasoning — tricky RTL timing, debugging integration failures, cross-domain decisions.
This is a deliberate least-cost architecture: don't burn expensive tokens on things a cheaper
tool handles fine.

**Pre-built brick library instead of generation:**
`projects/common/` holds a fully tested, testbenched library of SystemVerilog modules and ESP32
C++ headers (UART, display, VGA, ADC, servos, etc.) built *before* the hackathon. The AI's job
during the event is to *assemble* bricks, not generate from scratch. This was the single biggest
time-saver — and it mirrors a real engineering principle: generate once, reuse many times.

**Domain skills as token-efficient context injection:**
Five large BKM (Best Known Method) skills encode hard-won domain knowledge:
`de10lite-board-and-build`, `de10lite-vga-graphics`, `de10lite-addon-peripherals`,
`esp32-firmware`, `kicad-board-design`. Each is loaded only when needed (not pre-loaded) — a
context budget decision that saves thousands of tokens per session.

**`challenge-intake` as a router:**
A single entry-point skill routes the user's challenge description to the right BKM skill and
scaffolds the folder structure. This prevents the model from having to reason about *which* skill
applies under time pressure.

## What worked

- Brick-first development: challenges that used existing bricks were solved 3-5× faster than
  challenges that required new modules
- Skill routing via `challenge-intake` removed decision overhead at the worst possible time (24h clock running)
- Separating Claude/Copilot budgets forced explicit reasoning about *what kind of AI help* was needed

## What was hard / broke

- **WSL/Windows toolchain split:** Quartus programs run on Windows, builds run in WSL. The AI
  occasionally gave commands that only work on one side. Now documented in
  `.claude/instructions/hardware/README.md`.
- **UART bring-up failures:** A recurring failure class (boot-loop strap, silkscreen TXD/RXD swap,
  stale .sof files). Required a dedicated `debug-lessons.md` checklist to avoid re-deriving the
  same 7-step debug protocol every session.
- **Context drift across sessions:** Hardware state (what's flashed, what's wired) doesn't persist
  in the model. `CHALLENGES.md` status board was the workaround — explicit, human-maintained state.

## What this demonstrates (portfolio angle)

- **AI-assisted engineering under real constraints** (time, budget, hardware in the loop)
- **Context budget design** as a first-class concern — not just "use AI," but *how much* and *when*
- **Skill/tool architecture for a domain** rather than general-purpose prompting
- **Honest failure documentation** — what broke, why, and what the structural fix was
