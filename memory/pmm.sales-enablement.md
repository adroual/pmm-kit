# /pmm.sales-enablement

Goal:
- Summarize what Sales needs to know in `sales-enablement.md`.

Prerequisites:
- `commdoc.md` and `gtm-plan.md` must exist. If not, run `/pmm.commdoc` and `/pmm.gtm` first.

Files:
- Read: `pmm-plan.md` (if available), `commdoc.md`, `gtm-plan.md`, `sales-playbook.md`, `narrative-playbook.md`.
- Write: `sales-enablement.md`.

Focus on:

- What this is
- Who it’s for
- Why it matters to Sales
- Where to find assets
- Training plan
- Feedback loop

Keep it short enough to be read in under 5 minutes.

## Output Routing

After generating or updating the spec content, check output routing:

1. Read `project.yaml` → `outputs.sales-enablement.format`
2. If format is `markdown` (default): write to `sales-enablement.md` only.
3. If format is `both`: write to `sales-enablement.md` AND copy the content to `.pmm-kit/publish/sales-enablement.md`. Tell the user: "Staged for Notion publish. Run /pmm.publish to push."
4. If format is `notion`: write ONLY to `.pmm-kit/publish/sales-enablement.md` (skip project root). Tell the user: "Staged for Notion publish. Run /pmm.publish to push."
