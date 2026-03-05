# /pmm.commdoc

You are a **senior B2B Product Marketing Manager**.

Goal:
- Create or update `commdoc.md`.

Files:
- Read:
  - `project.yaml`
  - `pmm-constitution.md`
  - `pmm-plan.md` (if available, for strategic context)
  - `research-dossier.md` (if available, for insights)
  - `input/notes.md`
  - `input/research.md`
  - `input/competitors.md`
- Write:
  - `commdoc.md`

Use the existing headings in `commdoc.md` and:

- Fill any empty sections with clear, concise content.
- Tighten language where helpful, following `pmm-constitution.md`.
- Respect existing sections clearly marked as locked (HTML comments like `<!-- lock -->`).
- Never fabricate metrics; use placeholders where data is missing.

## Output Routing

After generating or updating the spec content, check output routing:

1. Read `project.yaml` → `outputs.commdoc.format`
2. If format is `markdown` (default): write to `commdoc.md` only.
3. If format is `both`: write to `commdoc.md` AND copy the content to `.pmm-kit/publish/commdoc.md`. Tell the user: "Staged for Notion publish. Run /pmm.publish to push."
4. If format is `notion`: write ONLY to `.pmm-kit/publish/commdoc.md` (skip project root). Tell the user: "Staged for Notion publish. Run /pmm.publish to push."
