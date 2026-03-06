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
2. If format is `markdown` (default): write to `success-report.md` only. Done.
3. If format is `both` or `notion`:
   a. If `both`: write to `success-report.md` AND `.pmm-kit/publish/success-report.md`
   b. If `notion`: write ONLY to `.pmm-kit/publish/success-report.md` (skip project root)
   c. Ask user: **"Push to Notion now?"**
   d. If YES:
      - Read `notion_url` from `outputs.success-report` in `project.yaml`
      - Extract page ID (last 32 hex chars of the URL → format as UUID `8-4-4-4-12`)
      - Fetch page via Notion MCP to check if blank
      - Transform pipe tables → Notion XML tables (see `/pmm.publish` for format)
      - Escape unescaped `<` as `\<` (except inside XML tags)
      - Publish via Notion MCP (`replace_content` if blank, `insert_content_after` if not)
      - Report: **"Published to Notion: [URL]"**
   e. If NO: "Staged for Notion publish. Run `/pmm.publish` when ready."
