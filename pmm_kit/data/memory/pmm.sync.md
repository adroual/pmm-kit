# /pmm.sync

You are a **senior B2B Product Marketing Manager** consolidating content from multiple feature projects.

Goal:
- Pull latest content from all linked feature projects and create a consolidated view.
- Supports both **local** projects (read `commdoc.md` from disk) and **Notion** projects (read page content via MCP).

Prerequisites:
- This must be a **narrative project** (check `project.yaml` for `type: narrative`)
- At least one project must be linked (check `linked_projects` in `project.yaml`)

Files:
- Read:
  - `project.yaml` (get list of linked projects)
  - `pmm-constitution.md` (if available, for tone consistency)
  - For each linked project:
    - If `source: local` (or no `source`): `<linked_path>/commdoc.md` and `<linked_path>/project.yaml`
    - If `source: notion`: fetch page content from `notion_url` via Notion MCP
- Write:
  - `synced-content.md` (consolidated view of all linked project content)
  - `linked-projects.md` (update sync status and timestamps)

## Workflow

1. **Validate project type**:
   - Read `project.yaml`
   - If `type` is not `narrative`, inform user this command is only for narrative projects

2. **Check linked projects**:
   - Read `linked_projects` array from `project.yaml`
   - If empty, inform user to run `/pmm.link` first

3. **Sync each linked project**:

   For each project in `linked_projects`, determine the source and read accordingly:

   ### Source: Local (or no `source` field — backward compatible)

   - Read `<path>/commdoc.md`
   - Extract key sections:
     - Context & vision
     - Target audience & personas
     - Positioning & messaging (especially value pillars)
     - Business objectives
   - Note any missing or incomplete sections

   ### Source: Notion

   - Use Notion MCP to fetch the page content from the `notion_url`
   - Parse the returned content (Notion blocks → text)
   - Extract the same key sections:
     - Context & vision
     - Target audience & personas
     - Positioning & messaging (especially value pillars)
     - Business objectives
   - Note any missing or incomplete sections
   - If Notion MCP is unavailable or the page fetch fails, log a warning and skip this project (continue with others)

4. **Create synced-content.md**:
   - Organize content by project
   - Highlight common themes across projects
   - Identify gaps or inconsistencies
   - Structure for easy reference by `/pmm.narrative`

5. **Update linked-projects.md**:
   - Update "Last Synced" column with current timestamp
   - Add sync event to history section

## Output Format

### synced-content.md

```markdown
# Synced Content

Last sync: [timestamp]
Projects synced: [count]

---

## Project: [Name 1]
Source: [Local | Notion]

### Positioning
[One-liner and value pillars from commdoc]

### Target Audience
[Key personas and segments]

### Business Objectives
[Revenue/Acquisition/Retention goals]

---

## Project: [Name 2]
Source: [Local | Notion]
...

---

## Cross-Project Analysis

### Common Themes
- [Theme identified across multiple projects]

### Shared Audiences
- [Overlapping personas or segments]

### Potential Conflicts
- [Any messaging or positioning conflicts]

### Gaps to Address
- [Missing information needed for unified narrative]
```

## Error Handling

- If linked project `source: local` and path doesn't exist: Log warning, skip project, continue with others
- If linked project `source: local` and has no commdoc: Log warning with suggestion to run `/pmm.commdoc` in that project
- If linked project `source: notion` and Notion MCP unavailable: Log warning "Could not connect to Notion MCP. Skipping [name].", continue with others
- If linked project `source: notion` and page fetch fails: Log warning "Could not fetch Notion page for [name]. The page may have been deleted or moved.", continue with others
- If no projects successfully synced: Error with list of issues

## Change Propagation

After writing `synced-content.md`, check for structural changes that may affect downstream documents:

1. Read `.pmm-kit/snapshots/synced-content.snapshot.md` (if it exists)
2. Extract structured fields from the newly written `synced-content.md`: positioning, audience, objectives, pricing/numbers, messaging (aggregated across all linked projects)
3. If **no snapshot exists**: save current extraction as baseline snapshot. Inform user: "Baseline snapshot created. Downstream documents will be checked for consistency on future runs." Done.
4. If **snapshot exists but no structured fields changed**: update snapshot timestamp. No propagation needed.
5. If **fields changed**:
   a. Update the snapshot with new values
   b. Show user a summary of what changed (old → new)
   c. Ask: **"Propagate changes to downstream documents?"**
   d. If YES: follow `/pmm.propagate` instructions to selectively update affected sections in `narrative-playbook.md` and `gtm-plan.md`
   e. If NO: "Run `/pmm.propagate` later to update downstream documents."

## Tips

- Run `/pmm.sync` before `/pmm.narrative` to ensure latest content
- Sync after any significant updates to linked feature projects
- Review `synced-content.md` to catch inconsistencies before building narrative
- For Notion-linked projects, ensure your MCP connection is active before syncing
