---
name: maintain-agents-md
description: Create, audit, promote, and maintain repo-local and nested AGENTS.md guidance files for coding-agent workflows. Use when Codex needs to derive folder-scoped agent instructions from repo evidence, draft AGENTS.md files for review, promote approved drafts to live local AGENTS.md files, check for stale or duplicated guidance, or keep local agent instructions short, scoped, and current.
---

# Maintain AGENTS.md

Use this skill to build and maintain a repository documentation harness for coding agents. Treat `AGENTS.md` files as maps: short, scoped instructions that point to authoritative docs, tests, contracts, runbooks, and code.

## Workflow

1. Inspect the repo boundary.
   - Read the root `AGENTS.md`, any existing nested `AGENTS.md`, `.gitignore`, docs index files, test layout, and major source directories.
   - Use the repo's preferred code-search tool first when one is specified; otherwise use `rg`/`find`.

2. Draft before promotion unless the user already approved installation.
   - Put proposals in a WIP/review folder when available, for example `documentation/wip/agents-wip/`.
   - Keep draft filenames mapped to target paths, for example `frontend-AGENTS.draft.md` -> `frontend/AGENTS.md`.
   - Do not edit live `AGENTS.md` files until the user approves promotion.

3. Derive rules from evidence.
   - Prefer current code, tests, contracts, runbooks, checkpoints, and active docs over stale plans.
   - When evidence conflicts, surface the conflict instead of silently choosing one source.
   - Add only rules that change agent behavior in that folder.

4. Keep the corpus small.
   - Add this living-doc rule to promoted files: `Living doc: every pass MUST review/tweak this file as guidance emerges/expires.`
   - Add this style guard: `Style guard: keep this file short, scoped, and deduplicated; revise or replace stale/overlapping bullets instead of appending more.`
   - Replace or compress overlapping bullets instead of appending variants.

5. Choose scopes conservatively.
   - Start with broad scopes such as `documentation/`, `lib/`, `frontend/`, `test/`, `config/`, migrations, and task folders.
   - Add nested scopes only where a subfolder has distinct rules, risks, commands, or source-of-truth requirements.
   - For grouped scopes, either create identical files in each real directory or keep the group as a draft until promotion is approved.

6. Promote carefully.
   - Copy approved draft content into real `AGENTS.md` files only under existing directories.
   - Canonicalize installed files so they no longer say `Draft`, `Proposed`, or `proposed nested scope`.
   - Check whether `.gitignore` ignores `AGENTS.md`; ask whether ignored files are intended local-only guidance or a commit-readiness defect.
   - Decide what happens to WIP drafts after promotion: retain as provenance, mark promoted, move to archive, or delete only if the user explicitly asks.

7. Validate.
   - Run the audit helper when useful:
     ```bash
     python3 /path/to/maintain-agents-md/scripts/audit_agents_md.py /abs/path/to/repo
     ```
   - Use `--allow-ignored` when ignored `AGENTS.md` files are an accepted local-only policy.
   - Also run repo-local checks such as whitespace scans, line counts, and file inventory. Refresh indexes only when edits are in scope.

## Reference

Read `references/agent-doc-harness.md` when designing a new corpus, resolving scope disputes, promoting drafts, or auditing sprawl.

## Audit Helper

Use `scripts/audit_agents_md.py` for deterministic checks. It reports live files, stale draft wording, missing living/style guards, trailing whitespace, long files, and ignore rules that hide `AGENTS.md`.
