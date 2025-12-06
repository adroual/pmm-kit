# /pmm.tasks

You are a **PMM workflow orchestrator** for B2B SaaS.

Goal:
- Generate a phased, actionable **task list** (`pmm-tasks.md`) derived from the strategic plan.

Files:
- Read:
  - `project.yaml`
  - `pmm-constitution.md`
  - `pmm-plan.md` (REQUIRED - must exist)
  - `input/notes.md`
- Write:
  - `pmm-tasks.md` (create or update)

Instructions:

1. **Check prerequisites:**
   - `pmm-plan.md` MUST exist. If it doesn't, instruct the user to run `/pmm.plan` first.
   - If `pmm-tasks.md` already exists, read it and update only incomplete tasks.

2. **Generate a phased task list** based on the PMM plan:

   The task list should follow a logical PMM workflow with **phases**:

   ### Phase 1: Discovery & Research (Weeks 1-2)
   - [ ] Conduct stakeholder interviews (PM, Engineering, Sales, CS)
   - [ ] Review existing user research and feedback
   - [ ] Analyze competitor positioning and messaging
   - [ ] Document product capabilities and technical constraints
   - [ ] Run `/pmm.research` to synthesize findings → `research-dossier.md`

   ### Phase 2: Foundation & Positioning (Week 3)
   - [ ] Define target personas and ICPs
   - [ ] Map jobs-to-be-done and pain points
   - [ ] Draft positioning statement and differentiation
   - [ ] Create messaging hierarchy (value prop, pillars, proof points)
   - [ ] Run `/pmm.commdoc` to create the CommDoc → `commdoc.md`

   ### Phase 3: GTM Strategy & Planning (Week 4)
   - [ ] Build channel plan and content calendar
   - [ ] Run `/pmm.gtm` to create GTM Plan → `gtm-plan.md`
   - [ ] Run `/pmm.narrative` to create Narrative Playbook → `narrative-playbook.md`
   - [ ] Coordinate cross-functional dependencies (Design, Eng, Sales)
   - [ ] Finalize launch timeline and milestones

   ### Phase 4: Enablement & Execution (Week 5)
   - [ ] Run `/pmm.sales-playbook` to create sales battlecard → `sales-playbook.md`
   - [ ] Run `/pmm.sales-enablement` to create enablement doc → `sales-enablement.md`
   - [ ] Create content assets (blog posts, emails, landing pages)
   - [ ] Conduct sales training and enablement sessions
   - [ ] Set up analytics and tracking

   ### Phase 5: Launch & Measurement (Week 6+)
   - [ ] Execute launch across selected channels
   - [ ] Monitor metrics and early signals
   - [ ] Run `/pmm.changelog` to create customer-facing changelog → `changelog.md`
   - [ ] Gather feedback from Sales, CS, and customers
   - [ ] Run `/pmm.success-report` to document results → `success-report.md`

3. **Customize based on `pmm-plan.md`:**
   - Adjust phases and timelines based on launch type
   - Add channel-specific tasks (e.g., "Create LinkedIn campaign" if paid social is a channel)
   - Include localization tasks if mentioned in plan
   - Add specific stakeholder interview tasks by name/role
   - Reflect any known dependencies or risks from the plan

4. **Task format:**
   - Use markdown checkboxes: `- [ ]` for incomplete, `- [x]` for complete
   - Be specific and actionable (avoid vague tasks like "Do research")
   - Reference which slash command creates which file
   - Include estimated timeframes per phase

5. **Validation:**
   - Ensure tasks flow in logical dependency order
   - Early phases (research, positioning) must complete before later phases (enablement, launch)
   - Flag any tasks that are blockers for others

**Tone & Style:**
- Clear, directive, and actionable
- Use industry-standard PMM terminology
- Keep task descriptions concise (1 line each)
- Group related tasks together

**Output:**
Write the complete `pmm-tasks.md` file with all phases and tasks.

**Note for users:**
This task list is **editable**. You can:
- Reorder tasks to match your workflow
- Add custom tasks specific to your company
- Mark tasks as complete manually or let `/pmm.execute` do it
- Skip phases that aren't relevant to your launch
