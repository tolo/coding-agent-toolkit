---
description: Creates a Feature Implementation Specification from template
argument-hint: <description> | --issue <number>
---

# Generate Feature Implementation Specification

Given a feature request, generate a Feature Implementation Specification (FIS) using the template in the **Appendix** below.


## Variables

ARGUMENTS: $ARGUMENTS


## Usage

```
/spec-create <feature description>        # Create FIS from inline description
/spec-create --issue 123                  # Create FIS from GitHub issue
/spec-create @docs/requirements.md        # Create FIS from requirements file
```


## Instructions

- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section in CLAUDE.md before starting work, including but not limited to:
  - **Foundational Rules and Guardrails**
  - **Foundational Development Guidelines and Standards** (e.g. Development, Architecture, UI/UX Guidelines etc.)
- **Spec generation only** - No code changes, commits, or modifications during execution of this command
- **Remember**: Agents executing the FIS only get the context you provide. Include all necessary documentation, examples, and references.


## Workflow

### 0. Parse Input & Get Requirements

**If `--issue` flag present (or if ARGUMENTS contain description that refers to GitHub issue(s)):**
1. Extract issue number(s) from ARGUMENTS
2. Use `gh issue view <number>` to fetch issue details (title, body, labels, comments)
3. Use issue content as the feature request
4. Store issue number for reference in generated FIS

**Otherwise:**
- Use inline description or file reference from ARGUMENTS as the feature request


### 1. Priming and Project Understanding
- Analyse the codebase to properly understand the project structure, relevant files and similar patterns
   - Use commands like `tree -d` and `git ls-files | head -250` to get overview of codebase structure
   - For complex codebase exploration, consider using the Explore agent


### 2. Feature Research and Design

#### Analyze Requirements
- Fully understand the feature request and requirements
- If from GitHub issue: include issue number reference, labels, and any relevant discussion from comments
- Note any provided documentation, examples, or constraints
- **Read additional guidelines and documentation** - Read additional relevant guidelines and documentation (API, guides, reference, etc.) as needed

#### Deep Research Process
- Use **parallel sub-agents (foreground, i.e. `run_in_background=false`)** for research tasks - multiple Task calls in one message.
- Save findings to _`<project_root>/docs/temp/research/{feature-name}/`_ **only** if substantial, and add links to generated FIS. Note: If only a file/URL is needed, do not create a research file, just add the reference.

##### 1. Codebase Research:
- Search codebase for relevant files and similar patterns
   - Use command like `tree -d` and `git ls-files | head -250` to get an overview of the codebase structure
- Similar features/patterns in the codebase
- Files to reference with exact line numbers
- Existing conventions and test patterns
- Existing patterns and architecture
- Recommended agents to use: `cc-workflows:research-specialist`, `cc-workflows:solution-architect`

##### 2. External Research:
If _`FEATURE_REQUEST`_ includes references to research already conducted, then use those as your primary research sources.

_Otherwise - if no such references are present_ - perform external research:
    - Search for similar features/patterns online
    - Library/framework documentation (include specific URLs)
    - Implementation examples (GitHub/StackOverflow/blogs)
    - UI inspiration
    - Best practices and common pitfalls
    - General explorative and deep web research
    - Recommended agents to use: `cc-workflows:research-specialist`, `cc-workflows:solution-architect`, `cc-workflows:ui-ux-designer`

##### 3. Research Multiple Architectural Approaches and Trade-offs
If _`FEATURE_REQUEST`_ includes a reference to an ADR or other architecture decision document, the simply use that as the architecture.

_Otherwise - if no such reference is present_ - perform architecture research:
    - Analyze 1-3 different approaches with trade-offs
    - Consider the trade-offs of different approaches 
    - Evaluate implementation complexity, performance implications etc
    - Document potential risks and mitigation strategies
    - Create architecture diagrams (when needed)
    - Recommended agents to use: `cc-workflows:solution-architect`

##### 4. UI Designs Research (when applicable)
If _`FEATURE_REQUEST`_ includes references to UI research already conducted, then use those as your primary research sources.

_Otherwise - if no such references are present_ - perform UI research:
    - Explore existing UI patterns and components
    - Download appropriate design inspiration assets
    - Gather inspiration from design systems and libraries
    - Create UI wireframes, mockups and sketches
    - Create and describe UI flows
    - Recommended agents to use: `cc-workflows:ui-ux-designer`
        - When novel UI ideas are needed: `cc-workflows:whimsy-injector`

#### User Clarification
Ask ONLY if implementation is blocked by ambiguity.


