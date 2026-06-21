# AGENTS.md — CrashTech 2026 Hackathon

This project is configured **Claude-canonical**. The source of truth for any agent is
**`CLAUDE.md`**. This file is a thin redirect so non-Claude agents find the same assets.

- **Instructions / project conventions:** `CLAUDE.md`, plus the instruction tree under
  `.claude/instructions/` (start with `.claude/instructions/hardware/README.md` for any RTL or
  wiring).
- **Skills:** `.claude/skills/` — domain BKM skills (`de10lite-board-and-build`,
  `de10lite-vga-graphics`, `de10lite-addon-peripherals`, `esp32-firmware`, `kicad-board-design`),
  the `challenge-intake` router, and discipline skills (`systematic-debugging`, `writing-plans`,
  `executing-plans`, `verification-before-completion`).
- **Hardware rules + host split (WSL vs Windows for programming/flashing):**
  `.claude/instructions/hardware/README.md`.
- **Reusable bricks (assemble, don't rewrite):** `projects/common/` — FPGA SystemVerilog modules
  + ESP32 C++ headers, all pre-built and testbenched. Catalog: `projects/common/README.md`.
  Starters: `challenges/starters/{uart_echo,clock,vga_game}`.
- **Build recipes:** `Justfile` (`just sim <name>` runs a brick testbench). **Toolchain quick-ref:**
  `SETUP_QUICKSTART.md`. **Status board:** `CHALLENGES.md`.

Budget note: token-frugal project. Prefer Copilot for bulk/boilerplate; keep Claude for hard
reasoning; no sub-agent fan-out. See the "Budget rules" section of `CLAUDE.md`.
