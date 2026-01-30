---
description: Creates a Feature Implementation Specification from template (simple, no sub-agents)
argument-hint: [Short description of the feature request, or reference to file]
---

# Generate Feature Implementation Specification (Simple)

Given a feature request, generate a Feature Implementation Specification (FIS) using the template in the **Appendix** below.


## Variables
FEATURE_REQUEST: $ARGUMENTS


## Instructions

- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section as defined in AGENTS.md, etc. before starting work, including but not limited to:
  - **Foundational Rules and Guardrails**
  - **Foundational Development Guidelines and Standards** (e.g. Development, Architecture, UI/UX Guidelines etc.)
- No sub-agents - direct research and generation approach
- **Favor simplicity** - recommend simplest solution (KISS, YAGNI, DRY)
- **Conciseness** - be brief without losing meaning
**Remember**: The FIS must be self-contained with all context needed for implementation.


## Workflow

### Phase 1: Project Understanding
- Analyse the codebase to properly understand the project structure, relevant files and similar patterns
   - Use commands like `tree -d` and `git ls-files | head -250` to get overview of codebase structure
   - For complex codebase exploration, consider using Explore agent (if available)

**Gate**: Project context understood


### Phase 2: Feature Research and Design

#### Analyze Requirements
- Fully understand the feature request (_`FEATURE_REQUEST`_) and requirements
- Note any provided documentation, examples, or constraints
- **Read additional guidelines and documentation** - Read additional relevant guidelines and documentation (API, guides, reference, etc.) as needed

#### Codebase Research
- Search codebase for relevant files and similar patterns
- Identify files to reference with exact line numbers
- Document existing conventions and test patterns
- Note existing architecture patterns

#### External Research (as needed)
If _`FEATURE_REQUEST`_ includes references to research already conducted, then use those as your primary research sources.

_Otherwise - if no such references are present_ - perform external research:
    - Search for similar features/patterns online
    - Library/framework documentation (include specific URLs)
    - Implementation examples (GitHub/StackOverflow/blogs)
    - UI inspiration
    - Best practices and common pitfalls
    - General explorative and deep web research

#### Research Multiple Architectural Approaches and Trade-offs
If _`FEATURE_REQUEST`_ includes a reference to an ADR or other architecture decision document, the simply use that as the architecture.

_Otherwise - if no such reference is present_ - perform architecture research:
    - Analyze 1-3 different approaches with trade-offs
    - Consider the trade-offs of different approaches 
    - Evaluate implementation complexity, performance implications etc
    - Document potential risks and mitigation strategies
    - Create architecture diagrams (when needed)

#### UI Designs Research (when applicable)
If _`FEATURE_REQUEST`_ includes references to UI research already conducted, then use those as your primary research sources.

_Otherwise - if no such references are present_ - perform UI research:
    - Explore existing UI patterns and components
    - Download appropriate design inspiration assets
    - Gather inspiration from design systems and libraries
    - Create UI wireframes, mockups and sketches
    - Create and describe UI flows


#### User Clarification
Ask ONLY if implementation is blocked by ambiguity.

**Gate**: Research complete, approach determined


### Phase 3: Generate FIS

#### Gather Context (as references, not inline content)
- Research findings with links
- File paths with line numbers for patterns to follow
- UI wireframes/mockups (if applicable)
- ADRs and architecture docs
- External documentation URLs with specific sections

#### Generate from Template
**USE THE TEMPLATE**: Generate the FIS using the template in the **Appendix** below as your structure.

#### Key Generation Guidelines
1. Each task: atomic, self-contained, with file:line references
2. Reference patterns, don't reproduce them
3. Stay within 300-500 line target

**Gate**: FIS generated


### Phase 4: Quality Validation

#### Plan Review
Use the `/review-plan` command to review the generated implementation plan for completeness, correctness, requirements coverage, edge cases, redundant aspects, etc.
- Use the generated FIS as input.
- Read the output (generated review report) carefully.
- Address all identified issues and improve the FIS accordingly.

#### Confidence Check
Rate your FIS 1-10 for single-pass implementation success:
- **9-10**: All context present, clear decisions, validation defined
- **7-8**: Good detail, minor clarifications might be needed
- **<7**: Missing context, unclear architecture, needs revision

**If score <8**: Revise or ask for user clarification.

#### Final Checklist
- [ ] FIS follows template structure exactly
- [ ] Context includes specific file:line references
- [ ] ADR clearly explains the decision
- [ ] Validation strategy is actionable

**Gate**: FIS validated


### Phase 5: Output
Save FIS as: _`<project_root>/docs/specs/{feature-name}.md`_

**Remember**: The FIS should be executable with minimal orchestration. All complexity and detail belongs in the FIS itself, not the execution command.


---


## Appendix: FIS Template (Simple)

Use the template below to generate the Feature Implementation Specification.

<spec-template>
# Feature Implementation Specification Template (Simple)

> **Purpose:**
> Executable specification for direct AI agent implementation — concise, actionable, reference-heavy.
>
> **Core Principles:**
> 1. **References over Content**: Link to docs, code (file:line), and research — don't inline them
> 2. **Decisions, not Explanations**: State what to do, not lengthy rationale
> 3. **Patterns by Reference**: Point to existing code patterns (file:line) rather than reproducing them
> 4. **Information Dense**: Keywords and patterns from the codebase, minimal prose
> 5. **Fix-forward approach**: Address issues immediately
>
> **Size Constraint:**
> - Target: **300-500 lines** max for most features
> - If exceeding 500 lines, split into multiple specs or extract shared content to referenced files
>
> **DON'Ts**
> - Code snippets longer than 5-10 lines — reference existing patterns instead
> - Inline documentation excerpts — link to the source
> - Verbose prose or explanations — be terse and actionable
> - Repeating information available elsewhere — reference it
> - Over-engineering or out-of-scope functionality



