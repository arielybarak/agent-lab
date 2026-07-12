#!/usr/bin/env bash
# Resolve a spec-name argument (e.g. "000" or "001-pipeline-skeleton") to exactly one
# specs/<project>/<NNN-name>/ directory, and report whether it looks past /speckit-clarify.
#
# Custom helper for the speckit-harden skill's Step 0 — not part of upstream spec-kit's
# .specify/scripts/bash/ engine, so it lives beside the skill instead of in that directory.
# Purpose: make spec-resolution deterministic (a script, not hand-rolled grep/find each run)
# so the harden skill doesn't have to re-derive this logic — mirrors why setup-plan.sh /
# setup-tasks.sh exist instead of the plan/tasks skills hand-rolling their own path logic.
#
# Usage: resolve.sh <spec-name>
# Output (stdout, JSON): {"RESOLVED_FEATURE_DIR":"specs/proj/NNN-name","CLARIFIED":true,"MATCH_COUNT":1,"CANDIDATES":[...]}
#
# MATCH_COUNT != 1 is a normal, reportable outcome (ambiguous or no match), not a script
# failure — the caller must check MATCH_COUNT and stop to ask the user, rather than treating
# a non-1 count as an error to recover from. Exit code is non-zero only for a usage error
# (missing argument) or an unexpected environment problem (e.g. .specify/ not found).
#
# CLARIFIED is a best-effort signal (checks for a "## Clarifications" heading in spec.md).
# A `false` here is not conclusive — some specs record "Clarified" only in the project's
# README spec index. Callers should treat `false` as "double-check the README," not as a
# final verdict.

set -euo pipefail

SPEC_NAME="${1:-}"
if [[ -z "$SPEC_NAME" ]]; then
    echo "ERROR: usage: resolve.sh <spec-name>" >&2
    exit 1
fi

SCRIPT_DIR="$(CDPATH="" cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/../../../.specify/scripts/bash/common.sh"

REPO_ROOT=$(get_repo_root)

declare -a MATCHES=()
while IFS= read -r -d '' spec_file; do
    dir="$(dirname "$spec_file")"
    base="$(basename "$dir")"
    if [[ "$base" == "$SPEC_NAME" || "$base" == "$SPEC_NAME"-* ]]; then
        MATCHES+=("${dir#"$REPO_ROOT"/}")
    fi
done < <(find "$REPO_ROOT/specs" -mindepth 3 -maxdepth 3 -name spec.md -print0 2>/dev/null)

MATCH_COUNT=${#MATCHES[@]}
RESOLVED=""
CLARIFIED="false"

if [[ "$MATCH_COUNT" -eq 1 ]]; then
    RESOLVED="${MATCHES[0]}"
    if grep -q '^## Clarifications' "$REPO_ROOT/$RESOLVED/spec.md" 2>/dev/null; then
        CLARIFIED="true"
    fi
fi

if has_jq; then
    if [[ "$MATCH_COUNT" -eq 0 ]]; then
        candidates_json="[]"
    else
        candidates_json=$(printf '%s\n' "${MATCHES[@]}" | jq -R . | jq -s .)
    fi
    jq -cn \
        --arg resolved "$RESOLVED" \
        --argjson clarified "$CLARIFIED" \
        --argjson count "$MATCH_COUNT" \
        --argjson candidates "$candidates_json" \
        '{RESOLVED_FEATURE_DIR:$resolved, CLARIFIED:$clarified, MATCH_COUNT:$count, CANDIDATES:$candidates}'
else
    # No-jq fallback: build the CANDIDATES array by hand with json_escape (same pattern
    # setup-plan.sh/common.sh use elsewhere in this repo when jq is unavailable).
    candidates_json="["
    for i in "${!MATCHES[@]}"; do
        [[ "$i" -gt 0 ]] && candidates_json+=","
        candidates_json+="\"$(json_escape "${MATCHES[$i]}")\""
    done
    candidates_json+="]"
    printf '{"RESOLVED_FEATURE_DIR":"%s","CLARIFIED":%s,"MATCH_COUNT":%d,"CANDIDATES":%s}\n' \
        "$(json_escape "$RESOLVED")" "$CLARIFIED" "$MATCH_COUNT" "$candidates_json"
fi
