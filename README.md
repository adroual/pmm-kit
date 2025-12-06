# PMM-Kit

**Spec-driven Product Marketing for the AI era**

PMM-Kit is a CLI-first, AI-powered Product Marketing workspace that helps PMMs work like developers: with version-controlled, spec-driven workflows.

Stop juggling Google Docs. Start shipping structured, reproducible, high-quality PMM artifacts—all in Markdown, all in Git, all powered by AI.

---

## 🎯 What is PMM-Kit?

PMM-Kit is inspired by developer tools like [Spec-Kit](https://github.com/anthropics/spec-kit) and designed for Product Marketing Managers who want to:

- **Work in plain text** — All outputs are Markdown files, not locked in Google Docs
- **Version everything** — Use Git for collaboration, history, and accountability
- **Automate with AI** — Let Claude, Gemini, or Cursor write and maintain your PMM documents
- **Follow a proven workflow** — From research → positioning → GTM → enablement → launch

---

## ✨ Features

- **📋 Structured templates** — CommDoc, GTM Plan, Narrative Playbook, Sales Enablement, and more
- **🤖 AI-native slash commands** — Let AI assistants generate, update, and refine documents
- **🔄 Workflow orchestration** — Guided step-by-step process from research to launch
- **⚡️ Fast scaffolding** — Initialize a new PMM project in seconds
- **🔍 Dependency checking** — Never run commands out of order
- **📦 Git-first** — Every project is a Git repo by default

---

## 🚀 Quick Start

### Installation

**Option 1: Using pip (recommended)**
```bash
git clone https://github.com/adroual/pmm-kit.git
cd pmm-kit
pip install -e .
```

**Option 2: Using uv (faster)**
```bash
git clone https://github.com/adroual/pmm-kit.git
cd pmm-kit
uv pip install -e .
```

**Option 3: Using pipx (isolated)**
```bash
git clone https://github.com/adroual/pmm-kit.git
cd pmm-kit
pipx install -e .
```

### Create Your First Project

```bash
pmm init "My Product Launch"
cd my-product-launch
```

### Open in Claude Code (or your AI IDE)

```bash
claude-code .
# or: cursor .
# or: open in Gemini, Copilot, etc.
```

### Start Building

Run slash commands to generate your PMM artifacts:

```bash
/pmm.constitution   # Define brand voice and strategy
/pmm.plan          # Create strategic plan
/pmm.tasks         # Generate actionable task list
/pmm.execute       # Execute tasks interactively
```

---

## 📚 CLI Commands

| Command | Description |
|---------|-------------|
| `pmm init "Project Name"` | Initialize a new PMM project workspace |
| `pmm check` | Check environment and dependencies |
| `pmm update` | Check for updates and install latest version |
| `pmm help` | Show detailed help and slash commands |

### `pmm init` Options

```bash
pmm init "Project Name" [OPTIONS]

Options:
  --id ID          Custom project ID/slug
  --ai PROVIDER    AI provider (claude, gemini, copilot, cursor, openai)
  --here           Use current directory instead of creating new folder
  --no-git         Skip git initialization
  --force          Initialize in non-empty directory
```

**Examples:**
```bash
# Basic init
pmm init "Tap to Pay Launch"

# Custom ID and AI provider
pmm init "New Feature" --id my-feature --ai claude

# Use current directory
pmm init "Project" --here --no-git
```

---

## 🎨 Slash Commands

Slash commands are AI instructions that Claude/Gemini/Cursor can execute inside your project. They're automatically available in the `.claude/commands/` directory of every project.

### Workflow Orchestration (NEW)

| Command | Output File | Description |
|---------|-------------|-------------|
| `/pmm.plan` | `pmm-plan.md` | Create strategic plan with launch scope, channel strategy, success criteria |
| `/pmm.tasks` | `pmm-tasks.md` | Generate phased task list (Discovery → Foundation → GTM → Enablement → Launch) |
| `/pmm.execute` | — | Interactive orchestrator that walks through tasks, checks dependencies, tracks progress |

### Core Documents

| Command | Output File | Description |
|---------|-------------|-------------|
| `/pmm.constitution` | `pmm-constitution.md` | Define brand voice, strategic priorities, markets, PMM frameworks |
| `/pmm.research` | `research-dossier.md` | Synthesize research into insights, jobs-to-be-done, competitive landscape |
| `/pmm.commdoc` | `commdoc.md` | Create comprehensive launch CommDoc with positioning, messaging, GTM strategy |
| `/pmm.gtm` | `gtm-plan.md` | Generate GTM plan with channel strategy, plays, metrics |
| `/pmm.narrative` | `narrative-playbook.md` | Build narrative playbook with story arc, hooks, soundbites |

### Enablement & Launch

| Command | Output File | Description |
|---------|-------------|-------------|
| `/pmm.sales-playbook` | `sales-playbook.md` | Create sales battlecard with pitches, objection handling, competitive talk tracks |
| `/pmm.sales-enablement` | `sales-enablement.md` | Generate sales enablement brief with training plan, assets, feedback loop |
| `/pmm.changelog` | `changelog.md` | Produce customer-friendly changelog entries |
| `/pmm.success-report` | `success-report.md` | Post-launch retrospective with results, insights, recommendations |

---

## 🔄 Workflows

PMM-Kit supports two workflows:

### Workflow 1: Guided Orchestration (Recommended)

Perfect for new users or complex launches. The system guides you step-by-step:

```bash
# In your project directory with Claude Code open:
/pmm.constitution    # Step 1: Establish brand voice
/pmm.plan           # Step 2: Create strategic plan
/pmm.tasks          # Step 3: Generate task list
/pmm.execute        # Step 4: Execute interactively
```

The `/pmm.execute` command will:
- Walk through tasks phase by phase
- Run slash commands automatically (e.g., `/pmm.research`, `/pmm.commdoc`)
- Check prerequisites before executing
- Track progress in `pmm-tasks.md`
- Allow you to skip, pause, or customize

### Workflow 2: Manual Execution (Advanced)

Run commands in your preferred order:

```bash
/pmm.constitution
/pmm.research
/pmm.commdoc
/pmm.gtm
/pmm.narrative
/pmm.sales-playbook
/pmm.sales-enablement
/pmm.changelog
/pmm.success-report
```

---

## 📁 Project Structure

After running `pmm init`, your project contains:

```
my-project/
├── project.yaml              # Project metadata
├── pmm-plan.md              # Strategic plan
├── pmm-tasks.md             # Task list with checkboxes
├── pmm-constitution.md      # Brand voice & guidelines
├── research-dossier.md      # Research synthesis
├── commdoc.md               # Launch CommDoc
├── gtm-plan.md              # GTM plan
├── narrative-playbook.md    # Narrative playbook
├── sales-playbook.md        # Sales battlecard
├── sales-enablement.md      # Sales enablement
├── success-report.md        # Post-launch report
├── changelog.md             # Customer changelog
├── input/
│   ├── notes.md            # Raw notes
│   ├── research.md         # Research inputs
│   └── competitors.md      # Competitive analysis
├── .claude/
│   └── commands/           # Slash commands (auto-copied)
├── .git/                    # Git repository
└── .gitignore
```

---

## 🔄 Updating

Check for updates and install the latest version:

```bash
pmm update
```

For editable installs (recommended for development):
- Automatically runs `git pull` to get latest changes
- Updates take effect immediately

For regular installs:
- Provides instructions for pip/pipx/uv

---

## 🎯 Example: Full Launch Workflow

```bash
# 1. Create project
pmm init "Q1 Feature Launch"
cd q1-feature-launch

# 2. Open in Claude Code
claude-code .

# 3. In Claude Code, run:
/pmm.constitution

# 4. Add your research notes to input/
# Edit: input/notes.md, input/research.md, input/competitors.md

# 5. Follow guided workflow
/pmm.plan
/pmm.tasks
/pmm.execute

# 6. The orchestrator will guide you through:
#    → Discovery & Research
#    → Foundation & Positioning
#    → GTM Strategy & Planning
#    → Enablement & Execution
#    → Launch & Measurement

# 7. All done! You now have:
#    ✓ CommDoc
#    ✓ GTM Plan
#    ✓ Narrative Playbook
#    ✓ Sales Enablement
#    ✓ Success Report
```

---

## 🤝 Contributing

PMM-Kit is an open-source project. Contributions are welcome!

**For developers:**
- See `CLAUDE.md` for architecture and development guidance
- Memory prompts are in `memory/*.md`
- Templates are in `config/templates/*.template.md`

**To contribute:**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

Inspired by:
- [Spec-Kit](https://github.com/anthropics/spec-kit) by Anthropic
- [Claude Code](https://claude.com/code)
- The Product Marketing community

---

## 📧 Support

- **Issues:** [GitHub Issues](https://github.com/adroual/pmm-kit/issues)
- **Discussions:** [GitHub Discussions](https://github.com/adroual/pmm-kit/discussions)

---

**Built with ❤️ for Product Marketing Managers**
