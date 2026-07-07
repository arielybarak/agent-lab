# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `.claude/instructions/hardware/debug-lessons.md` — live-session hardware debug lessons + 7-step
  dead-UART protocol (extracted from a teammate's fork). Wired into the hardware README,
  `challenge-intake`, and `CLAUDE.md`.
- `docs/manual/DE10-Lite_User_Manual.pdf` — official board manual as offline fallback (gitignored,
  local-only).

### Changed
- All ESP32 `platformio.ini` (template, starters, demos) now set `monitor_rts = 0` /
  `monitor_dtr = 0` so closing the serial monitor no longer resets the ESP32.