## Feature Overview and Goal
{{Clear description of what needs to be built and why}}


## Success Criteria
- [ ] {{Specific measurable outcome}}
- [ ] {{User-visible behavior}}
- [ ] {{Technical requirement}}
- [ ] {{Performance/scaling requirement}}


## Scope & Boundaries

### In Scope
- {{Core functionality to be built}}
- {{Integration points to be created}}
- {{User interactions to be enabled}}

### What We're NOT Doing
- {{Out of scope item - be specific}}
- {{Feature explicitly not included}}
- {{Existing functionality not to be modified}}

### Anti-Patterns to Avoid
- Don't {{common mistake}} - instead {{correct approach}}
- Don't {{framework misuse}} - use {{proper pattern}}
- Don't {{reinvent wheel}} - use existing {{utility/pattern}}


## Solution Architecture and Design

### Architecture Decision Record (ADR)
{{Links to relevant ADRs / _OR_ include details inline below (Decision, Rationale, Alternatives Considered)}}

#### Decision
**We will**: {{Chosen approach}}

#### Rationale
{{Why this approach best solves the problem given constraints}}

#### Alternatives Considered
1. **{{Alternative 1}}**: {{Brief description}}
- Rejected because: {{Specific reason}}
2. **{{Alternative 2}}**: {{Brief description}}
- Rejected because: {{Specific reason}}

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
> Keep this list focused — only include references essential for implementation.


### Known Constraints & Gotchas
- **Constraint**: {{Known limitation}} - Workaround: {{Specific solution}}
- **Gotcha**: {{Common mistake}} - Avoid by: {{Best practice}}
- **Critical**: {{Framework/library limitation}} - Must handle by: {{Specific approach}}


## Implementation Plan
Below is an overview of the tasks that make up the implementation plan.
**IMPORTANT:**
- Each task is self-contained with all context needed
- Check off task checkboxes (- [ ] -> - [x]) as tasks are completed

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

- [ ] **TI03** Set up development tooling and scripts
  - Configure deno fmt, deno lint, and deno check tasks
  - Set up Playwright for E2E testing in tests/e2e/
  - Create development and deployment scripts

- [ ] **TI04** Integrate design system foundation
  - Add Pico CSS CDN link and Google Fonts (Nunito Sans, Outfit)
  - Create static/styles/architecture-theme.css with custom variables
  - Set up responsive design system per ADR-002

#### Implementation Notes (per task, only when needed)
- Reference existing patterns: `see src/components/Modal.tsx:45-78 for similar pattern`
- Only include pseudocode (max 5-10 lines) when no existing pattern exists in codebase
- Configuration/data models: describe structure briefly, don't write full schemas

### List of validation tasks to be completed

- [ ] **TV01** Run Level 1 commands of Validation Strategy: Code Review and Analysis
- [ ] **TV02** Run Level 2 commands of Validation Strategy: Testing (Unit, Integration, E2E)
- [ ] **TV03** Run Level 3 commands of Validation Strategy: Visual Validation (if applicable)
- [ ] **TV04** Address remaining issues and verify Final Validation Checklist
  - Address any defects, analysis/review feedback, and functionality gaps
  - Ensure *Final Validation Checklist* is complete
  - Execute any additional cleanup (files, unused code, etc.)


## Validation Strategy

### Level 1: Code Review and Analysis
Use the `code-review` skill (if available) to perform comprehensive review and analysis covering:

- Static analysis, linting, formatting and type checking issues
- Code quality (correctness, readability, best practices, performance, maintainability)
- Architecture (pattern adherence, ADR compliance, anti-pattern detection)
- Security (input validation, injection prevention, auth, data protection, OWASP Top 10)
- UI/UX (if applicable - visual quality, usability, accessibility)


### Level 2: Testing (Unit, Integration and E2E)

#### Unit Tests
- Update/create and run unit tests for the new feature
- Set up and run appropriate unit tests as per project guidelines (see CLAUDE.md)
- Verify all unit tests pass

#### System and Integration Tests (if applicable)
- Update/create and run integration tests for the new feature
- Verify all integration tests pass

#### UI/E2E Tests (if applicable)
- Update/create and run UI/E2E tests for the new feature
- Verify all UI/E2E tests pass


### Level 3: Visual Validation (if applicable)

- Verify updated UI works correctly according to specified requirements
- Follow any Visual Validation Protocols defined in project guidelines (see CLAUDE.md)
- Check for visual regressions and ensure UI matches design specs


## **IMPORTANT**: Final Validation Checklist

### Feature Validation
- [ ] **All success criteria** from the top-level "Success Criteria" section met
- [ ] **All tasks** in the implementation plan are _fully completed_ (not partially) and verified
- [ ] **No regressions** or breaking changes introduced
- [ ] **UI verified** to match requirements (if applicable)

### Technical Validation
- [ ] **All validation levels** completed successfully
- [ ] Code **builds / compiles** and **all** tests pass without errors
- [ ] **No** analysis, linting/type errors or critical code style issues
- [ ] Code follows existing codebase patterns, naming conventions and structures
- [ ] **All** temporary, refactored, migrated or obsolete code/files removed and cleaned up
- [ ] No commented-out code left behind
</spec-template>
