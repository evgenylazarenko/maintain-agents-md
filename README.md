# Maintain AGENTS.md

Maintain AGENTS.md is a Codex skill for creating and maintaining repository-level and nested `AGENTS.md` files.

It creates domain-scoped AGENT.md files that help AI agents orient themselves in a project. Each file contains only the rules that change an agent's behavior in that scope, then point to the code, tests, contracts, runbooks, and documentation that hold the deeper truth.

## What it does

- Audits existing `AGENTS.md` files and repository boundaries.
- Derives guidance from current code, tests, contracts, and maintained documentation.
- Drafts proposed files for review before installing them by default.
- Adds nested scopes only when a directory has distinct rules, risks, or validation commands.
- Promotes approved drafts without leaving draft wording in live files.
- Checks for stale wording, missing maintenance guards, trailing whitespace, long files, and ignored guidance.

The default workflow is draft first, promote after approval. Direct installation is reserved for requests that already approve setup or promotion.

## Install

Install the skill:

```bash
npx skills add evgenylazarenko/maintain-agents-md
```

Or clone the repository into your Codex skills directory:

```bash
git clone https://github.com/evgenylazarenko/maintain-agents-md.git ~/.codex/skills/maintain-agents-md
```

## How to use (examples)
Simply ask Codex to use the skill. Some examples:

### Initial setup
```text
Use $maintain-agents-md to audit and update this repository's AGENTS.md files.
```

### Continuous refinement
```text
When done with your current task and prior to committing changes, use $maintain-agents-md to update the AGENT.md files in the parts of the repo that you touched.
```

## What's included

- [`SKILL.md`](SKILL.md): the workflow and scope rules.
- [`references/agent-doc-harness.md`](references/agent-doc-harness.md): the deeper design and promotion guidance.
- [`scripts/audit_agents_md.py`](scripts/audit_agents_md.py): a read-only structural auditor.
- [`agents/openai.yaml`](agents/openai.yaml): the Codex interface metadata.

## Run the auditor

```bash
python3 scripts/audit_agents_md.py /path/to/repo
```

If ignored `AGENTS.md` files are an intentional local-only policy, add `--allow-ignored`.
