---
name: spec-plan
description: Creates implementation plan with focused, independently executable stories from PRD and optional assets (architecture, design system, wireframes).
argument-hint: [Specs directory containing PRD and optional assets]
---

# Create Implementation Plan & Stories

Transform PRD and supporting assets into executable implementation plan with focused, parallel-executable stories (Feature Implementation Specifications).

**Key difference from `/spec-create`:** No research phase - PRD and assets are the research output. This command plans and structures implementation only.


## Variables

_Specs directory containing PRD and assets (**required**):_
INPUT_DIR: $ARGUMENTS

_Output location (defaults to INPUT_DIR):_
OUTPUT_DIR: `INPUT_DIR`


## Instructions

- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section in CLAUDE.md before starting work
- **No research phase** - PRD and assets are the source of truth; don't re-research
- **Parallel execution** - Use **foreground parallel agents (`run_in_background=false`)** for story creation - multiple Task calls in one message
- **Focused stories** - Each story must be standalone, independently verifiable
- **No over-engineering** - Minimum stories to cover all requirements
- **Progressive implementation** - Foundation → Features → Integration → Polish


## Workflow

### 1. Input Validation

**Required:**
- PRD file in `INPUT_DIR` (e.g., `prd.md` or similar)

**Optional but recommended:**
- Architecture/ADRs (e.g., `architecture/`, `adrs/`)
- Design system (e.g., `design-system/`, `tokens.css`, `components.css`)
- Wireframes (e.g., `wireframes/`)
- Concept designs or mockups

**Validate:**
1. `INPUT_DIR` exists
2. PRD file present and readable
3. Document which optional assets are available

If PRD missing, **STOP** and recommend `/prd` first.

**Gate**: PRD validated, available assets documented


### 2. Requirements Analysis

#### Understand the PRD
- All requirements and user stories
- MVP scope and boundaries
- Success criteria
- Prioritization (P0/P1/P2, MoSCoW)

#### Understand Available Assets
- **Architecture/ADRs**: Technical decisions, patterns, constraints
- **Design system**: Tokens, components, styling approach
- **Wireframes**: Screen layouts, UI structure (reference in UI stories)
- **Guidelines**: Dev guidelines, UX guidelines from project

#### Map Features to Stories
For each major feature/requirement in PRD:
- Identify implementation scope
- Note dependencies on other features
- Flag UI components needing wireframe references
- Estimate story complexity (single vs multi-story)

**Gate**: Requirements understood, feature-to-story mapping complete


### 3. Story Planning

#### Story Guidelines

**Every story MUST be:**
1. **Focused** - Single aspect of functionality, standalone
2. **Verifiable** - Clear acceptance criteria, testable
3. **Complete** - All context included for independent execution

**Story Set Rules:**
- Minimum stories to cover all requirements
- No overlap or duplicated work between stories
- No over-specification or unnecessary complexity

#### Progressive Implementation Layers

Organize stories into execution phases:

```
Foundation Layer (Sequential)
├── Project setup / scaffolding
├── Core architecture / routing
└── Data layer (with mocks)

Feature Layer (Parallel - mark with [P])
├── [P] Feature modules (use mocks)
├── [P] Business logic (TDD)
├── [P] API endpoints (mock responses initially)
└── [P] UI components (wireframes first, no styling)

Integration Layer (Sequential)
├── Real data connections
├── External services
└── API integrations

Polish Layer (Parallel - mark with [P])
├── [P] Design system application
├── [P] Performance optimization
├── [P] Error handling refinement
└── [P] Accessibility
```

#### Create Story List
For each identified story:
- Story ID and name
- Brief description
- Layer/phase assignment
- Dependencies (other story IDs)
- Parallel execution flag [P] if applicable
- Asset references (wireframes, ADRs, design system)

**Gate**: Complete story list with dependencies mapped


### 4. Story Specification

#### Parallel Story Creation
Use `cc-workflows:solution-architect` sub-agents to create stories in parallel.

**For each story, generate FIS with:**

1. **Feature Overview** - What this story implements
2. **Success Criteria** - Testable outcomes
3. **Scope** - In scope, out of scope, anti-patterns
4. **Architecture** - Reference relevant ADRs
5. **Critical Context**
   - Exact file paths with line numbers
   - Documentation URLs with sections
   - Wireframe references (UI stories MUST reference their wireframe)
   - Design system references (tokens, components)
   - Relevant guidelines
6. **Implementation Tasks** - Atomic tasks with [P] markers
7. **Validation Tasks** - Code review, testing, visual validation
8. **Final Checklist** - Completion criteria

**Use the FIS template from `/spec-create` appendix.**

#### Story File Naming
```
OUTPUT_DIR/
├── impl-plan.md              # Master implementation plan
└── stories/
    ├── story-001-[name].md
    ├── story-002-[name].md
    └── ...
```

**Gate**: All story FIS files created


### 5. Plan Assembly

Create master implementation plan (`impl-plan.md`):

```markdown
# Implementation Plan: [Project/Feature Name]

## Executive Summary
- Approach overview
- Total stories: [N]
- Execution phases: [N]

## Story Catalog
| ID | Name | Layer | Dependencies | Parallel |
|----|------|-------|--------------|----------|
| 001 | [Name] | Foundation | - | No |
| 002 | [Name] | Feature | 001 | [P] |

## Execution Roadmap

### Phase 1: Foundation (Sequential)
- [ ] story-001-[name]
- [ ] story-002-[name]

### Phase 2: Features (Parallel)
- [ ] [P] story-003-[name]
- [ ] [P] story-004-[name]

### Phase 3: Integration (Sequential)
- [ ] story-005-[name]

### Phase 4: Polish (Parallel)
- [ ] [P] story-006-[name]
- [ ] [P] story-007-[name]

## Dependency Map
```yaml
story-001: []
story-002: [story-001]
story-003: [story-001]
story-004: [story-001, story-002]
```

## Risk Register
| Risk | Impact | Mitigation | Stories |
|------|--------|------------|---------|
| [Risk] | High/Med/Low | [Strategy] | [IDs] |

## Success Metrics
- [ ] All PRD requirements covered
- [ ] All stories independently executable
- [ ] No story overlap or conflicts
- [ ] Progressive implementation enabled


**Gate**: Master plan assembled


### 6. Validation & Review

#### Self-Check
- [ ] All PRD features have corresponding stories
- [ ] No missing functionality or edge cases
- [ ] Each story is self-contained
- [ ] No over-engineering or over-specification
- [ ] No overlap between stories
- [ ] UI stories reference wireframes
- [ ] Stories reference relevant ADRs
- [ ] Parallel markers [P] correctly applied
- [ ] Dependencies accurately mapped

#### Peer Review
Use the `/cc-workflows:review-plan` command to validate:
- Requirements coverage against PRD
- Story quality and focus
- Completeness, correctness, edge cases, redundant aspects, etc.

**Action**: Revise based on review findings before finalizing.

**Gate**: All validation checks pass


## Output

```
OUTPUT_DIR/
├── impl-plan.md              # Master implementation plan
└── stories/
    ├── story-001-[name].md   # Individual story FIS files
    ├── story-002-[name].md
    └── ...
```

Inform user of output locations when complete.


## Follow-Up Actions

After completion, ask user if they'd like to:
1. Execute stories sequentially (`/spec-execute stories/story-001-*.md`)
2. Execute parallel stories concurrently
3. Review specific stories in more depth
4. Adjust story scope or priorities
