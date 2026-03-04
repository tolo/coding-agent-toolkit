---
description: Creates implementation plan with story breakdown from PRD. Lightweight planning - detailed specs created JIT per story.
argument-hint: [Specs directory containing PRD]
---

# Create Implementation Plan

Transform PRD into lightweight implementation plan with story breakdown. Stories are scoped and sequenced but NOT fully specified - use `/cc-workflows:spec` just-in-time before implementing each story.

**Philosophy**: Detailed specs decay quickly. This command creates just enough structure to sequence work and track progress, while deferring detailed specification to implementation time.


## Variables

_Specs directory containing PRD (**required**):_
INPUT_DIR: $ARGUMENTS

_Output location (defaults to INPUT_DIR):_
OUTPUT_DIR: `INPUT_DIR`


## Instructions

- **Make sure `INPUT_DIR` is provided** - otherwise **STOP** immediately and ask user for input
- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section in CLAUDE.md (and/or system prompt) before starting work, including but not limited to:
  - **Foundational Rules and Guardrails**
  - **Foundational Development Guidelines and Standards** (e.g. Development, Architecture, UI/UX Guidelines etc.)
- **Orchestrate, don't do everything yourself** - Delegate research, analysis, and exploration to sub-agents (see Workflow below)
- **Lightweight planning** - Stories define scope, not implementation details
- **No over-engineering** - Minimum stories to cover requirements
- **Progressive implementation** - Organize into logical phases (examples provided are templates, adapt to project)
- **JIT specification** - Detailed specs come later via `/cc-workflows:spec`


## Workflow

### 1. Input Validation

**Required:**
- PRD file in `INPUT_DIR` (e.g., `prd.md`)

**Optional (document if present):**
- Architecture/ADRs
- Design system
- Wireframes

If PRD missing, **STOP** and recommend `/cc-workflows:prd` first.

**Gate**: PRD validated


### 2. Requirements Analysis

**Delegate** codebase exploration to sub-agents to keep your context lean:

- Spawn an **Explore agent** to analyze codebase structure, existing patterns, and relevant files

Collect sub-agent results and synthesize into a unified understanding of:

#### Understand the PRD
- All requirements and user stories
- MVP scope and boundaries
- Success criteria
- Prioritization (P0/P1/P2)

#### Map to Implementation Units
For each major feature/requirement:
- Identify natural implementation boundaries
- Note dependencies between features
- Flag complexity and risk areas
- Group related functionality

**Gate**: Feature mapping complete


### 3. Story Breakdown

#### Story Guidelines

**Each story should be:**
- **Bounded** - Clear scope, single responsibility
- **Verifiable** - Has acceptance criteria
- **Independent** - Minimal coupling to other stories (after dependencies met)

**Story set rules:**
- Minimum stories to cover all requirements
- No overlap between stories
- No over-granularity (combine small related items)

#### Implementation Phases

Organize stories into logical phases. The number and nature of phases depends on the project - adapt as needed. Common pattern:

```
Phase 1: Foundation (Sequential)
├── Project setup / scaffolding
├── Core architecture / routing
└── Data layer setup

Phase 2: Core Features (Parallel where possible)
├── [P] Feature A
├── [P] Feature B
└── [P] Feature C (depends on A)

Phase 3: Integration (Sequential)
├── External service connections
├── API integrations
└── Cross-feature integration

Phase 4: Polish (Parallel)
├── [P] UI refinement
├── [P] Error handling
├── [P] Performance
└── [P] Accessibility
```

#### Story Definition

For each story, define:
- **ID**: Sequential identifier (S01, S02, etc.)
- **Name**: Brief descriptive name
- **Status**: Tracking field — initially `Pending` (updated to `In Progress` / `Done` during execution)
- **FIS**: Reference to generated spec — initially `—` (updated to file path when `/cc-workflows:spec` creates the FIS)
- **Scope**: 2-4 sentences — what's included and excluded (no implementation approach — that's for `/cc-workflows:spec`)
- **Acceptance criteria**: 3-6 testable outcomes — specific and unambiguous
- **Dependencies**: Other story IDs that must complete first
- **Phase**: Which implementation phase
- **Parallel**: [P] if can run parallel with others in same phase
- **Risk**: Low/Medium/High with brief note if Medium+
- **Asset refs**: Relevant wireframes, ADRs, design system sections

