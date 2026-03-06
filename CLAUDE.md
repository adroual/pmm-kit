# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What PMM-Kit Is

PMM-Kit is a CLI-first, AI-powered Product Marketing workspace, heavily inspired by Spec-Kit and engineered to help Product Marketing Managers work the way developers work: with version-controlled, spec-driven workflows.

It provides:
- A command-line interface (`pmm`)
- A structured project scaffolding system
- A library of PMM templates (CommDoc, GTM plan, Narrative, Sales Enablement, Success Report, Changelog…)
- A set of AI agent instructions ("slash commands") that Claude/Gemini/Cursor/OpenAI can execute to automatically generate, update, or refine PMM artifacts
- A workflow that keeps everything in plain text + Git, so that PMM work is reproducible, auditable, and collaborative

**PMM-Kit is NOT a web app.** It is a dev-style tool for PMMs, meant to be used inside a terminal and AI coding IDEs like Claude Code.

The tool operates in two phases:
1. **Init phase**: Uses the `pmm` CLI to bootstrap a new project workspace
2. **AI-assisted phase**: Users work in the created project using slash commands (memory prompts) to generate marketing artifacts

## Target User

PMMs in SaaS / fintech / tech companies building:
- Feature specs
- Go-to-market plans
- Product narratives
- Sales enablement
- Changelogs
- Success reports

PMM-Kit is designed for people who want to manage PMM work the same way developers manage specs or documentation.

## Core Philosophy

### Text-first, Git-native
All PMM outputs are Markdown files stored locally. No databases, no servers. Just text + Git.

### AI-native
Users rely on Claude/Gemini/Cursor to fill and maintain documents via slash commands. PMM-Kit provides the specs, instructions, and templates the agent needs.

### Deterministic & Predictable
Slash commands must:
- Read from specific files
- Write to specific files
- Never generate surprises
- Never break the document structure

### Reusable, Portable, Opinionated
PMM-Kit encodes industry-standard PMM workflows in reusable templates.

## Development Commands

### Installation & Setup
```bash
# Install in editable mode for development
pip install -e .

# The pmm command becomes available after installation
pmm --help
```

### Running the CLI
```bash
# Create a new PMM project (feature type - default)
pmm init "Project Name"
pmm init "Project Name" --id custom-slug --ai claude
pmm init "Project Name" --here  # Use current directory
pmm init "Project Name" --no-git  # Skip git initialization

# Create a narrative project (for bundling multiple features)
pmm init "Q1 Launch Bundle" --type narrative

# Check environment
pmm check

# Get help
pmm help
```

### CLI Design
The CLI uses the `rich` library for beautiful, colorful terminal output:
- Color-coded messages: cyan for info, green for success, yellow for warnings, red for errors
- ASCII art banner on startup
- Progress indicators and bordered sections
- Interactive questionary-based selectors with custom styling
- Post-init success screen with comprehensive next steps

### Testing
There are currently no automated tests in this repository.

## Architecture

### Code Structure

```
pmm_kit/
├── cli/
│   └── main.py          # CLI entry point, argument parsing, user interaction, help screens
└── core/
    ├── banner.py        # ASCII art and banner utilities
    ├── config.py        # YAML config loading/saving
    ├── files.py         # Project initialization, file operations, git setup, success screens
    ├── logger.py        # Rich-powered colored console output utilities
    └── slugify.py       # String slugification for project IDs
```

### Key Architectural Concepts

**1. Dual-Mode Operation**

The system has two distinct operational contexts:
- **pmm-kit repo**: Where the CLI tool itself lives (this repo)
- **Project workspace**: Created by `pmm init`, contains actual marketing artifacts

**2. Template-Based Project Creation**

When `pmm init` runs (pmm_kit/core/files.py):
- Creates a new folder under `projects/` (or uses current dir with `--here`)
- Copies markdown templates from `config/templates/*.template.md` (conditionally based on project type)
  - **Feature projects**: Full template set including `commdoc.md`, sales templates, changelog
  - **Narrative projects**: Subset with `linked-projects.md` instead of `commdoc.md`