### 3. Generate FIS
**IMPORTANT**: Use `cc-workflows:solution-architect` to create the FIS.

#### Gather Context (as references, not inline content)
- Research docs from previous phase (link to files in `docs/temp/research/`)
- ADRs and architecture docs
- File paths with line numbers for patterns to follow
- UI wireframes/mockups (required for UI tasks)
- Design system references (required for UI tasks)
- External documentation URLs with specific sections

#### Generate from Template
**USE THE TEMPLATE**: Generate the FIS using the template in the **Appendix** below as your structure.

#### Key Generation Guidelines
1. Each task: atomic, self-contained, with file:line references
2. Mark parallelizable tasks with [P]
3. Reference patterns, don't reproduce them
4. Stay within 300-500 line target


### 4. Quality Validation

#### Plan Review
Use the `/cc-workflows:review-plan` command (**important**: run this as in a separate sub-agent) to review the generated implementation plan for completeness, correctness, requirements coverage, edge cases, redundant aspects, etc.
- Use the generated FIS as input.
- After review-plan command completes, read the output (generated review report) carefully.
- Address **all** issues identified during review and improve/update the FIS accordingly.

#### Confidence Check
Rate your FIS 1-10 for single-pass implementation success:
- **9-10**: All context present, clear decisions, validation automated
- **7-8**: Good detail, minor clarifications might be needed
- **<7**: Missing context, unclear architecture, needs revision

**If score <8**: Revise or ask for user clarification.

#### Final Checklist
- [ ] FIS follows template structure exactly
- [ ] Validation task use different agents than implementation
- [ ] Context includes specific file:line references
- [ ] ADR clearly explains the decision


## Output
Save FIS as: _`<project_root>/docs/specs/{feature-name}.md`_
- If from GitHub issue: include issue reference in filename, e.g. `issue-123-feature-name.md`

**Remember**: The FIS should be executable with minimal orchestration. All complexity and detail belongs in the FIS itself, not the execution command.


---


## Appendix: FIS Template

Use the template below to generate the Feature Implementation Specification.

<spec-template>
# Feature Implementation Specification Template

> **Purpose:**
> Executable specification optimized for AI agents — concise, actionable, reference-heavy.
>
> **Core Principles:**
> 1. **References over Content**: Link to docs, code (file:line), and research — don't inline them
> 2. **Decisions, not Explanations**: State what to do, not lengthy rationale
> 3. **Patterns by Reference**: Point to existing code patterns (file:line) rather than reproducing them
> 4. **Validation at Execution**: Code is written during spec-execute, not spec-create
> 5. **Information Dense**: Keywords and patterns from the codebase, minimal prose
> 6. **Delegate**: Sub-agents do the work; main agent orchestrates
>
> **Size Constraint:**
> - Target: **300-500 lines** max for most features
> - If exceeding 500 lines, split into multiple specs or extract shared content to referenced files
>
> **DON'Ts**
> - ❌ Code snippets longer than 5-10 lines — reference existing patterns instead
> - ❌ Inline documentation excerpts — link to the source
> - ❌ Verbose prose or explanations — be terse and actionable
> - ❌ Repeating information available elsewhere — reference it
> - ❌ Over-engineering or out-of-scope functionality



## Feature Overview and Goal
{{Clear description of what needs to be built and why}}


## Success Criteria
- [ ] {{Specific measurable outcome}}
- [ ] {{User-visible behavior}}
- [ ] {{Technical requirement}}
- [ ] {{Performance/scaling requirement}}


## Scope & Boundaries

### In Scope
- ✅ {{Core functionality to be built}}
- ✅ {{Integration points to be created}}
- ✅ {{User interactions to be enabled}}

### What We're NOT Doing
- ❌ {{Out of scope item - be specific}}
- ❌ {{Feature explicitly not included}}
- ❌ {{Existing functionality not to be modified}}

### Anti-Patterns to Avoid
- ❌ Don't {{common mistake}} - instead {{correct approach}}
- ❌ Don't {{framework misuse}} - use {{proper pattern}}
- ❌ Don't {{reinvent wheel}} - use existing {{utility/pattern}}


## Solution Architecture and Design

### Architecture Decision Record (ADR)
{{Links to relevant ADRs / _OR_ include details inline below (Decision, Rationale, Alternatives Considered)}}

#### Decision
**We will**: {{Chosen approach}}

#### Rationale
{{Why this approach best solves the problem given constraints}}

