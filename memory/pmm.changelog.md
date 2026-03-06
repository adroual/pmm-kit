# /pmm.changelog

Goal:
- Generate a public-facing changelog entry in `changelog.md` (or append to it).

Prerequisites:
- `commdoc.md` must exist. If not, run `/pmm.commdoc` first.

Files:
- Read: `pmm-plan.md` (if available), `commdoc.md` and any relevant information in `input/notes.md`.
- Write:
  - If `changelog.md` only contains the template: replace it with a first, dated entry.
  - If it already has entries: append a new dated section at the top.

Instructions:

- Use clear, customer-friendly language.
- Follow the structure: What’s new / What changes / Why / Who / When / Things to watch.
- Do not expose internal jargon, internal OKR codes, or implementation details.
- Optionally suggest a shorter summary variant that could be reused for in-app or help-center updates.

## Output Routing

After generating or updating the spec content, check output routing:

1. Read `project.yaml` → `outputs.changelog.format`
2. If format is `markdown` (default): write to `changelog.md` only. Done.
3. If format is `both` or `notion`:
   a. If `both`: write to `changelog.md` AND `.pmm-kit/publish/changelog.md`
   b. If `notion`: write ONLY to `.pmm-kit/publish/changelog.md` (skip project root)
   c. Ask user: **"Push to Notion now?"**
   d. If YES:
      - Read `notion_url` from `outputs.changelog` in `project.yaml`
      - Extract page ID (last 32 hex chars of the URL → format as UUID `8-4-4-4-12`)
      - Fetch page via Notion MCP to check if blank
      - Transform pipe tables → Notion XML tables (see `/pmm.publish` for format)
      - Escape unescaped `<` as `\<` (except inside XML tags)
      - Publish via Notion MCP (`replace_content` if blank, `insert_content_after` if not)
      - Report: **"Published to Notion: [URL]"**
   e. If NO: "Staged for Notion publish. Run `/pmm.publish` when ready."
