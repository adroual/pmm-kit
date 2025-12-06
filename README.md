# PMM-Kit

## ⭐ Spec-Driven Product Marketing for the AI Era

Product Marketing operates at the intersection of strategy, storytelling, product, and go-to-market execution.  
Yet most of the tools we rely on were never designed for the depth, rigor, or cross-functional alignment our work requires.

**PMM-Kit brings Product Marketing into the modern era** — giving PMMs the same clarity, structure, and operational discipline that engineering teams have enjoyed for years, with AI woven directly into the workflow.

It replaces scattered docs, inconsistent templates, and ad-hoc processes with a **unified, spec-driven system** where research, strategy, positioning, GTM plans, narratives, enablement, and retrospectives all live within a clean, predictable structure.

The experience is:

- More focused  
- More organized  
- More scalable  
- Dramatically more efficient  

And the impact?

- **Faster alignment** with Product, Sales, and Leadership  
- **Clearer communication** across the entire organization  
- **Higher-quality launches** that feel crafted, not rushed  
- **Stronger cross-functional influence** through rigor and repeatability  

All powered by the precision of a spec-driven workflow and the acceleration of AI.

---

## 🎯 What is PMM-Kit?

PMM-Kit is a **CLI-first operating system for Product Marketing** — a technical workspace that turns PMM work into a structured, repeatable, AI-accelerated craft.

It allows PMMs to plan, write, refine, and maintain every strategic document involved in a launch using simple commands, clean templates, and intelligent automation.  
Everything lives in Markdown. Everything is versioned in Git. Everything follows a consistent, high-quality framework.

It feels like a developer tool.  
But it’s built entirely for Product Marketing.

PMM-Kit gives you:

- **A disciplined workflow** that mirrors how engineers manage specs and ship features  
- **A unified structure** across all PMM deliverables  
- **A repeatable process** you can trust across products and launches  
- **A scalable system** that grows with your team and your company  

With PMM-Kit you can:

- Spin up a complete PMM project in seconds  
- Generate production-ready documents with AI  
- Follow structured frameworks grounded in real PMM best practices  
- Iterate confidently with full version history  
- Bring consistency and excellence to every launch  

PMM-Kit isn’t another AI writing helper.  
**It’s the foundation for a more rigorous, predictable, and influential Product Marketing function — built for teams who want to operate at an elite level.**

---

## ✨ Features

- **📋 Structured templates** — CommDoc, GTM Plan, Narrative Playbook, Sales Enablement, and more
- **🤖 AI-native slash commands** — Let AI assistants generate, update, and refine documents
- **🔄 Workflow orchestration** — Guided step-by-step process from research to launch
- **⚡️ Fast scaffolding** — Initialize a new PMM project in seconds
- **🔍 Dependency checking** — Never run commands out of order
- **📦 Git-first** — Every project is a Git repo by default

---

## ⚡ Get Started

### 1. Install PMM-Kit CLI

Choose your preferred installation method:

#### Option 1: Persistent Installation (Recommended)

Install once and use everywhere:

```bash
uv tool install pmm-kit --from git+https://github.com/adroual/pmm-kit.git
```

Then use the tool directly:

```bash
# Create new project
pmm init "My Product Launch"

# Or initialize in existing directory
pmm init . --ai claude
# or
pmm init --here --ai claude

# Check environment
pmm check

# Update to latest version
pmm update
```

To upgrade PMM-Kit:

```bash
uv tool install pmm-kit --force --from git+https://github.com/adroual/pmm-kit.git
```

#### Option 2: One-time Usage

Run directly without installing:

```bash
uvx --from git+https://github.com/adroual/pmm-kit.git pmm init "My Product Launch"
```

**Benefits of persistent installation:**
- Tool stays installed and available in PATH
- No need to create shell aliases
- Better tool management with `uv tool list`, `uv tool upgrade`, `uv tool uninstall`
- Cleaner shell configuration
- Automatic updates with `pmm update`

---

### 2. Establish brand voice and strategy

Launch your AI assistant in the project directory. The `/pmm.*` commands are available in the assistant.

Use the `/pmm.constitution` command to create your project's governing principles, brand voice, strategic priorities, and PMM frameworks.

```bash
/pmm.constitution
```

Create principles focused on brand tone, target audience, strategic priorities (Revenue, Acquisition, Retention), markets, and preferred PMM frameworks.

---

### 3. Create strategic plan

Use the `/pmm.plan` command to establish your launch scope, research approach, positioning strategy, channel strategy, and success criteria.

```bash
/pmm.plan
```

Define launch type, timeline, key milestones, target channels, primary business objective, known risks, and research status.

---

### 4. Generate actionable task list

Use `/pmm.tasks` to create a phased, actionable task list derived from your strategic plan.

```bash
/pmm.tasks
```

This creates a step-by-step checklist across five phases:
- **Phase 1:** Discovery & Research
- **Phase 2:** Foundation & Positioning
- **Phase 3:** GTM Strategy & Planning
- **Phase 4:** Enablement & Execution
- **Phase 5:** Launch & Measurement

---

### 5. Execute your launch workflow

Use `/pmm.execute` to walk through tasks interactively, with automatic dependency checking and progress tracking.

```bash
/pmm.execute
```

The orchestrator will:
- Guide you through each phase step-by-step
- Run appropriate slash commands automatically
- Check prerequisites before executing
- Track progress in `pmm-tasks.md`
- Allow you to skip, pause, or customize

Alternatively, run commands manually:

```bash
/pmm.research         # Synthesize research insights
/pmm.commdoc          # Create launch CommDoc
/pmm.gtm              # Generate GTM plan
/pmm.narrative        # Build narrative playbook
/pmm.sales-playbook   # Create sales battlecard
/pmm.sales-enablement # Generate sales enablement
/pmm.changelog        # Customer-facing changelog
/pmm.success-report   # Post-launch retrospective
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

### Quick Update

Check for updates and install the latest version:

```bash
pmm update
```

### Manual Update Methods

**For persistent installations (recommended):**

```bash
uv tool install pmm-kit --force --from git+https://github.com/adroual/pmm-kit.git
```

**For editable/development installs:**

```bash
cd /path/to/pmm-kit
git pull
# Changes take effect immediately (no reinstall needed)
```

**Check your installation method:**

```bash
uv tool list  # Shows if installed via uv tool
which pmm     # Shows location of pmm binary
```

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
- The Product Marketing community

---

## 📧 Support

- **Issues:** [GitHub Issues](https://github.com/adroual/pmm-kit/issues)
- **Discussions:** [GitHub Discussions](https://github.com/adroual/pmm-kit/discussions)

---

**Built with ❤️ for Product Marketing Managers**