- Creates `input/` folder with starter files (notes.md, research.md, competitors.md)
- Creates `input/imports/` folder with README for document import workflow
- **Copies `memory/*.md` files to `.claude/commands/` in the project** (this makes slash commands work!)
- Generates `project.yaml` with metadata (includes `type` and `linked_projects` for narrative projects)
- Optionally initializes git
- Displays beautiful success screen with type-specific next steps

**3. Memory-Based Slash Commands**

The `memory/` directory in the pmm-kit repo contains prompt templates named `pmm.<command>.md`. During `pmm init`, these files are **automatically copied** to `.claude/commands/` in the created project, making them available as actual slash commands in Claude Code.

This is a critical architectural decision: the slash commands are not executed by the `pmm` CLI itself—they're meant for AI assistants working inside the created projects.

Available slash commands:

**Workflow Orchestration (NEW):**

- **`/pmm.plan`** - Creates a strategic plan (`pmm-plan.md`) that establishes launch scope, research approach, positioning strategy, channel strategy, success criteria, and dependencies. This is the starting point for guided workflows.

- **`/pmm.tasks`** - Generates a phased, actionable task list (`pmm-tasks.md`) derived from the strategic plan. Creates a step-by-step checklist with phases: Discovery, Foundation, GTM Strategy, Enablement, and Launch.

- **`/pmm.execute`** - Interactive workflow orchestrator that walks through the task list, executes slash commands in order, checks dependencies, and tracks progress. Supports both guided mode (step-by-step) and auto mode.

**Core Documents:**

- **`/pmm.constitution`** - Creates the foundational document describing brand tone, strategic priorities, markets, PMM frameworks, and writing guidelines. Every other AI command must rely on it.

- **`/pmm.research`** - Synthesizes raw notes into insights, jobs-to-be-done, pains, trigger events, competitive landscape, and assumptions. Outputs: `research-dossier.md`

- **`/pmm.commdoc`** - Generates or updates the full Launch CommDoc with context & vision, business objectives (Revenue/Acquisition/Retention), target audience & personas, product scope, positioning & messaging, GTM strategy, cross-team dependencies, and metrics.

- **`/pmm.import`** - Multi-source knowledge base builder. Gathers content from 4 sources: local files in `input/imports/`, user-provided Notion URLs, Notion workspace discovery (searches workspace using project context, asks user to approve), and web research (fills gaps in competitor/market data). Classifies and routes content to both `commdoc.md` sections AND input files (`input/notes.md`, `input/research.md`, `input/competitors.md`). Creates comprehensive `input/imports/import-log.md` tracking all sources, origins, and destinations.

- **`/pmm.gtm`** - Takes the CommDoc and generates the GTM Plan with objectives recap, segmentation, key messages, channel plan, plays (top/mid/bottom funnel), localization, and measurement.

- **`/pmm.narrative`** - Generates the Narrative Playbook with one-sentence story, before/after, narrative arc, hooks & metaphors, narrative by audience, and soundbites. Has dual-mode behavior: in feature projects reads from `commdoc.md`, in narrative projects reads from `synced-content.md` (linked projects).

**Enablement & Launch:**

- **`/pmm.sales-playbook`** - Creates the sales battlecard-style document with elevator pitches, discovery questions, objection handling, and competitive talk tracks.

- **`/pmm.sales-enablement`** - Creates a document summarizing what Sales needs to know, assets, training plan, call talk track, and feedback loop.

- **`/pmm.changelog`** - Produces customer-friendly changelog entries linked to the CommDoc.

- **`/pmm.success-report`** - At the end of launch, produces: did we hit objectives? insights, results by channel, and recommendations.

**Narrative Project Commands (for `--type narrative` projects):**

- **`/pmm.link`** - Links a feature project to the narrative bundle. Validates the target project has a `commdoc.md`, then adds it to `linked_projects` in `project.yaml` and updates `linked-projects.md`.

