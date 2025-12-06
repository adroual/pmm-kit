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
