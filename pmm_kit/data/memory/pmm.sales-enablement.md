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
2. If format is `markdown` (default): write to `sales-enablement.md` only. Done.
3. If format is `both` or `notion`:
   a. If `both`: write to `sales-enablement.md` AND `.pmm-kit/publish/sales-enablement.md`
   b. If `notion`: write ONLY to `.pmm-kit/publish/sales-enablement.md` (skip project root)
   c. Ask user: **"Push to Notion now?"**
   d. If YES:
      - Read `notion_url` from `outputs.sales-enablement` in `project.yaml`
      - Extract page ID (last 32 hex chars of the URL → format as UUID `8-4-4-4-12`)
      - Fetch page via Notion MCP to check if blank
      - Transform pipe tables → Notion XML tables (see `/pmm.publish` for format)
      - Escape unescaped `<` as `\<` (except inside XML tags)
      - Publish via Notion MCP (`replace_content` if blank, `insert_content_after` if not)
      - Report: **"Published to Notion: [URL]"**
   e. If NO: "Staged for Notion publish. Run `/pmm.publish` when ready."
