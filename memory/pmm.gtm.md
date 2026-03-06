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
2. If format is `markdown` (default): write to `gtm-plan.md` only. Done.
3. If format is `both` or `notion`:
   a. If `both`: write to `gtm-plan.md` AND `.pmm-kit/publish/gtm-package.md`
   b. If `notion`: write ONLY to `.pmm-kit/publish/gtm-package.md` (skip project root)
   c. Ask user: **"Push to Notion now?"**
   d. If YES:
      - Read `notion_url` from `outputs.gtm-package` in `project.yaml`
      - Extract page ID (last 32 hex chars of the URL → format as UUID `8-4-4-4-12`)
      - Fetch page via Notion MCP to check if blank
      - Transform pipe tables → Notion XML tables (see `/pmm.publish` for format)
      - Escape unescaped `<` as `\<` (except inside XML tags)
      - Publish via Notion MCP (`replace_content` if blank, `insert_content_after` if not)
      - Report: **"Published to Notion: [URL]"**
   e. If NO: "Staged for Notion publish. Run `/pmm.publish` when ready."
