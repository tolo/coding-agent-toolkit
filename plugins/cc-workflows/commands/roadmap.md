---
description: Creates implementation roadmap with story breakdown from PRD. Lightweight planning - detailed specs created JIT per story.
argument-hint: [Specs directory containing PRD]
---

# Create Implementation Roadmap

Transform PRD into lightweight implementation roadmap with story breakdown. Stories are scoped and sequenced but NOT fully specified - use `/spec-create` just-in-time before implementing each story.

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
- **Lightweight planning** - Stories define scope, not implementation details
- **No over-engineering** - Minimum stories to cover requirements
- **Progressive implementation** - Organize into logical phases (examples provided are templates, adapt to project)
- **JIT specification** - Detailed specs come later via `/spec-create`


## Workflow

### 1. Input Validation

**Required:**
- PRD file in `INPUT_DIR` (e.g., `prd.md`)

**Optional (document if present):**
- Architecture/ADRs
- Design system
- Wireframes

If PRD missing, **STOP** and recommend `/prd` first.

**Gate**: PRD validated


### 2. Requirements Analysis

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
- **Scope**: 3-5 sentences — what's included AND the general approach (e.g. "Implement X using Y pattern; Z is handled by...")
- **Approach**: 1-2 sentences on the high-level technical direction (key pattern, library, or strategy to use)
- **Acceptance criteria**: 3-6 testable outcomes — specific and unambiguous
- **Key Notes** _(optional)_: Max 3 bullets for gotchas, constraints, or non-obvious decisions
- **Dependencies**: Other story IDs that must complete first
- **Phase**: Which implementation phase
- **Parallel**: [P] if can run parallel with others in same phase
- **Risk**: Low/Medium/High with brief note if Medium+
- **Asset refs**: Relevant wireframes, ADRs, design system sections

**Do NOT include:**
- File paths, line numbers, or code specifics (that's for `/spec-create`)
- Full technical design or pseudocode

These come later via `/spec-create` when the story is ready for implementation.

**Gate**: All stories defined


### 4. Create Roadmap Document

Generate `roadmap.md` with a structure like the following (adapt phases and structure to fit the project):

<example-roadmap-format>
# Implementation Roadmap: [Project Name]

## Overview
- **Total stories**: [N]
- **Phases**: [N]
- **Approach**: [1-2 sentence summary]

## Story Catalog

| ID | Name | Phase | Dependencies | Parallel | Risk |
|----|------|-------|--------------|----------|------|
| S01 | [Name] | Foundation | - | No | Low |
| S02 | [Name] | Foundation | S01 | No | Low |
| S03 | [Name] | Core | S01, S02 | [P] | Medium |

## Phase Breakdown

### Phase 1: Foundation
_Sequential execution - establishes base for all features_

#### S01: [Story Name]
**Scope**: [3-5 sentences covering what is built and the general approach]
**Approach**: [1-2 sentences — key pattern, library, or strategy]
**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
**Key Notes**: _(optional)_
- [Gotcha or constraint]
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
   - Run `/spec-create` with story scope as input
   - Run `/spec-execute` on generated FIS
3. Phase 2+ stories marked [P] can run in parallel after dependencies met
4. Use `/review-impl` after completing all stories
</example-roadmap-format>

**Gate**: Roadmap document complete


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
Use the `/cc-workflows:review-plan` command to validate roadmap for:
- Requirements coverage
- Story scope clarity
- Dependency correctness

**Gate**: Validation complete


## Output

```
OUTPUT_DIR/
└── roadmap.md    # Implementation roadmap
```

Inform user of output location when complete.


## Follow-Up Actions

After completion, suggest:

1. **Start implementation**: `/spec-create` for first story (S01)
2. **Create GitHub issues** (if requested):
   ```bash
   # Create milestone
   gh milestone create "[Project Name] MVP" --description "..."

   # Create issues per story
   gh issue create --title "S01: [Story Name]" --body "..." --milestone "[Project Name] MVP"
   gh issue create --title "S02: [Story Name]" --body "..." --milestone "[Project Name] MVP"
   # ... etc
   ```
3. **Review roadmap**: `/cc-workflows:review-plan roadmap.md`
