# PMM-Kit

## Spec-Driven Product Marketing for the AI Era

PMM-Kit is a **CLI + AI workspace for Product Marketing Managers**. It gives PMMs the same structured, repeatable workflows that engineering teams use for specs and documentation — powered by AI slash commands.

Everything lives in Markdown. Everything is versioned in Git. AI does the heavy lifting.

**What you get:**

- A complete PMM project in seconds (`pmm init`)
- AI-generated documents: CommDoc, GTM Plan, Narrative, Sales Enablement, and more
- Structured frameworks grounded in real PMM best practices
- Optional Notion publishing — author in Markdown, publish to Notion for your team
- Full version history via Git

---

## Quick Start

### 1. Install

```bash
uv tool install pmm-kit --from git+https://github.com/adroual/pmm-kit.git
```

> Don't have `uv`? Install it first: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 2. Run the setup wizard

```bash
pmm
```

The wizard walks you through:
1. Installing slash commands globally (makes `/pmm.*` work everywhere)
2. Choosing your AI assistant (Claude, Gemini, Copilot, Cursor, etc.)
3. Choosing where specs live — **Markdown** (local files), **Notion** (via MCP), or **both**
4. Creating your first project

That's it. Your project is ready.

### 3. Open in Claude Code and start

```bash
cd your-project-name
claude .
```

Then run your first slash command:

```
/pmm.constitution
```

---

## How It Works

PMM-Kit operates in two phases:

**Phase 1 — Scaffold (CLI)**
You run `pmm init "Project Name"` in your terminal. This creates a project folder with templates, config, and slash commands ready to go.

**Phase 2 — Generate (AI)**
You open the project in Claude Code (or another AI IDE) and use slash commands like `/pmm.commdoc` or `/pmm.gtm`. The AI reads your inputs, follows the command's instructions, and writes structured marketing documents.

The slash commands are Markdown files in `.claude/commands/` — they tell the AI exactly what to read, what to write, and how to structure the output. No magic, no surprises.

---

## Workflows

### Guided Workflow (Recommended for New Users)

The guided workflow takes you from zero to a complete launch package, step by step:

```
/pmm.constitution    →  Establish brand voice and strategic priorities
/pmm.plan            →  Create a strategic plan for the launch
/pmm.tasks           →  Generate a phased task list
/pmm.execute         →  Execute tasks interactively (runs commands for you)
```

`/pmm.execute` is the orchestrator — it walks through your task list phase by phase, runs the right commands in order, checks prerequisites, and tracks progress. You can skip, pause, or customize at any point.

### Manual Workflow (Pick and Choose)

Run any command directly, in whatever order makes sense for your project:

| Step | Command | What it produces |
|------|---------|-----------------|
| Brand voice | `/pmm.constitution` | `pmm-constitution.md` |
| Research | `/pmm.research` | `research-dossier.md` |
| CommDoc | `/pmm.commdoc` | `commdoc.md` — positioning, messaging, audience, GTM strategy |
| GTM Plan | `/pmm.gtm` | `gtm-plan.md` — channels, plays, metrics |
| Narrative | `/pmm.narrative` | `narrative-playbook.md` — story arc, hooks, soundbites |
| Sales Battlecard | `/pmm.sales-playbook` | `sales-playbook.md` — pitches, objections, talk tracks |
| Sales Enablement | `/pmm.sales-enablement` | `sales-enablement.md` — training plan, assets |
| Changelog | `/pmm.changelog` | `changelog.md` — customer-facing entries |
| Retrospective | `/pmm.success-report` | `success-report.md` — results, insights, recommendations |

### Import Workflow (Existing Documents)

Already have marketing materials? Import them:

1. Drop files (PDF, Markdown, HTML, TXT) into `input/imports/`
2. Run `/pmm.import` — extracts content and merges into `commdoc.md`
3. Check `input/imports/import-log.md` for what was imported
4. Continue with `/pmm.gtm`, `/pmm.narrative`, etc.

### Narrative Workflow (Multi-Feature Bundles)

For bundling multiple feature launches into one unified story:

```bash
# 1. Create feature projects first (each needs a commdoc.md)
pmm init "Feature A"
pmm init "Feature B"

# 2. Create a narrative project
pmm init "Q1 Launch Bundle" --type narrative

# 3. In Claude Code, link and sync
/pmm.link ../feature-a
/pmm.link ../feature-b
/pmm.sync                   # Pulls content from linked projects
/pmm.narrative               # Creates unified narrative across all features
```