**Do NOT include** (these are deferred to `/cc-workflows:spec`):
- Technical approach, patterns, or library choices
- File paths, line numbers, or code specifics
- Implementation gotchas or constraints with workarounds
- Full technical design or pseudocode

**Gate**: All stories defined


### 4. Create Plan Document

Generate `plan.md` with a structure like the following (adapt phases and structure to fit the project):

<example-plan-format>
# Implementation Plan: [Project Name]

## Overview
- **Total stories**: [N]
- **Phases**: [N]
- **Approach**: [1-2 sentence summary]

## Story Catalog

| ID | Name | Phase | Dependencies | Parallel | Risk | Status |
|----|------|-------|--------------|----------|------|--------|
| S01 | [Name] | Foundation | - | No | Low | Pending |
| S02 | [Name] | Foundation | S01 | No | Low | Pending |
| S03 | [Name] | Core | S01, S02 | [P] | Medium | Pending |

## Phase Breakdown

### Phase 1: Foundation
_Sequential execution - establishes base for all features_

#### S01: [Story Name]
**Status**: Pending
**FIS**: —
**Scope**: [2-4 sentences covering what is built and what's excluded]
**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
**Assets**: [Wireframe refs, ADR refs if any]

#### S02: [Story Name]
...

### Phase 2: Core Features
_Parallel execution where marked [P]_

#### [P] S03: [Story Name]
...

### Phase 3: Integration
...

### Phase 4: Polish
...

## Dependency Graph

```
S01 ──→ S02 ──→ S05
  │       │
  │       └──→ S06
  │
  └──→ S03 ──→ S07
  │
  └──→ S04
```

## Risk Summary

| Story | Risk | Concern | Mitigation |
|-------|------|---------|------------|
| S03 | Medium | [Concern] | [Approach] |

## Execution Guide

1. Execute Phase 1 stories sequentially (S01 → S02 → ...)
2. For each story ready to implement:
   - Run `/cc-workflows:spec` with story scope as input → update **FIS** field with generated spec path
   - Run `/cc-workflows:implement` on generated FIS
   - Check off completed acceptance criteria in this plan
   - Update **Status** field (Pending → In Progress → Done)
3. Phase 2+ stories marked [P] can run in parallel after dependencies met
4. Use `/cc-workflows:review-gap` after completing all stories

> **Status tracking**: After each story's spec is created, update the **FIS** field with the spec file path. After implementation and review, check off acceptance criteria and set **Status** to Done. Update the Story Catalog table status accordingly. `/cc-workflows:implement-plan` does this automatically; for manual per-story execution, the orchestrating agent or user is responsible.
</example-plan-format>

**Gate**: Plan document complete


### 5. Validation

#### Self-Check
- [ ] All PRD features have corresponding stories
- [ ] No missing functionality
- [ ] Stories have clear boundaries (no overlap)
- [ ] Dependencies accurately mapped
- [ ] Parallel markers correctly applied
- [ ] Risk areas identified
- [ ] Not over-granular (combined where sensible)

#### Optional: Peer Review
Use the `/cc-workflows:review-doc` skill to validate plan for:
- Requirements coverage
- Story scope clarity
- Dependency correctness

**Gate**: Validation complete


## Output

```
OUTPUT_DIR/
└── plan.md    # Implementation plan
```

Inform user of output location when complete.


## Follow-Up Actions

After completion, suggest:

1. **Start implementation**: `/cc-workflows:spec` for first story (S01)
2. **Create GitHub issues** (if requested):
   ```bash
   # Create milestone
   gh milestone create "[Project Name] MVP" --description "..."

   # Create issues per story
   gh issue create --title "S01: [Story Name]" --body "..." --milestone "[Project Name] MVP"
   gh issue create --title "S02: [Story Name]" --body "..." --milestone "[Project Name] MVP"
   # ... etc
   ```
3. **Review plan**: `/cc-workflows:review-doc plan.md`
