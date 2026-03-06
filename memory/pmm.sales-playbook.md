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
2. If format is `markdown` (default): write to `sales-playbook.md` only. Done.
3. If format is `both` or `notion`:
   a. If `both`: write to `sales-playbook.md` AND `.pmm-kit/publish/sales-playbook.md`
   b. If `notion`: write ONLY to `.pmm-kit/publish/sales-playbook.md` (skip project root)
   c. Ask user: **"Push to Notion now?"**
   d. If YES:
      - Read `notion_url` from `outputs.sales-playbook` in `project.yaml`
      - Extract page ID (last 32 hex chars of the URL → format as UUID `8-4-4-4-12`)
      - Fetch page via Notion MCP to check if blank
      - Transform pipe tables → Notion XML tables (see `/pmm.publish` for format)
      - Escape unescaped `<` as `\<` (except inside XML tags)
      - Publish via Notion MCP (`replace_content` if blank, `insert_content_after` if not)
      - Report: **"Published to Notion: [URL]"**
   e. If NO: "Staged for Notion publish. Run `/pmm.publish` when ready."