---

## Output Destinations: Markdown, Notion, or Both

When you run `pmm init`, you choose where your specs should live:

| Destination | What happens |
|-------------|-------------|
| **`markdown`** (default) | Specs are written as local `.md` files. No setup needed. |
| **`notion`** | Specs are published to Notion pages via MCP. Requires `/pmm.scaffold` setup. |
| **`both`** | Local `.md` files AND Notion pages. Best of both worlds. |

You can set this interactively during `pmm init`, or pass it as a flag:

```bash
pmm init "My Launch" --output markdown    # Local files only (default)
pmm init "My Launch" --output notion      # Notion pages
pmm init "My Launch" --output both        # Both
```

### Setting Up Notion

If you choose `notion` or `both`:

1. **`pmm init` saves your choice** in `project.yaml` under `outputs`
2. **If you've used Notion before** (`config/notion.yaml` exists), you'll be prompted for project-specific properties (market, quarter, priority, etc.) right during init
3. **Open the project in Claude Code** and run `/pmm.scaffold`
4. **Scaffold detects pending setup** — it reads your saved preferences and creates Notion pages without re-asking

**First-time Notion setup** (`/pmm.scaffold` in Claude Code):
- Discovers your Notion database schema via MCP
- Asks you to map database templates to PMM spec types (CommDoc, Narrative, GTM)
- Classifies properties (auto-filled vs. prompted vs. skipped)
- Saves the mapping to `config/notion.yaml` — only asks once per workspace

**Subsequent projects** — scaffold uses the saved mapping and any properties you provided during `pmm init`. It just creates pages and wires them into config.

Your `project.yaml` will look like:

```yaml
outputs:
  commdoc:
    format: notion
    notion_url: "https://www.notion.so/..."
  narrative:
    format: both
    notion_url: "https://www.notion.so/..."
  sales-playbook:
    format: markdown    # local only
```

PMM-Kit itself has **no Notion SDK dependency**. The CLI handles config and file management. Claude Code delivers content to Notion via its MCP connection.

---

## CLI Reference

### Commands

| Command | Description |
|---------|-------------|
| `pmm` | Setup wizard (first run) or quick help |
| `pmm init "Name"` | Create a new PMM project |
| `pmm install-commands` | Install slash commands globally for Claude Code |
| `pmm check` | Check environment and dependencies |
| `pmm update` | Check for updates |
| `pmm setup` | Re-run the setup wizard |
| `pmm help` | Show all commands and slash commands |

### `pmm init` Flags

```
--id ID            Custom project slug (auto-generated from name if omitted)
--ai PROVIDER      AI provider: claude, gemini, copilot, cursor, opencode, openai
--output DEST      Output destination: markdown (default), notion, or both
--type TYPE        Project type: feature (default) or narrative
--here             Use current directory instead of creating a new folder
--no-git           Skip git initialization
--force            Allow init in a non-empty directory
```

**Examples:**

```bash
pmm init "Tap to Pay Launch"
pmm init "Tap to Pay Launch" --ai claude --output notion
pmm init "Q1 Bundle" --type narrative --output both
pmm init "Quick Test" --here --no-git --force
```

---

## Slash Commands Reference

All slash commands are available inside your project in Claude Code (or any AI IDE that reads `.claude/commands/`).

### Workflow Orchestration

| Command | Output | Purpose |
|---------|--------|---------|
| `/pmm.plan` | `pmm-plan.md` | Strategic plan: scope, channels, success criteria |
| `/pmm.tasks` | `pmm-tasks.md` | Phased task list: Discovery → Foundation → GTM → Enablement → Launch |
| `/pmm.execute` | — | Interactive orchestrator: runs commands, checks dependencies, tracks progress |

### Core Documents

