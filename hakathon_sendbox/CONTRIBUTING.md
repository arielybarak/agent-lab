# Contributing to CrashTech 2026 Hackathon

## Setup

See the [README](README.md) for language-specific setup commands.

## Workflow

1. Create a branch off `main`.
2. Make focused changes — one logical concern per PR.
3. Run `just lint` and `just test` locally before pushing.
4. Update `CHANGELOG.md` under `## [Unreleased]` for user-facing changes.
5. Open a PR. Squash-merge after review.

## Coding conventions

See [.claude/instructions/coding-conventions.md](.claude/instructions/coding-conventions.md).

## Architecture

The project follows a DDD layering. See
[.claude/instructions/architecture.md](.claude/instructions/architecture.md) for
allowed dependencies between layers.

## AI agents

If you're an AI assistant (or working alongside one), start with
[CLAUDE.md](CLAUDE.md).
