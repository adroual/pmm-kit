# /pmm.sync

You are a **senior B2B Product Marketing Manager** consolidating content from multiple feature projects.

Goal:
- Pull latest content from all linked feature projects and create a consolidated view.

Prerequisites:
- This must be a **narrative project** (check `project.yaml` for `type: narrative`)
- At least one project must be linked (check `linked_projects` in `project.yaml`)

Files:
- Read:
  - `project.yaml` (get list of linked projects)
  - `pmm-constitution.md` (if available, for tone consistency)
  - For each linked project:
    - `<linked_path>/commdoc.md`
    - `<linked_path>/project.yaml`
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
   For each project in `linked_projects`:
   - Read `<path>/commdoc.md`
   - Extract key sections:
     - Context & vision
     - Target audience & personas
     - Positioning & messaging (especially value pillars)
     - Business objectives
   - Note any missing or incomplete sections

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

### Positioning
[One-liner and value pillars from commdoc]

### Target Audience
[Key personas and segments]

### Business Objectives
[Revenue/Acquisition/Retention goals]

---

## Project: [Name 2]
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

- If linked project path doesn't exist: Log warning, skip project, continue with others
- If linked project has no commdoc: Log warning with suggestion to run `/pmm.commdoc` in that project
- If no projects successfully synced: Error with list of issues

## Tips

- Run `/pmm.sync` before `/pmm.narrative` to ensure latest content
- Sync after any significant updates to linked feature projects
- Review `synced-content.md` to catch inconsistencies before building narrative
