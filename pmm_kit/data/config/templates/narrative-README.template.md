# {{project.name}} — Narrative Project

This is a **narrative project** for bundling multiple feature launches into a unified story.

## What's Different

Unlike feature projects, narrative projects:
- **Don't have their own `commdoc.md`** — they pull from linked feature projects
- **Have `linked-projects.md`** — tracks which feature projects are bundled
- **Focus on the unified narrative** — creating a cohesive story across features

## Workflow

### 1. Link Feature Projects

First, link the feature projects you want to include:

```
/pmm.link ../feature-project-a
/pmm.link ../feature-project-b
```

### 2. Sync Content

Pull the latest content from linked projects:

```
/pmm.sync
```

This reads the `commdoc.md` from each linked project and creates a consolidated view.

### 3. Generate Narrative

Create the unified narrative that weaves all features together:

```
/pmm.narrative
```

## Files in This Project

| File | Purpose |
|------|---------|
| `project.yaml` | Project metadata and linked project paths |
| `linked-projects.md` | Tracks linked feature projects and sync status |
| `narrative-playbook.md` | Unified narrative across all linked features |
| `gtm-plan.md` | Consolidated GTM plan for the bundle |
| `input/` | Notes and research specific to this narrative |

## Tips

- Run `/pmm.sync` before `/pmm.narrative` to ensure you have latest content
- The narrative focuses on the **unified story**, not individual features
- Each linked feature project should have a complete `commdoc.md`
- You can still run `/pmm.research` with narrative-specific insights
