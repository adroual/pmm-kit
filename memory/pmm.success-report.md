# /pmm.success-report

Goal:
- Create or update `success-report.md` at the end of the launch.

Prerequisites:
- `gtm-plan.md` must exist (to compare objectives vs. results). If not, run `/pmm.gtm` first.

Files:
- Read: `project.yaml`, `pmm-plan.md` (if available), `commdoc.md`, `gtm-plan.md`, and any metrics the user includes in `input/results.md` if present.
- Write: `success-report.md`.

Use the template structure and:

- Compare objectives vs results honestly.
- Highlight 3–5 key learnings that will materially change future GTMs.
- Avoid vanity metrics; focus on what influenced behaviour and business impact.

## Output Routing

After generating or updating the spec content, check output routing:

1. Read `project.yaml` → `outputs.success-report.format`
2. If format is `markdown` (default): write to `success-report.md` only.
3. If format is `both`: write to `success-report.md` AND copy the content to `.pmm-kit/publish/success-report.md`. Tell the user: "Staged for Notion publish. Run /pmm.publish to push."
4. If format is `notion`: write ONLY to `.pmm-kit/publish/success-report.md` (skip project root). Tell the user: "Staged for Notion publish. Run /pmm.publish to push."
