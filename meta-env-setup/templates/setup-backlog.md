# Setup Backlog — <repo>

> The **brownfield** counterpart to `setup-spec.md`: a priority-ordered list of changes an
> *existing* `.claude/` setup needs, grounded in where time was actually burned. Authored by an
> agent (or human) after real use, then consumed by **`/upgrade-claude-setup`**, which imports
> the live setup into `claude-setups/<repo>/`, reconciles it against this backlog, and works the
> items down. Lives in the target repo as `.claude/setup-backlog.md`.
>
> Write for a builder agent with **no chat context**: every item must be implementable cold —
> name the block, the observed cost, the exact behavior/args/entry points, and the done-check.
> Cite real files, commands, and line anchors throughout; an ungrounded item gets cut.

- **Repo:** <path / name>   **Date:** <YYYY-MM-DD>   **Author context:** <what work surfaced these>

## 1. Where time was burned (grounding — keep short)
> 2–5 bullets naming the themes of pain that justify the backlog. This is the credibility
> behind every ask below — not narrative.

- …

## 2. The backlog (priority order)
> One entry per change, highest-leverage first. **Tag** = ADD | FIX | REWRITE | KEEP | CUT.
> ADD = new block · FIX = existing block falls short · REWRITE = existing block is now *wrong*
> (see §3) · KEEP = pulls its weight, don't touch · CUT = remove/merge (see §4).

### [TAG] <block name> — <one-line value> · <value/effort>
- **Target:** which skill / command / agent / hook (or `new <type>`), with its path.
- **Why:** the observed cost this addresses — what you did by hand, how often (grounded).
- **What to build/change (cold-implementable):** behavior, args/flags, entry points, file:line.
- **Done when:** the concrete check that proves it works.

*(repeat per item)*

## 3. Stale — existing blocks now WRONG (high-priority REWRITEs)
> Blocks whose content is actively misleading because the code/world changed under them. These
> can't wait — a wrong skill is worse than a missing one. Each: which block, why it's wrong now,
> what it must say instead.

| Block (path) | Why it's now wrong | What it must say instead |
|---|---|---|
| … | … | … |

## 4. Keep / unchanged
> Blocks that already earn their place. Naming them prevents needless churn (and stops the
> refine loop from "fixing" what works).

- `…` — why it stays as-is.

## 5. Cut
> Blocks to remove or merge, with the reason. (Prove a cut with `--ablate --execute` when it's
> worth the compute.)

- `…` — why / merge into `…`.

## 6. Durable knowledge (skill / memory candidates)
> Facts learned this round that deserve capture as a *new* skill or a memory, distinct from the
> block changes above.

- …

## 7. Appendix — exact facts for a cold builder
> Constants, endpoints, entry-point function signatures, file/line anchors — everything a fresh
> agent needs to implement §2 without re-deriving it. The single most valuable section.

- …

## 8. Effectiveness targets (the exit condition for /upgrade-claude-setup → /refine-setup)
- `validate` clean · composite **≥ 85** · 0 `[CUT?]` · routing **100%**.
- **Every §2 item is resolved** (done-check met) and every §3 stale block is rewritten.
- (Optional) `--ablate --execute`: no block flagged `CUT`.
