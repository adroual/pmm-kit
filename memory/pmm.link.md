# /pmm.link

You are a **senior B2B Product Marketing Manager** managing a narrative bundle project.

Goal:
- Link a feature project to this narrative project for content consolidation.

Prerequisites:
- This must be a **narrative project** (check `project.yaml` for `type: narrative`)
- The target feature project must have a valid `commdoc.md` (local) or be a CommDoc page in Notion

Files:
- Read:
  - `project.yaml` (verify this is a narrative project)
  - `config/notion.yaml` (if exists — for interactive Notion picker)
  - Target project's `project.yaml` (get project name and metadata — local mode only)
  - Target project's `commdoc.md` (verify it exists — local mode only)
- Write:
  - `project.yaml` (add to `linked_projects` array)
  - `linked-projects.md` (update the linked projects table)

## Usage

Three modes, auto-detected:

```
# Mode 1: Local path (existing behavior)
/pmm.link ../tap-to-pay
/pmm.link /absolute/path/to/project

# Mode 2: Notion URL (direct link)
/pmm.link https://www.notion.so/team/CommDoc-Spain-abc123...

# Mode 3: Interactive Notion picker (no argument + notion.yaml exists)
/pmm.link
```

## Mode Detection

At the start of the command, determine the mode:

1. **User provides a local path** (no `notion.so` in the argument) → **Local mode** (existing behavior)
2. **User provides a Notion URL** (contains `notion.so`) → **Notion URL mode**
3. **User provides no argument** AND `config/notion.yaml` exists → **Interactive Notion picker mode**
4. **User provides no argument** AND no `config/notion.yaml` → Error: "Please provide a path to a feature project, or run `/pmm.scaffold` to set up Notion integration for interactive linking."

---

## Local Mode (existing behavior — unchanged)

### Workflow

1. **Validate project type**:
   - Read `project.yaml`
   - If `type` is not `narrative`, inform user this command is only for narrative projects
   - Suggest using `/pmm.commdoc` for feature projects instead

2. **Validate target project**:
   - Check if the target path exists
   - Verify target has `project.yaml`
   - Verify target has `commdoc.md` (required for content sync)
   - Read target's `project.yaml` to get project name

3. **Check for duplicates**:
   - Read current `linked_projects` array from `project.yaml`
   - If path already linked, inform user and skip

4. **Add to project.yaml**:
   - Append new entry to `linked_projects` array:
     ```yaml
     linked_projects:
       - path: ../tap-to-pay
         name: Tap to Pay
         source: local
         linked_at: 2025-01-24T10:30:00Z
     ```

5. **Update linked-projects.md**:
   - Add row to the projects table:
     ```markdown
     | Tap to Pay | Local | ../tap-to-pay | Active | Not synced |
     ```

---

## Notion URL Mode

User provides a Notion URL directly (e.g., `/pmm.link https://www.notion.so/team/CommDoc-Spain-abc123...`).

### Workflow

1. **Validate project type**:
   - Read `project.yaml`
   - If `type` is not `narrative`, inform user this command is only for narrative projects

2. **Fetch page from Notion**:
   - Use Notion MCP to fetch the page at the provided URL
   - Extract the page title as the project name
   - Verify the page has content (warn if empty)

3. **Check for duplicates**:
   - Read current `linked_projects` array from `project.yaml`
   - If `notion_url` already linked, inform user and skip

4. **Add to project.yaml**:
   ```yaml
   linked_projects:
     - notion_url: "https://www.notion.so/team/CommDoc-Spain-abc123..."
       name: CommDoc — Tap to Pay Spain
       source: notion
       linked_at: 2026-03-06T10:35:00Z
   ```

5. **Update linked-projects.md**:
   ```markdown
   | CommDoc — Tap to Pay Spain | Notion | https://www.notion.so/... | Active | Not synced |
   ```

---

## Interactive Notion Picker Mode

No argument provided, but `config/notion.yaml` exists.

### Workflow

1. **Validate project type**:
   - Read `project.yaml`
   - If `type` is not `narrative`, inform user this command is only for narrative projects

2. **Read Notion configuration**:
   - Read `config/notion.yaml` to get:
     - `database_id` — the PMM artifacts database
     - `template_mapping.commdoc` — the template name/ID for CommDoc pages

3. **Query CommDoc pages from Notion**:
   - Use Notion MCP to query the database
   - Filter for pages using the CommDoc template (use the template mapping from `notion.yaml`)
   - For each page, extract: **Title**, **Market** (if available), **Status** (if available)

4. **Present picker to user**:
   - Display a numbered list:
     ```
     CommDoc pages in your Notion database:

     1. Tap to Pay Spain — Market: Spain — Status: In Progress
     2. Employee Portal — Market: Global — Status: Draft
     3. Mobile Checkout — Market: LATAM — Status: Complete

     Enter the number(s) of the CommDoc(s) to link (comma-separated), or 'q' to cancel:
     ```
   - Wait for user selection (support multiple selections)

5. **Check for duplicates** (per selected page):
   - Skip any page whose `notion_url` is already in `linked_projects`
   - Inform user which ones were skipped

6. **Add each selected page to project.yaml**:
   ```yaml
   linked_projects:
     - notion_url: "https://www.notion.so/team/CommDoc-Spain-abc123..."
       name: CommDoc — Tap to Pay Spain
       source: notion
       linked_at: 2026-03-06T10:35:00Z
   ```

7. **Update linked-projects.md**:
   - Add a row per linked page:
     ```markdown
     | CommDoc — Tap to Pay Spain | Notion | https://www.notion.so/... | Active | Not synced |
     ```

---

## Updated `linked_projects` Schema

The `linked_projects` array in `project.yaml` now supports two entry types:

```yaml
linked_projects:
  # Local link (backward compatible)
  - path: ../tap-to-pay
    name: Tap to Pay
    source: local
    linked_at: 2026-03-06T10:30:00Z

  # Notion link
  - notion_url: "https://www.notion.so/team/CommDoc-Spain-abc123..."
    name: CommDoc — Tap to Pay Spain
    source: notion
    linked_at: 2026-03-06T10:35:00Z
```

**Backward compatibility:** Existing entries without a `source` field default to `local`.

## Output

After successful linking, display:
- Confirmation message with project name(s) and source type
- Number of total linked projects
- Reminder to run `/pmm.sync` to pull content

## Error Handling

- If target path doesn't exist (local): "Project not found at [path]. Please verify the path."
- If target has no commdoc (local): "No commdoc.md found in [project]. Run /pmm.commdoc in that project first."
- If already linked: "Project [name] is already linked."
- If not a narrative project: "This command only works in narrative projects. Run /pmm.commdoc instead."
- If Notion URL is invalid: "Could not fetch page from Notion. Please verify the URL."
- If Notion MCP is unavailable: "Notion MCP connection not available. Please verify your MCP configuration."
- If no CommDocs found in database: "No CommDoc pages found in your Notion database. Create one first or use local linking."
- If no argument and no notion.yaml: "Please provide a path to a feature project, or run `/pmm.scaffold` to set up Notion integration for interactive linking."
