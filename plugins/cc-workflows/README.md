# cc-workflows

Development workflows for Claude Code - from requirements to implementation with built-in quality gates.

> **Note**: Hooks (security, notifications, context re-injection) have moved to [`hooks/`](../../hooks/) at the repo root as standalone scripts. See [hooks/README.md](../../hooks/README.md) for setup.

## Installation

Add the parent repo as a [plugin marketplace](https://code.claude.com/docs/en/discover-plugins), then install:

```bash
# Add marketplace
/plugin marketplace add tolo/coding-agent-toolkit

# Install plugin
/plugin install cc-workflows@coding-agent-toolkit
```

**Scope options** — installs at `user` scope (all projects) by default:
```bash
/plugin install cc-workflows@coding-agent-toolkit --scope project  # current project only
```

**Local install** — if you have the repo cloned:
```bash
claude plugin install ./plugins/cc-workflows
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

### Agent Teams (Optional)

Some commands like `review-council` and `implement-plan` use [Agent Teams](https://code.claude.com/docs/en/agent-teams) for parallel multi-agent coordination.

To enable Agent Teams (experimental):

```json
// ~/.claude/settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Or via environment variable:
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

Commands automatically fall back to single-agent alternatives when Agent Teams unavailable.


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
│  clarify ────────────→   spec   ────→ review-doc            │
│                              │                              │
│                              ▼                              │
│                          implement                          │
│                              │                              │
│                              ▼                              │
│                        review-gap                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PLAN WORKFLOW (MVP / multi-feature)                        │
│                                                             │
│  ┌───────────────────── RECOMMENDED: ────────────────────┐  │
│  │ wireframes, design-system, trade-off-analysis         │  │
│  └───────────────────────────┬───────────────────────────┘  │
│                              │                              │
│    (optional)                ▼                              │
│    clarify ──→ prd ─────→  plan  ───────→ review-doc        │
│                       (story breakdown)                     │
│                              │                              │
│                   ┌─────────┴──────────┐                    │
│                   ▼                    ▼                    │
│            Manual per-story    implement-plan            │
│            (spec →             (Agent Team pipeline:        │
│             implement →         parallel story execution)   │
│             review-gap)                                     │
│                   └─────────┬──────────┘                    │
│                              ▼                              │
│                        review-gap                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  QUICK PATH (small features/fixes)                          │
│                                                             │
│  quick-implement ──→ review-code (optional) ──→ done (or PR)│
└─────────────────────────────────────────────────────────────┘
```

**When to use which:**
- **Feature workflow**: Single feature, complex changes, multi-file modifications
- **Plan workflow**: MVP, new project, multi-feature work
- **Quick path**: Bug fixes, small features, GitHub issues

**Pre-activities** (feed into spec, prd, or plan):
- `clarify` - When requirements are vague
- `wireframes` / `design-system` - When UI design is needed
- `trade-off-analysis` - When architectural decisions are needed

## Commands / Skills

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
| `spec` | Create single FIS from feature requirements (includes research) |
| `plan` | Create lightweight implementation plan with story breakdown from PRD |
| `implement` | Execute FIS with validation loops until complete |
| `implement-plan` | Execute entire plan through Agent Team pipeline (spec → implement → review-gap per story) |

### Quick Path

| Command | Purpose |
|---------|---------|
| `quick-implement` | Fast path for small features/fixes (supports `--issue` for GitHub) |

### Review

| Command / Skill | Purpose | When |
|---------|---------|------|
| `review-code` | Comprehensive code review with checklists (code quality, security, architecture, UI/UX) | Post-execution |
| `review-doc` | Document review for completeness, clarity, edge cases, and technical accuracy | Pre-execution |
| `review-gap` | Gap analysis: implementation vs requirements (includes code review + remediation plan) | Post-execution |
| `review-council` | Multi-perspective review with Agent Teams (adaptive roster: 5-7 specialized reviewers + debate) | Post-execution |

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
/cc-workflows:spec <requirements from step 1>

# 3. Execute the spec
/cc-workflows:implement

# 4. Final review (against requirements)
/cc-workflows:review-gap
```

### Plan Workflow (MVP / multi-feature)

```bash
# 1. Clarify and create PRD
/cc-workflows:clarify "dashboard for analytics"
/cc-workflows:prd

# 2. Optional: create design assets
/cc-workflows:wireframes
/cc-workflows:design-system

# 3. Generate implementation plan (story breakdown)
/cc-workflows:plan docs/specs/dashboard/

# 4a. Execute all stories via Agent Team pipeline (recommended)
/cc-workflows:implement-plan docs/specs/dashboard/

# 4b. OR manually per story: create spec JIT, then execute
/cc-workflows:spec "S01: Project Setup" # from plan
/cc-workflows:implement
/cc-workflows:review-gap
# ... repeat for each story

# 5. Final review (against PRD requirements)
/cc-workflows:review-gap
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

### Plan Execution with Agent Team Pipeline

```bash
# Execute entire plan through parallelized Agent Team pipeline
# Requires Agent Teams feature enabled
/cc-workflows:implement-plan docs/specs/dashboard/

# Spawns Spec Creators, Implementers, and Reviewers that work
# through all stories: spec → implement → review-gap
# Respects phase ordering, dependencies, and [P] parallel markers
# Team size scales with story count (3-8 agents)

# Falls back to manual per-story execution if Agent Teams unavailable
```

### Multi-Perspective Review (Agent Teams)

```bash
# Adaptive review - analyzes scope and selects 5-7 relevant reviewers
# Requires Agent Teams feature enabled
/cc-workflows:review-council

# Review specific PR with council
/cc-workflows:review-council --pr 123

# Focus on specific aspect
/cc-workflows:review-council "security"

# Reviewers auto-selected based on changes:
# - Product features → Product Manager, Requirements Analyst, etc.
# - Backend APIs → Security, Performance, API Designer, etc.
# - Frontend UI → UX/Accessibility, Frontend Specialist, etc.
# - Always includes Devil's Advocate + Synthesis Challenger (two-phase validation)

# Falls back to /cc-workflows:review-code if Agent Teams unavailable
```

## External Dependencies (Optional)

Some commands optionally use skills from other plugins when available:

| Plugin | Used by | Purpose |
|--------|---------|---------|
| `code-simplifier` | `refactor`, `implement`, `quick-implement` | Code cleanup and simplification |
| `frontend-design` | `wireframes` (via `ui-ux-designer` agent) | Design implementation |

Commands work without these plugins but skip the corresponding steps.

## Agents

Specialized sub-agents for delegation (used internally by commands):

| Agent | Purpose |
|-------|---------|
| `build-troubleshooter` | Build/test failure diagnosis |
| `documentation-lookup` | External documentation retrieval |
| `qa-test-engineer` | Test coverage and validation |
| `research-specialist` | Web research and synthesis |
| `solution-architect` | Architecture design |
| `ui-ux-designer` | UI/UX design |
| `visual-validation-specialist` | Full visual validation workflow (primary) |
| `whimsy-injector` | Playful, unconventional UI/UX inspiration |

## Key Concepts

### Feature Implementation Specification (FIS)

A structured document generated by `spec` containing everything needed for autonomous implementation:
- Requirements and acceptance criteria
- Technical approach and architecture
- File changes and dependencies
- Validation checklist

### Implementation Plan

A lightweight planning document generated by `plan` that breaks down PRD into stories:
- Story scope and acceptance criteria (high-level)
- Dependencies and execution sequence
- Phase organization (Foundation → Features → Integration → Polish)

Detailed FIS specs are created just-in-time via `spec` when each story is ready for implementation.

### Implementation Loop

Both `implement` and `quick-implement` use an iterative cycle:
```
Implement → Verify → Evaluate → (repeat if needed)
```

Verification includes code review, testing, and visual validation (when applicable).

### Review Types

- **Document Review** (`review-doc`): Is the spec complete and clear? (before execution)
- **Code Review** (`review-code` skill): Is the code well-written? (after execution)
- **Gap Analysis** (`review-gap`): Does implementation match requirements? (after execution)

## License

MIT