| Command | Output | Purpose |
|---------|--------|---------|
| `/pmm.constitution` | `pmm-constitution.md` | Brand voice, strategic priorities, writing guidelines |
| `/pmm.research` | `research-dossier.md` | Research synthesis: insights, JTBD, competitive landscape |
| `/pmm.commdoc` | `commdoc.md` | Launch CommDoc: positioning, messaging, audience, GTM |
| `/pmm.import` | `commdoc.md` | Import existing docs (PDF, MD, HTML, TXT) into CommDoc |
| `/pmm.gtm` | `gtm-plan.md` | GTM plan: channels, plays, localization, metrics |
| `/pmm.narrative` | `narrative-playbook.md` | Narrative: story arc, hooks, metaphors, soundbites |

### Enablement & Launch

| Command | Output | Purpose |
|---------|--------|---------|
| `/pmm.sales-playbook` | `sales-playbook.md` | Sales battlecard: pitches, objections, competitive tracks |
| `/pmm.sales-enablement` | `sales-enablement.md` | Enablement brief: training, assets, feedback loop |
| `/pmm.changelog` | `changelog.md` | Customer-facing changelog entries |
| `/pmm.success-report` | `success-report.md` | Post-launch retrospective: results, insights, next steps |

### Notion Integration

| Command | Purpose |
|---------|---------|
| `/pmm.scaffold` | Create Notion pages from templates, wire URLs into project config |
| `/pmm.publish` | Publish specs to Notion pages via MCP |

### Narrative Projects

| Command | Output | Purpose |
|---------|--------|---------|
| `/pmm.link` | `linked-projects.md` | Link a feature project to a narrative bundle |
| `/pmm.sync` | `synced-content.md` | Sync content from all linked feature projects |

---

## Project Structure

### Feature Project (default)

```
my-project/
├── project.yaml              # Project metadata and output config
├── commdoc.md                # Launch CommDoc
├── gtm-plan.md               # GTM plan
├── narrative-playbook.md     # Narrative playbook
├── sales-playbook.md         # Sales battlecard
├── sales-enablement.md       # Sales enablement
├── success-report.md         # Post-launch report
├── changelog.md              # Customer changelog
├── input/
│   ├── notes.md              # Your raw notes
│   ├── research.md           # Research inputs
│   ├── competitors.md        # Competitive analysis
│   └── imports/              # Drop existing docs here for /pmm.import
├── .claude/
│   └── commands/             # Slash commands (auto-copied from pmm-kit)
└── .gitignore
```

### Narrative Project

```
my-bundle/
├── project.yaml              # Includes linked_projects list
├── linked-projects.md        # Tracks linked feature projects
├── synced-content.md         # Consolidated content (via /pmm.sync)
├── gtm-plan.md               # Consolidated GTM plan
├── narrative-playbook.md     # Unified narrative
├── success-report.md         # Post-launch report
├── input/
│   ├── notes.md
│   ├── research.md
│   ├── competitors.md
│   └── imports/
├── .claude/
│   └── commands/
└── .gitignore
```

Narrative projects don't have `commdoc.md` — they pull content from linked feature projects via `/pmm.sync`.

---

## End-to-End Example

```bash
# Install
uv tool install pmm-kit --from git+https://github.com/adroual/pmm-kit.git

# Create project with Notion output
pmm init "Q2 Tap to Pay Spain" --ai claude --output notion

# Open in Claude Code
cd q2-tap-to-pay-spain
claude .
```

In Claude Code:

```
/pmm.scaffold        # Creates Notion pages, wires URLs into config
/pmm.constitution    # Define brand voice
/pmm.plan            # Strategic plan
/pmm.tasks           # Generate task list
/pmm.execute         # Run through everything interactively
```

When done, you have a complete launch package — local Markdown files and/or Notion pages — with CommDoc, GTM Plan, Narrative, Sales Enablement, Changelog, and Success Report.

---

## Updating

```bash
# Quick check
pmm update

# Force reinstall
uv cache clean
uv tool install pmm-kit --force --from git+https://github.com/adroual/pmm-kit.git
```

For development installs: `git pull` in the repo — changes take effect immediately.

---

## Contributing

- See `CLAUDE.md` for architecture and development guidance
- Slash command prompts are in `memory/*.md`
- Templates are in `config/templates/*.template.md`

To contribute: fork, branch, change, PR.

---

## License

MIT License

---

**Issues:** [GitHub Issues](https://github.com/adroual/pmm-kit/issues) | **Discussions:** [GitHub Discussions](https://github.com/adroual/pmm-kit/discussions)

**Built for Product Marketing Managers who want to ship with clarity and confidence.**
