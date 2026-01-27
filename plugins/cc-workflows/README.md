# cc-workflows

Development workflows for Claude Code - from requirements to implementation with built-in quality gates.

## Installation

```bash
# User scope (available in all projects)
claude plugin install ./plugins/cc-workflows --scope user

# Project scope (this project only)
claude plugin install ./plugins/cc-workflows --scope project
```

## Setup

Commands and agents reference a **"Workflow Rules, Guardrails and Guidelines"** section in your project's `CLAUDE.md`. Add this section to define the rules and guidelines that should be followed during workflow execution.

Example structure:

```markdown
## Workflow Rules, Guardrails and Guidelines

### Foundational Rules and Guardrails
[Link to or inline your project's core rules - code quality, testing requirements, etc.]

### Foundational Development Guidelines and Standards
[List paths to relevant guidelines, such as:]
- [Development and architecture]
- [UI/UX standards]
- [Other domain-specific guidelines]
```

See [CLAUDE.template.md](./../../CLAUDE.template.md) for a starter template, or this repository's [CLAUDE.md](./../../CLAUDE.md) for a full example.


## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│  FEATURE WORKFLOW (single feature)                          │
│                                                             │
│  ┌─────────────────────── OPTIONAL: ─────────────────────┐  │
│  │ wireframes, design-system, trade-off-analysis         │  │
│  └───────────────────────────┬───────────────────────────┘  │
│                              │                              │
│  (optional)                  ▼         (optional)           │
│  clarify ────────────→ spec-create ──→ review-plan          │
│                              │                              │
│                              ▼                              │
│                        spec-execute                         │
│                              │                              │
│                              ▼                              │
│                        review-impl                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  IMPLEMENTATION PLAN WORKFLOW (MVP / multi-feature)         │
│                                                             │
│  ┌───────────────────── RECOMMENDED: ────────────────────┐  │
│  │ wireframes, design-system, trade-off-analysis         │  │
│  └───────────────────────────┬───────────────────────────┘  │
│                              │                              │
│  (optional)                  ▼            (optional)        │
│  clarify ──→ prd ─────→ spec-plan ──────→ review-plan       │
│                        (creates stories)                    │
│                              │                              │
│                              ▼                              │
│                     spec-execute (per story)                │
│                              │                              │
│                              ▼                              │
│                        review-impl                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  QUICK PATH (small features/fixes)                          │
│                                                             │
│  quick-implement ──→ review-code (optional) ──→ done (or PR)│
└─────────────────────────────────────────────────────────────┘
```

**When to use which:**
- **Feature workflow**: Single feature, complex changes, multi-file modifications
- **Implementation plan workflow**: MVP, new project, multi-feature work
- **Quick path**: Bug fixes, small features, GitHub issues

**Pre-activities** (feed into spec-create, prd, or spec-plan):
- `clarify` - When requirements are vague
- `wireframes` / `design-system` - When UI design is needed
- `trade-off-analysis` - When architectural decisions are needed

## Commands

Invoke with `/cc-workflows:<command>` or just `/<command>` if unambiguous.

### Preparation (Pre-spec)

| Command | Purpose |
|---------|---------|
| `clarify` | Transform vague ideas into clear, actionable requirements |
| `prd` | Create comprehensive PRD from refined requirements |
| `trade-off-analysis` | Evaluate technical alternatives with structured comparison |
| `wireframes` | Generate HTML wireframes for UI planning |
| `design-system` | Create design tokens and component styles |

### Specification (Core)

| Command | Purpose |
|---------|---------|
| `spec-create` | Create single FIS from feature requirements (includes research) |
| `spec-plan` | Create implementation plan with multiple stories from PRD (no research) |
| `spec-execute` | Execute FIS/story with validation loops until complete |

### Quick Path

| Command | Purpose |
|---------|---------|
| `quick-implement` | Fast path for small features/fixes (supports `--issue` for GitHub) |

### Review

| Command | Purpose | When |
|---------|---------|------|
| `review-plan` | Review requirements/specs/plans for completeness, clarity, feasibility | Pre-execution |
| `review-code` | Code quality, security, architecture review (uses code-review skill) | Post-execution |
| `review-impl` | Review implementation against requirements (includes code review + gap analysis) | Post-execution |

### Utilities

| Command | Purpose |
|---------|---------|
| `troubleshoot` | Diagnose and fix implementation issues systematically |
| `ui-concept` | Exploratory UI design with multiple creative directions |

## Usage Examples

### Feature Workflow (single feature)

```bash
# 1. Clarify vague requirements
/cc-workflows:clarify "users should be able to export their data"

# 2. Generate implementation spec (includes research)
/cc-workflows:spec-create <requirements from step 1>

# 3. Execute the spec
/cc-workflows:spec-execute

# 4. Final review (against requirements)
/cc-workflows:review-impl
```

### Implementation Plan Workflow (MVP / multi-feature)

```bash
# 1. Clarify and create PRD
/cc-workflows:clarify "dashboard for analytics"
/cc-workflows:prd

# 2. Optional: create design assets
/cc-workflows:wireframes
/cc-workflows:design-system

# 3. Generate implementation plan with stories
/cc-workflows:spec-plan docs/specs/dashboard/

# 4. Execute stories (can parallelize independent ones)
/cc-workflows:spec-execute docs/specs/dashboard/stories/story-001-*.md
/cc-workflows:spec-execute docs/specs/dashboard/stories/story-002-*.md

# 5. Final review (against PRD requirements)
/cc-workflows:review-impl
```

### Quick Fix from GitHub Issue

```bash
# Fetches issue, implements, creates PR
/cc-workflows:quick-implement --issue 123
```

### Technical Decision Making

```bash
# When facing architectural choices
/cc-workflows:trade-off-analysis "caching strategy for API responses"
```

## Agents

Specialized sub-agents for delegation (used internally by commands):

| Agent | Purpose |
|-------|---------|
| `build-troubleshooter` | Build/test failure diagnosis |
| `documentation-lookup` | External documentation retrieval |
| `qa-test-engineer` | Test coverage and validation |
| `research-specialist` | Web research and synthesis |
| `screenshot-validation-specialist` | Visual UI comparison |
| `solution-architect` | Architecture design |
| `ui-ux-designer` | UI/UX design |
| `whimsy-injector` | Playful, unconventional UI/UX inspiration |

## Skills

| Skill | Purpose |
|-------|---------|
| `code-review` | Comprehensive review with checklists (code, security, architecture, UI/UX) |

## Key Concepts

### Feature Implementation Specification (FIS)

A structured document generated by `spec-create` or `spec-plan` containing everything needed for autonomous implementation:
- Requirements and acceptance criteria
- Technical approach and architecture
- File changes and dependencies
- Validation checklist

### Implementation Loop

Both `spec-execute` and `quick-implement` use an iterative cycle:
```
Implement → Verify → Evaluate → (repeat if needed)
```

Verification includes code review, testing, and visual validation (when applicable).

### Review Types

- **Plan Review**: Is the spec complete and clear? (before execution)
- **Code Review**: Is the code well-written? (after execution)
- **Gap Analysis**: Does implementation match requirements? (after execution)

## License

MIT