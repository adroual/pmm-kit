# /pmm.scaffold — Scaffold a PMM project in Notion

Create all PMM artifact pages from database templates and wire them into the PMM Kit project config. Workspace-agnostic — works against any Notion database by discovering schema and templates dynamically.

## Prerequisites

- Notion MCP connection is active (run `/mcp` to verify)
- The user has a Notion database for PMM artifacts with templates
- The database is shared with the Notion integration

## Workflow

### First Run (no saved mapping)

1. Ask the user for:
   - **Project name** (e.g., "Tap to Pay Spain Launch")
   - **PMM artifacts database URL**

2. Extract the database ID from the URL

3. **Discover the database schema via MCP:**
   - Read all properties (name, type, options)
   - Read all available templates
   - Show the user what was found

4. **Interactive mapping — ask the user to match templates to spec types:**
   ```
   Found 3 templates in your database:
     1. "CommDoc"
     2. "Narrative Playbook"
     3. "GTM Package v2"

   PMM Kit spec types to map:
     - commdoc → which template? [1]
     - narrative → which template? [2]
     - gtm-package → which template? [3]
   ```

5. **Interactive property mapping — classify ALL database properties:**

   For every property in the database schema, determine its role. Group them into:

   - **Auto-filled on creation** — properties the scaffold command fills automatically:
     - Title property → set to `[Template Name] — [Project Name]`
     - Status property → set to a default value (ask which)
     - Template Type → set to match the template being used
     - Last Updated / date properties → set to today's date

   - **Prompted per project** — properties the user must provide a value for each time:
     - Market / region selects
     - Quarter / timeline selects
     - Priority selects
     - OKR / objective multi-selects
     - Product/Feature text
     - Launch Date

   - **Skipped** — properties that don't apply at creation time:
     - Owner (person) — usually assigned later
     - Computed / formula properties

   Ask the user to confirm the classification. Save it so subsequent runs know which properties to prompt for and which to auto-fill.

   ```
   Found these properties:
     - Name (title) → auto: "[Template] — [Project Name]"
     - Template Type (select) → auto: matches template
     - Status (status) → auto: "In Progress"
     - Last Updated (date) → auto: today
     - Markets (multi_select) → prompt: ask per project
     - Quarter (select) → prompt: ask per project
     - Priority (select) → prompt: ask per project
     - Company OKRs (multi_select) → prompt: ask per project
     - Product/Feature (text) → prompt: ask per project
     - Launch Date (date) → prompt: ask per project
     - Owner (person) → skip

   Does this look right? [Y/n]
   ```

6. **Save the full mapping** in `config/notion.yaml`:
   ```yaml
   notion:
     database_url: "https://www.notion.so/team/PMM-Artifacts-xyz..."
     database_id: "abc123..."
     data_source_id: "def456..."
     template_mapping:
       commdoc:
         name: "[CommDoc]"
         template_id: "..."
       narrative:
         name: "[Narrative Playbook]"
         template_id: "..."
       gtm-package:
         name: "[GTM Package v2]"
         template_id: "..."
     property_mapping:
       auto:
         project_name: "Name"
         template_type: "Template Type"
         status: "Status"
         last_updated: "Last Updated"
         default_status: "In Progress"
       prompt:
         - property: "Markets"
           type: "multi_select"
           options: ["FR", "DE", "IT", "ES", "NL"]
         - property: "Quarter"
           type: "select"
           options: ["Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026"]
         - property: "Priority"
           type: "select"
           options: ["Low", "Medium", "High", "Critical"]
         - property: "Company OKRs"
           type: "multi_select"
           options: ["Accelerate Revenue Growth", "Expand Market Share", "Drive Product Adoption", "Increase Customer Retention", "Strengthen Brand Awareness"]
         - property: "Product/Feature"
           type: "text"
         - property: "Launch Date"
           type: "date"
       skip:
         - "Owner"
   ```

### Subsequent Runs (mapping exists)

1. Read saved mapping from `config/notion.yaml`

2. Ask for **project name**

3. **Prompt for every property classified as `prompt`:**
   - For `select` / `multi_select`: show the saved options as choices
   - For `text`: ask for free-text input
   - For `date`: ask for a date value
   - The user can skip any property by leaving it blank

4. For each mapped template:
   a. Create a new page in the database from the template
   b. Set title: `[Template Name] — [Project Name]`
   c. Set ALL auto-filled properties (status, template type, last updated)
   d. Set ALL prompted properties with the values the user provided
   e. Capture the created page URL

5. **Every property should be filled.** The database entries must be clean — no blank cells for properties that have values.

6. Write the URLs into the project config:
   ```yaml
   outputs:
     commdoc:
       format: notion
       notion_url: "<captured URL>"
     narrative:
       format: notion
       notion_url: "<captured URL>"
     gtm-package:
       format: notion
       notion_url: "<captured URL>"
   ```

7. Confirm to the user:
   - List the created pages with clickable URLs
   - Show all property values that were set
   - Show the updated config
   - Suggest next step: run `/pmm.commdoc` to start filling in content

## Re-mapping

If the database structure changes or the user switches workspaces:
```
/pmm.scaffold --remap    # Re-run the interactive mapping flow
```

## Important Rules

- **Fill all properties.** Every database property that has a value should be set on creation. No blank cells in the database view.
- **Zero assumptions about database structure.** Never hardcode template names, property names, or property types. Always discover via MCP.
- **Don't duplicate.** Before creating, search the database for existing pages with the same project name. If found, ask the user whether to reuse or create new.
- **Graceful degradation.** If a mapped property doesn't exist in a new workspace, warn the user and skip it rather than failing.
- **Template instantiation fallback.** If MCP doesn't support creating pages from a specific template, create a blank page in the database with the right properties and warn the user to apply the template manually in Notion. The URLs are still captured and wired into config regardless.

## Usage

```
/pmm.scaffold                              # Interactive — asks for all inputs
/pmm.scaffold "Tap to Pay Spain Launch"    # Pre-fills the project name
/pmm.scaffold --remap                      # Re-run template and property mapping
```
