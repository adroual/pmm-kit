# pmm-kit

**pmm-kit** is a CLI-first, Spec-driven Product Marketing workspace inspired by tools like Spec-kit and Claude Code.

It helps Product Marketing Managers generate and maintain:

- CommDocs
- GTM plans
- Narrative playbooks
- Sales playbooks
- Sales enablement briefs
- Success reports
- Changelogs

All as Markdown, all versioned in git, all powered by your favourite AI coding assistant.

## Install (local dev)

```bash
cd pmm-kit
pip install -e .
# or with uv / pipx when packaged
```

## Usage

Create a new project:

```bash
pmm init "Tap to Pay — Employee Access"
```

Then:

1. `cd` into the created project directory.
2. Open it in Claude Code, Gemini, Cursor, etc.
3. Use slash commands like `/pmm.constitution`, `/pmm.research`, `/pmm.commdoc`, `/pmm.gtm`.

This is an MVP; adjust templates and memory prompts to fit your own workflows.