- **`/pmm.sync`** - Syncs content from all linked feature projects. Reads each linked project's `commdoc.md`, extracts key sections (positioning, audience, objectives), and creates `synced-content.md` with a consolidated view and cross-project analysis.

**Change Propagation:**

- **`/pmm.propagate`** - Detects changes in structured fields (positioning, audience, objectives, pricing, messaging) of upstream documents and selectively regenerates affected sections in downstream documents. Uses snapshot-based change detection (`.pmm-kit/snapshots/`) to compare field values between runs. Annotates changed values with `(updated MM/DD/YY)` timestamps. Automatically triggered after `/pmm.commdoc`, `/pmm.narrative`, and `/pmm.sync` when structural changes are detected — or can be run manually.

**4. Configuration Flow**

- Global config: `config/pmm.config.yaml` (default AI provider)
- Project config: Created as `project.yaml` in each project workspace
- Templates: `config/templates/*.template.md` copied to new projects

### Important Implementation Details

**Project ID Generation**: Project names are auto-slugified if no `--id` provided (pmm_kit/core/slugify.py:5-11). Example: "Tap to Pay — Employee Access" becomes "tap-to-pay-employee-access".

**Project Type**: The `--type` flag accepts `feature` (default) or `narrative`. This controls which templates are copied and how `project.yaml` is structured. Narrative projects get `linked_projects: []` in their config.

**Repo Root Detection**: The CLI finds the repo root using `Path(__file__).resolve().parents[2]` (pmm_kit/cli/main.py:94, 112). This assumes the script is at `pmm_kit/cli/main.py`.

**AI Provider Selection**: Interactive questionary-based picker when `--ai` flag not provided (pmm_kit/cli/main.py:19-48). Supports claude, gemini, copilot, cursor, opencode, openai.

**Git Initialization**: Automatically runs `git init` in project directory unless `--no-git` flag used. Creates basic `.gitignore` (pmm_kit/core/files.py:80-93).

**Template Variable Substitution**: Currently templates use `{{project.name}}` placeholders but there's no templating engine. These are intended to be manually edited or replaced by AI assistants.

**Conditional Template Copying**: Feature projects get the full template set. Narrative projects skip `commdoc.md`, sales templates, and changelog, but get `linked-projects.md` instead.

## Expected Project Structure

### Feature Project (default)

After `pmm init "Project Name"`, the created project contains:

```
projects/<slug>/
├── project.yaml              # Project metadata (type: feature)
├── pmm-plan.md              # Strategic plan (via /pmm.plan)
├── pmm-tasks.md             # Task list (via /pmm.tasks)
├── pmm-constitution.md      # Brand voice & guidelines (via /pmm.constitution)
├── research-dossier.md      # Research synthesis (via /pmm.research)
├── commdoc.md               # CommDoc (populated via /pmm.commdoc)
├── gtm-plan.md              # GTM plan (via /pmm.gtm)
├── narrative-playbook.md    # Narrative (via /pmm.narrative)
├── sales-playbook.md        # Sales battlecard (via /pmm.sales-playbook)
├── sales-enablement.md      # Sales enablement (via /pmm.sales-enablement)
├── success-report.md        # Launch retrospective (via /pmm.success-report)
├── changelog.md             # Customer-facing changelog (via /pmm.changelog)
├── input/
│   ├── notes.md            # Raw notes
│   ├── research.md         # Research inputs
│   ├── competitors.md      # Competitive analysis
│   └── imports/            # Drop existing docs here for /pmm.import
│       └── README.md       # Instructions for importing
├── .pmm-kit/
│   ├── publish/             # Staged content for Notion publishing
│   └── snapshots/           # Field snapshots for change propagation
├── .claude/
│   └── commands/           # Slash commands (auto-copied from memory/)
├── .git/                    # Git repository (optional)
└── .gitignore
```

### Narrative Project

After `pmm init "Project Name" --type narrative`, the created project contains:

