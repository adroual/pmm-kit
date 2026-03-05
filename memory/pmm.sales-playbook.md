# /pmm.sales-playbook

Goal:
- Create or update `sales-playbook.md` aligned with CommDoc & GTM.

Prerequisites:
- `commdoc.md` must exist. If not, run `/pmm.commdoc` first.
- Recommended: `narrative-playbook.md` exists for messaging hooks.

Files:
- Read: `pmm-constitution.md`, `project.yaml`, `pmm-plan.md` (if available), `commdoc.md`, `gtm-plan.md`, `narrative-playbook.md` if available.
- Write: `sales-playbook.md`.

Ensure the playbook is directly usable by Sales:

- Pitches should be simple to say out loud.
- Objection handling should be realistic and concrete.
- Competitive notes should be factual and not disparaging.

## Output Routing

After generating or updating the spec content, check output routing:

1. Read `project.yaml` → `outputs.sales-playbook.format`
2. If format is `markdown` (default): write to `sales-playbook.md` only.
3. If format is `both`: write to `sales-playbook.md` AND copy the content to `.pmm-kit/publish/sales-playbook.md`. Tell the user: "Staged for Notion publish. Run /pmm.publish to push."
4. If format is `notion`: write ONLY to `.pmm-kit/publish/sales-playbook.md` (skip project root). Tell the user: "Staged for Notion publish. Run /pmm.publish to push."
