# /pmm.publish — Publish PMM Kit output to Notion

Publish generated PMM specs to their configured Notion pages using the Notion MCP connection.

## How It Works

The Notion MCP accepts **Notion-flavored Markdown** directly — no block-level API conversion is needed. Standard markdown (headings, bold, italic, lists, dividers) passes through as-is. Only two transformations are required:

1. **Pipe tables → XML tables**: Convert `| col | col |` markdown tables to Notion's `<table>` XML format
2. **Escape `<`**: Any literal `<` in body text must be escaped as `\<` (otherwise interpreted as HTML)

## Workflow

1. Read `project.yaml` → `outputs`
2. Identify all spec types where `format` is `notion` or `both`
3. For each:
   a. Check that a staged file exists at `.pmm-kit/publish/<spec-type>.md`
   b. Extract the Notion page ID from the `notion_url` in `outputs.<spec-type>`:
      - Take the last 32 hex characters from the URL
      - Format as UUID: `8-4-4-4-12` (e.g., `abc123de-f456-abc1-23de-f456abc123de`)
   c. Read the markdown content from `.pmm-kit/publish/<spec-type>.md`
   d. Apply the two transformations:

      **Pipe table conversion** — turn this:
      ```
      | Objective | Target |
      |-----------|--------|
      | Revenue   | €2M    |
      ```
      Into this:
      ```xml
      <table header-row="true" fit-page-width="true">
      	<tr>
      		<td>**Objective**</td>
      		<td>**Target**</td>
      	</tr>
      	<tr>
      		<td>Revenue</td>
      		<td>€2M</td>
      	</tr>
      </table>
      ```
      - If the first data row is a separator (`|---|---|`), set `header-row="true"` and bold the header cell text
      - Always set `fit-page-width="true"`

      **Escape angle brackets** — replace any unescaped `<` in body text with `\<`. Do NOT escape `<` inside XML tags (`<table>`, `<tr>`, `<td>`, etc.).

   e. Use the Notion MCP `update-page` tool:
      - If the target page is **blank**: use `replace_content` with the full markdown
      - If the target page has **existing content**: use `insert_content_after` to append after the last block (use `fetch` first to get the selection anchor)
   f. Report success with the page URL

## Formatting Reference

These elements pass through to Notion unchanged:
- `# Heading` / `## Heading` / `### Heading` → H1 / H2 / H3
- `**bold**` and `*italic*` → bold and italic rich text
- `- item` → bulleted list
- `1. item` → numbered list
- `> quote` → quote block
- `---` → divider
- `` `code` `` → inline code
- `[text](url)` → hyperlink

## Important Rules

- **Append, don't replace** unless the page is blank. The target page may have template content from Notion database templates. Always fetch the page first to check.
- **Confirm before publishing.** Show the user which specs will be published to which pages and ask for confirmation before writing.
- **Handle long content.** If a spec is very large (100+ blocks), consider splitting across two `insert_content_after` calls.

## Usage

```
/pmm.publish                    # Publish all specs with notion/both format
/pmm.publish commdoc            # Publish only the commdoc spec
/pmm.publish --dry-run          # Show what would be published without writing
```

## Error Handling

- If no `project.yaml` exists → tell user to run `pmm init` first
- If `notion_url` is missing for a spec → skip and warn
- If the Notion page is not accessible → check MCP connection and page permissions
- If `.pmm-kit/publish/<spec-type>.md` doesn't exist → skip and warn, suggest running the relevant slash command first