```
projects/<slug>/
├── project.yaml              # Project metadata (type: narrative, linked_projects: [])
├── linked-projects.md        # Tracks linked feature projects
├── synced-content.md         # Consolidated content from linked projects (via /pmm.sync)
├── pmm-constitution.md       # Brand voice & guidelines (via /pmm.constitution)
├── gtm-plan.md               # Consolidated GTM plan (via /pmm.gtm)
├── narrative-playbook.md     # Unified narrative (via /pmm.narrative)
├── success-report.md         # Launch retrospective (via /pmm.success-report)
├── input/
│   ├── notes.md             # Raw notes
│   ├── research.md          # Research inputs
│   ├── competitors.md       # Competitive analysis
│   └── imports/             # Drop existing docs here for /pmm.import
│       └── README.md        # Instructions for importing
├── .pmm-kit/
│   ├── publish/              # Staged content for Notion publishing
│   └── snapshots/            # Field snapshots for change propagation
├── .claude/
│   └── commands/            # Slash commands (auto-copied from memory/)
├── .git/                     # Git repository (optional)
└── .gitignore
```

**Key differences:** Narrative projects do NOT have `commdoc.md` (they read from linked projects instead). They have `linked-projects.md` for tracking linked feature projects.

## Working with Projects

PMM-Kit supports **two project types** and multiple workflows:

### Project Types

| Aspect | Feature Project (default) | Narrative Project |
|--------|---------------------------|-------------------|
| Created with | `pmm init "Name"` | `pmm init "Name" --type narrative` |
| Has `commdoc.md` | Yes | No (reads from linked projects) |
| Has `linked-projects.md` | No | Yes |
| project.yaml `type` | `feature` | `narrative` |
| project.yaml `linked_projects` | N/A | `[]` (array) |
| Primary workflow | `/pmm.commdoc` → `/pmm.gtm` | `/pmm.link` → `/pmm.sync` → `/pmm.narrative` |

### Feature Project Workflows

#### Workflow 1: Guided Orchestration (Recommended for New Users)

After running `pmm init`, users:
1. `cd` into the created project directory
2. Open it in Claude Code (or other AI assistant)
3. Run `/pmm.constitution` to establish brand voice and strategic priorities
4. Run `/pmm.plan` to create the strategic plan
5. Run `/pmm.tasks` to generate a phased task list
6. Run `/pmm.execute` to execute tasks interactively with dependency checking

The `/pmm.execute` command will:
- Walk through tasks phase by phase
- Automatically run the appropriate slash commands (e.g., `/pmm.research`, `/pmm.commdoc`)
- Check prerequisites before executing commands
- Track progress by marking tasks complete in `pmm-tasks.md`
- Allow users to skip, pause, or customize the workflow

#### Workflow 2: Manual Execution (Advanced Users)

Users can also run slash commands manually in their preferred order:
1. Run `/pmm.constitution` to establish brand voice
2. Run `/pmm.research` to synthesize insights
3. Run `/pmm.commdoc` to bootstrap the CommDoc (or `/pmm.import` to import existing docs)
4. Run `/pmm.gtm`, `/pmm.narrative`, etc. as needed

#### Workflow 3: Import Existing Documents

For projects with existing marketing materials:
1. Place documents (PDF, MD, HTML, TXT) in `input/imports/`
2. Run `/pmm.import` to extract and consolidate into `commdoc.md`
3. Review `input/imports/import-log.md` to see what was imported
4. Continue with `/pmm.gtm`, `/pmm.narrative`, etc.

### Narrative Project Workflow

For bundling multiple feature launches into a unified narrative:

1. **Create feature projects first**: Each feature should have its own project with a complete `commdoc.md`
2. **Create narrative project**: `pmm init "Q1 Bundle" --type narrative`
3. **Link feature projects**:
   ```
   /pmm.link ../feature-a
   /pmm.link ../feature-b
   ```
4. **Sync content**: `/pmm.sync` pulls latest from all linked projects into `synced-content.md`
5. **Generate unified narrative**: `/pmm.narrative` creates a cohesive story across all features
6. **Generate consolidated GTM**: `/pmm.gtm` for the bundle