#### Alternatives Considered
1. **{{Alternative 1}}**: {{Brief description}}
- ❌ Rejected because: {{Specific reason}}
2. **{{Alternative 2}}**: {{Brief description}}
- ❌ Rejected because: {{Specific reason}}

### Technical Overview

#### Outline of New/Changed Files
```bash
# Show where new files/modules will be added or updated
{{Illustrate the changes with annotations}}
```

#### UI/UX Design (if applicable)
{{Describe any UI/UX changes, including new screens, UI components, interactions, or user flows}}

#### UI Mockups/Wireframes (if applicable)
{{Include links to existing wireframes and/or simple mockups/sketches in Markdown / Ascii format}}


#### Data Models & Structures (if applicable)
{{Describe new or modified data models, including fields and types etc}}
```
# Data model pseudocode
```

#### Integration Points (if applicable)
{{Describe how this integrates with existing systems or APIs}}


## Critical Documentation & Context

### Documentation & References
```
# Reference format: type | path/url | section | why needed
file   | src/components/Modal.tsx:45-78    | Pattern for dialog handling
file   | src/api/users.ts:12-34            | API structure to follow
url    | https://docs.example.com/auth     | OAuth flow reference
doc    | docs/architecture/adr-001.md      | Auth architecture decision
wire   | docs/specs/wireframes/login.html  | UI layout for login screen
```
> Keep this list focused — only include references that are essential for implementation.


### Known Constraints & Gotchas
- **Constraint**: {{Known limitation}} - Workaround: {{Specific solution}}
- **Gotcha**: {{Common mistake}} - Avoid by: {{Best practice}}
- **Critical**: {{Framework/library limitation}} - Must handle by: {{Specific approach}}


## Implementation Plan
Below is an overview of the tasks that make up the implementation plan.
**IMPORTANT:**
- Each task is self-contained with all context needed, for independent execution
- Check off task checkboxes (- [ ] → - [x]) as tasks are completed
- Tasks that can be safely executed in parallel using sub-agents will be marked with a [P].

### List of implementation tasks to be completed and the order in which they should be completed

_Examples:_
- [ ] **TI01** Initialize Fresh project structure in repository root
  - Create deno.json with Fresh dependencies and tasks
  - Set up basic routes/, islands/, components/, lib/ directories
  - Configure import maps and TypeScript settings

- [ ] **TI02** Configure Supabase integration and environment
  - Create .env.example and .env files with Supabase credentials
  - Set up lib/supabase/client.ts and lib/supabase/server.ts
  - Configure database connection and authentication helpers

- [ ] **TI03** [P] Set up development tooling and scripts
  - Configure deno fmt, deno lint, and deno check tasks
  - Set up Playwright for E2E testing in tests/e2e/
  - Create development and deployment scripts

- [ ] **TI04** [P] Integrate design system foundation
  - Add Pico CSS CDN link and Google Fonts (Nunito Sans, Outfit)
  - Create static/styles/architecture-theme.css with custom variables
  - Set up responsive design system per ADR-002

#### Implementation Notes (per task, only when needed)
- Reference existing patterns: `see src/components/Modal.tsx:45-78 for similar pattern`
- Only include pseudocode (max 5-10 lines) when no existing pattern exists in codebase
- Configuration/data models: describe structure briefly, don't write full schemas

### Validation Tasks
> Validation methodology details (agents, checks) defined in spec-execute.

- [ ] **TV01** [P] Level 1: Code review and analysis
- [ ] **TV02** [P] Level 2: Unit, integration, E2E testing
- [ ] **TV03** [P] Level 3: Visual validation _(if UI applicable)_
- [ ] **TV04** Address validation issues, verify *Final Validation Checklist*

### Feature-Specific Validation (if any)
{{Only add requirements not covered by standard validation levels}}


## Final Validation Checklist

### Feature Validation
- [ ] **All success criteria** from the top-level "Success Criteria" section met
- [ ] **All tasks** in the implementation plan are _fully completed_ (not partially) and the completion is _reviewed, verified checkboxes checked_
- [ ] **No regressions** or breaking changes introduced
- [ ] **UI verified** to match requirements (if applicable)

### Technical Validation
- [ ] **All validation levels** completed successfully
- [ ] Code **builds / compiles** and **all** tests pass without errors
- [ ] **No** analysis, linting/type errors or critical code style issues
- [ ] Code follows existing codebase patterns, naming conventions and stuctures
- [ ] **All** temporary, refactored, migrated or obsolete code/files removed and cleaned up
- [ ] No commented-out code left behind
</spec-template>
