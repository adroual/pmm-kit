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
# Create a new PMM project
pmm init "Project Name"
pmm init "Project Name" --id custom-slug --ai claude
pmm init "Project Name" --here  # Use current directory
pmm init "Project Name" --no-git  # Skip git initialization

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
- Copies markdown templates from `config/templates/*.template.md`
- Creates `input/` folder with starter files (notes.md, research.md, competitors.md)
- **Copies `memory/*.md` files to `.claude/commands/` in the project** (this makes slash commands work!)
- Generates `project.yaml` with metadata
- Optionally initializes git
- Displays beautiful success screen with next steps

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

- **`/pmm.gtm`** - Takes the CommDoc and generates the GTM Plan with objectives recap, segmentation, key messages, channel plan, plays (top/mid/bottom funnel), localization, and measurement.

- **`/pmm.narrative`** - Generates the Narrative Playbook with one-sentence story, before/after, narrative arc, hooks & metaphors, narrative by audience, and soundbites.

**Enablement & Launch:**

- **`/pmm.sales-playbook`** - Creates the sales battlecard-style document with elevator pitches, discovery questions, objection handling, and competitive talk tracks.

- **`/pmm.sales-enablement`** - Creates a document summarizing what Sales needs to know, assets, training plan, call talk track, and feedback loop.

- **`/pmm.changelog`** - Produces customer-friendly changelog entries linked to the CommDoc.

- **`/pmm.success-report`** - At the end of launch, produces: did we hit objectives? insights, results by channel, and recommendations.

**4. Configuration Flow**

- Global config: `config/pmm.config.yaml` (default AI provider)
- Project config: Created as `project.yaml` in each project workspace
- Templates: `config/templates/*.template.md` copied to new projects

### Important Implementation Details

**Project ID Generation**: Project names are auto-slugified if no `--id` provided (pmm_kit/core/slugify.py:5-11). Example: "Tap to Pay — Employee Access" becomes "tap-to-pay-employee-access".

**Repo Root Detection**: The CLI finds the repo root using `Path(__file__).resolve().parents[2]` (pmm_kit/cli/main.py:94, 112). This assumes the script is at `pmm_kit/cli/main.py`.

**AI Provider Selection**: Interactive questionary-based picker when `--ai` flag not provided (pmm_kit/cli/main.py:19-48). Supports claude, gemini, copilot, cursor, opencode, openai.

**Git Initialization**: Automatically runs `git init` in project directory unless `--no-git` flag used. Creates basic `.gitignore` (pmm_kit/core/files.py:80-93).

**Template Variable Substitution**: Currently templates use `{{project.name}}` placeholders but there's no templating engine. These are intended to be manually edited or replaced by AI assistants.

## Expected Project Structure

After `pmm init "Project Name"`, the created project contains:

```
projects/<slug>/
├── project.yaml              # Project metadata
├── pmm-plan.md              # Strategic plan (via /pmm.plan) [NEW]
├── pmm-tasks.md             # Task list (via /pmm.tasks) [NEW]
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
│   └── competitors.md      # Competitive analysis
├── .claude/
│   └── commands/           # Slash commands (auto-copied from memory/)
├── .git/                    # Git repository (optional)
└── .gitignore
```

## Working with Projects

PMM-Kit now supports **two workflows**:

### Workflow 1: Guided Orchestration (Recommended for New Users)

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

### Workflow 2: Manual Execution (Advanced Users)

Users can also run slash commands manually in their preferred order:
1. Run `/pmm.constitution` to establish brand voice
2. Run `/pmm.research` to synthesize insights
3. Run `/pmm.commdoc` to bootstrap the CommDoc
4. Run `/pmm.gtm`, `/pmm.narrative`, etc. as needed

The memory prompts reference:
- `project.yaml` - Project metadata
- `pmm-plan.md` - Strategic plan (if using guided workflow)
- `pmm-tasks.md` - Task list with completion status
- `pmm-constitution.md` - Brand voice (created by `/pmm.constitution`)
- `input/*.md` - Research and notes
- Output files: `commdoc.md`, `gtm-plan.md`, etc.

**Key Design Principles:**
- Users always know which file is edited
- Dependencies are checked (e.g., `/pmm.gtm` requires `commdoc.md`)
- Tasks can be customized by editing `pmm-tasks.md`
- Both workflows produce the same high-quality artifacts

## Package Structure

The package is explicitly configured in pyproject.toml:
```toml
[tool.setuptools]
packages = ["pmm_kit", "pmm_kit.cli", "pmm_kit.core"]
```

The CLI entry point `pmm` maps to `pmm_kit.cli.main:main`.

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
