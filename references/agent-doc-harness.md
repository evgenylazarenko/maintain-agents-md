# Agent Doc Harness Guide

## Principles

- `AGENTS.md` is a map, not an encyclopedia.
- Deep facts belong in linked code, docs, tests, contracts, runbooks, migrations, and operational evidence.
- Local instructions may narrow or add scope-specific rules, but they must not weaken root instructions or user constraints.
- Every local file is living guidance: update it when new rules emerge or old rules expire.
- The corpus should become shorter and clearer over time, not more repetitive.

## Evidence Pattern

Use current sources before stale intent:

1. Root and nested `AGENTS.md`
2. Current code, tests, migrations, runtime config, and operational evidence
3. Active contracts, ADRs, runbooks, RCAs, checkpoints, and maintained docs
4. Historical plans, archived docs, old tickets, and stale notes

When sources disagree, record whether the conflict looks like code drift, doc drift, stale operational state, or unresolved ambiguity.

## Scope Pattern

Prefer broad files first:

- `documentation/AGENTS.md`
- source root such as `lib/AGENTS.md`, `src/AGENTS.md`, or `app/AGENTS.md`
- `frontend/AGENTS.md`
- `test/AGENTS.md`
- config, migration, task, or operations folders

Add nested files only when the subfolder has distinct:

- source-of-truth rules
- safety or side-effect constraints
- verification commands
- state-machine or input-composition risks
- styling/visual or runtime requirements

## Draft And Promotion Pattern

Drafting:

- Use a WIP folder when the user asks to review first.
- Keep target mapping clear in draft names or a README.
- Validate that drafts are not accidentally live.

Promotion:

- Copy only approved drafts into real existing folders.
- Remove draft-only wording from installed files.
- Duplicate grouped-scope content into each real directory only when the user approves that shape.
- Check `.gitignore` for `AGENTS.md`. If ignored files are intentional local-only guidance, record that; if the user expects commit-ready canonical docs, treat it as a defect to resolve.
- Decide the WIP draft fate after promotion: retain as provenance, update status to promoted, archive, or remove only with explicit approval.

## Recommended One-Liners

Living doc:

```markdown
- Living doc: every pass MUST review/tweak this file as guidance emerges/expires.
```

Style guard:

```markdown
- Style guard: keep this file short, scoped, and deduplicated; revise or replace stale/overlapping bullets instead of appending more.
```

## Validation Checklist

- Live file inventory excludes dependency/vendor directories.
- No promoted file says `Draft`, `Proposed`, or `proposed nested scope` except domain language.
- No trailing whitespace.
- Line counts are reasonable for local scope.
- Living-doc and style-guard bullets are present where desired.
- Draft inventory and promoted inventory match the approved plan.
- WIP draft folders clearly say whether they are still proposals or retained promotion provenance.
- Root `AGENTS.md` was not changed unless explicitly requested.
- Search index or semantic corpus is refreshed after edits when repo practice requires it; skip refresh during explicitly read-only audits.