### Files Referenced by Memory Prompts

- `project.yaml` - Project metadata (including `type` and `linked_projects` for narrative projects)
- `pmm-plan.md` - Strategic plan (if using guided workflow)
- `pmm-tasks.md` - Task list with completion status
- `pmm-constitution.md` - Brand voice (created by `/pmm.constitution`)
- `input/*.md` - Research and notes
- `input/imports/` - Documents for import
- `linked-projects.md` - Linked projects (narrative only)
- `synced-content.md` - Consolidated content from linked projects (narrative only)
- Output files: `commdoc.md`, `gtm-plan.md`, etc.
- `.pmm-kit/publish/` - Staged markdown for Notion publishing
- `.pmm-kit/snapshots/` - Structured field snapshots for change propagation (used by `/pmm.propagate`)

**Key Design Principles:**
- Users always know which file is edited
- Dependencies are checked (e.g., `/pmm.gtm` requires `commdoc.md` or `synced-content.md`)
- Tasks can be customized by editing `pmm-tasks.md`
- Both project types produce high-quality artifacts

## Package Structure

The package is explicitly configured in pyproject.toml:
```toml
[tool.setuptools]
packages = ["pmm_kit", "pmm_kit.cli", "pmm_kit.core"]
```

The CLI entry point `pmm` maps to `pmm_kit.cli.main:main`.

## CRITICAL: Slash Command Dual-Directory Sync

Slash commands exist in **two locations** that MUST stay in sync:

| Location | Purpose |
|----------|---------|
| `memory/pmm.*.md` | **Source of truth** — the authoritative versions, used by dev installs and `pmm install-commands` |
| `pmm_kit/data/memory/pmm.*.md` | **Packaged copy** — bundled into the pip/uv package for non-dev installs |

**When you add, edit, or delete a slash command in `memory/`, you MUST also update `pmm_kit/data/memory/`.**

If you forget, the command will work in dev installs but **be invisible** in `uv tool install` installs — the exact bug that bit us when `pmm.scaffold.md` and `pmm.publish.md` were missing for packaged users.

Quick sync command:
```bash
# Copy all slash commands from source to package data
for f in memory/pmm.*.md; do cp "$f" "pmm_kit/data/memory/$(basename "$f")"; done

# Verify they match
diff <(ls memory/pmm.*.md | xargs -I{} basename {} | sort) \
     <(ls pmm_kit/data/memory/pmm.*.md | xargs -I{} basename {} | sort)
```

The same applies to config templates: `config/templates/` is the source, `pmm_kit/data/config/templates/` is the packaged copy.

## Development Notes

- Python 3.10+ required
- Dependencies:
  - `rich>=13.0` - Beautiful terminal output with colors, panels, and formatting
  - `questionary>=2.0` - Interactive prompts and selectors
  - `PyYAML>=6.0` - YAML config file handling
- Logger functions available: `log_info()`, `log_success()`, `log_error()`, `log_warning()`, `log_step()`
- Console available via `from pmm_kit.core.logger import console` for rich printing
- Banner utilities in `pmm_kit.core.banner` for consistent branding
- Minimal error handling - relies on exceptions bubbling up to main()

## Design Principles

PMM-Kit follows these design principles:

**Clean UX** - Inspired by Spec-kit, with predictable file layout and minimal state machine.

**Deterministic logic** - No magical behaviors. Users always understand what's happening.

**Predictable file layout** - Consistent structure across all projects.

**AI agent clarity** - The AI always knows which file to read, which file to write, and how to interpret documents.

## What Success Looks Like

Claude (or Gemini/OpenAI/Cursor) should be able to:
- Autonomously populate PMM documents
- Keep them updated as inputs evolve
- Maintain structure, clarity, and consistency
- Produce GTMs, narratives, enablement docs, and retro reports
- Build a reusable, high-quality PMM operating system

## Long-Term Vision

