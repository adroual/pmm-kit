# /pmm.gtm

Goal:
- Create or update `gtm-plan.md` based on `commdoc.md`.

Prerequisites:
- `commdoc.md` must exist. If not, run `/pmm.commdoc` first.

Files:
- Read: `project.yaml`, `pmm-constitution.md`, `pmm-plan.md` (for channel strategy), `commdoc.md`.
- Write: `gtm-plan.md`.

Use the existing headings in `gtm-plan.md` and:

- Make objectives, segments, and messages consistent with the CommDoc.
- Prioritize channels and plays (must-have vs. nice-to-have).
- Mark assumptions clearly.

## Output Routing

After generating or updating the spec content, check output routing:

1. Read `project.yaml` → `outputs.gtm-package.format`
2. If format is `markdown` (default): write to `gtm-plan.md` only.
3. If format is `both`: write to `gtm-plan.md` AND copy the content to `.pmm-kit/publish/gtm-package.md`. Tell the user: "Staged for Notion publish. Run /pmm.publish to push."
4. If format is `notion`: write ONLY to `.pmm-kit/publish/gtm-package.md` (skip project root). Tell the user: "Staged for Notion publish. Run /pmm.publish to push."