PMM-Kit should become the PMM equivalent of a code framework:
- Reusable scaffolding
- Consistent workflows
- One-command project setup
- Git-friendly documentation
- AI-native spec maintenance

Future versions may include:
- A project wizard with multi-step TUI
- Feature lifecycle automations
- Integrations with PMs and engineers
- Optional remote storage (GitHub → Issues or PR templates)

**But the core stays CLI-first + Markdown-first + AI-driven.**

# PMM Kit — Notion Integration Architecture

## Overview

PMM Kit supports two output formats for generated specs: **Markdown files** (local) and **Notion pages** (remote). The user configures the output destination per spec type in the project config. Claude Code handles Notion delivery via its MCP connection — **PMM Kit itself has no Notion SDK dependency**.

## Output Flow

```
pmm-kit generate <spec-type>
        │
        ├── format: markdown → writes .md file to /specs/<spec-type>/
        ├── format: notion   → outputs structured markdown to stdout/temp file
        │                      → Claude Code reads it and pushes to Notion via MCP
        └── format: both     → does both of the above
```

## Project Config Schema (`config/project.yaml`)

```yaml
project:
  name: "Tap to Pay Spain Launch"
  market: "Spain"

outputs:
  commdoc:
    format: notion          # markdown | notion | both
    notion_url: "https://www.notion.so/team/CommDoc-TtP-Spain-abc123..."
  narrative:
    format: notion
    notion_url: "https://www.notion.so/team/Narrative-TtP-Spain-def456..."
  gtm-package:
    format: both
    notion_url: "https://www.notion.so/team/GTM-Package-TtP-Spain-ghi789..."
```

## Notion URL → Page ID Extraction

Notion URLs contain the page ID as the last 32 hex chars (with or without dashes). PMM Kit must extract this reliably:

```
https://www.notion.so/team/My-Page-Title-abc123def456ghi789jkl012mno345pq
                                         └──────── page_id (32 hex) ────────┘
```

Strip dashes and take the last 32 characters. Format as UUID (8-4-4-4-12) for API calls.

## Critical Rules

1. **Never create child pages.** The user provides a URL to an existing page (created from a Notion database template). PMM Kit / Claude Code writes content **directly onto that page body**.
2. **No Notion SDK in PMM Kit.** The Python CLI outputs content. Claude Code delivers it via MCP.
3. **Respect existing page content.** If the page was created from a template, it may have pre-existing structure (headers, callout blocks, etc.). The publishing step should **append content after existing blocks**, not wipe the page.
4. **Notion block limits.** Notion API allows max 100 blocks per append call. Batch large documents accordingly. Rich text blocks have a 2000-character limit per text segment.

## Three Database Templates

The PMM team uses a Notion database for PMM artifacts with three templates:

| Template     | Spec Type in PMM Kit | Purpose                                    |
|-------------|---------------------|--------------------------------------------|
| CommDoc     | `commdoc`           | Communication document — positioning, messaging, proof points |
| Narrative   | `narrative`         | Narrative playbook — story arc, audience framing, key messages |
| GTM Package | `gtm-package`       | Go-to-market package — launch plan, channels, timeline, enablement |

## Scaffolding (Phase 2)

The `/pmm-scaffold` command automates project setup and is **fully workspace-agnostic** — it makes zero assumptions about template names, property names, or database structure.

### First run: discovery + mapping
1. Connects to the user's PMM artifacts database via MCP
2. Discovers the schema (properties, types, options) and available templates
3. Interactively asks the user to map templates → spec types (commdoc, narrative, gtm-package)
4. Interactively asks the user to map properties → fields (project name, market, status, etc.)
5. Saves the full mapping in `config/notion.yaml`

### Subsequent runs: create + wire
1. Creates pages in the database from each mapped template
2. Sets properties (project name, market, status) based on saved mapping
3. Extracts Notion URLs of the created pages
4. Writes them into `config/project.yaml` under `outputs:`

### Fallback
If MCP doesn't support template instantiation, create blank pages in the database with the right properties. The URLs are still captured and wired into config. The user applies templates manually in Notion UI.