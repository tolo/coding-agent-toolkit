---
description: Creates comprehensive Product Requirements Document (PRD) from refined requirements, covering all functional and non-functional requirements with no outstanding questions.
argument-hint: [Requirements source - refined idea file, clarification doc, or description]
---

# Create Product Requirements Document (PRD)

Create comprehensive PRD from refined requirements, ensuring all edge cases covered and no outstanding questions remain.


## Variables

_Requirements source (**required**):_
INPUT: $ARGUMENTS

_Output directory for PRD:_
OUTPUT_DIR: `<project_root>/docs/specs/`


## Instructions

- **Make sure `INPUT` is provided** - otherwise **STOP** immediately and ask user for input
- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section in CLAUDE.md before starting work
- **Interactive process** - Interview user iteratively; don't assume answers
- **Be thorough** - Challenge assumptions, find edge cases, identify all ambiguities
- **Focus on "what" not "how"** - Requirements, not implementation details
- **Be specific** - Replace vague terms with measurable criteria
- **Document decisions** - Record rationale, trade-offs, alternatives considered


## Workflow

### 1. Parse and Validate Input

1. **Parse INPUT** - Determine type: file path, URL, or inline description
   - If file path: Read and extract requirements
   - If URL: Fetch and extract requirements
   - If description: Use directly

2. **Validate prerequisites**
   - Requirements should be reasonably refined (not raw ideas)
   - If input is too vague, recommend `/clarify` first

3. **Initial gap analysis** - Document:
   - What's explicitly stated
   - What's assumed or implied
   - What's missing or unclear in these areas:
     - Functional requirements
     - User flows and edge cases
     - Success criteria
     - Business context
     - MVP scope

**Gate**: Input validated, initial gaps documented


### 2. Requirements Discovery Interview

Interview user to fill gaps. Ask 3-5 targeted questions at a time, iterate until no major gaps remain.

**Core Functionality**
- Must-have vs nice-to-have features?
- Specific workflow for each major user action?
- Data validation rules and constraints?
- Error handling and recovery?
- Does this involve UI/frontend work? (determines if wireframes needed)

**Users & Permissions**
- User roles and their permissions?
- Expected user onboarding process?
- Accessibility requirements?
- Devices and platforms to support?

**Business Logic**
- Business rules and constraints?
- Concurrent access handling?
- Data retention and deletion policies?
- Compliance or regulatory requirements?

**Edge Cases & Errors**
- Network connectivity loss handling?
- Incomplete or partial data handling?
- Timeout and retry policies?
- Graceful degradation under load?
- Fallback for external dependency failures?

**Success Metrics**
- Specific metrics defining success?
- Performance benchmarks?
- Quality thresholds?

**Gate**: All critical questions answered, no blocking ambiguities


### 3. Structure PRD

Based on interview responses, structure comprehensive PRD:

#### Executive Summary
- Project title
- Problem statement with quantified impact
- Product vision and objectives
- Target audience and user personas
- Success definition with measurable metrics

#### Problem Definition & Context
- Clear problem statement with evidence
- User research insights and pain points
- Market opportunity (if applicable)
- Competitive landscape (if applicable)

#### MVP Scope & Boundaries

**In Scope**
- Core functionality (must-haves)
- Explicit inclusions

**Out of Scope**
- Explicit exclusions
- Deferred to future iterations

**MVP Boundary**
- Minimum viable version definition
- MVP validation approach

#### Functional Requirements

**User Stories**
- Format: "As a [user type], I want [goal], so that [benefit]"
- Include acceptance criteria for each

**Feature Specifications**
For each feature:
- Description and purpose
- Testable acceptance criteria
- Input/output specifications
- Validation rules
- Error handling
- Priority (P0/P1/P2)

**Core User Flows**
- Primary flows with step-by-step descriptions
- Alternative paths
- Error scenarios and recovery

**UI Wireframes** _(if applicable - skip for backend-only work)_
- Simple ASCII wireframes for core screens/views
- Focus on layout structure and key elements only
- Show primary user interaction points
- Keep minimal - just enough to communicate intent

**Data Requirements**
- Data models and relationships
- Required fields and constraints
- Data validation rules
- Privacy considerations

#### Non-Functional Requirements

**Performance**
- Response time expectations
- Throughput requirements
- Scalability considerations

**Reliability**
- Uptime requirements
- Error recovery expectations
- Data backup needs

**Security**
- Authentication requirements
- Authorization and access control
- Data protection needs
- Compliance requirements

**Usability**
- Accessibility standards
- Browser/device compatibility
- Internationalization needs

#### Edge Cases
| Scenario | Expected Behavior |
|----------|------------------|
| [Edge case] | [Handling] |

#### Constraints & Assumptions

**Constraints**
- Technical constraints
- Resource limitations
- Regulatory constraints

**Assumptions**
- User behavior assumptions
- Technical assumptions
- Business assumptions
- External dependencies

**Gate**: PRD structure complete with all sections filled


### 4. Prioritization

Apply systematic prioritization to features:

**MoSCoW Classification**
- **Must have**: Core MVP functionality
- **Should have**: Important but not vital
- **Could have**: Desirable but optional
- **Won't have**: Explicitly out of scope

**Priority Levels**
- P0: Critical - MVP blocker
- P1: High - Core functionality
- P2: Medium - Important enhancement

**Gate**: All features prioritized


### 5. Validation & Review

#### Completeness Check
- [ ] Problem definition clearly articulated with impact
- [ ] All user stories have testable acceptance criteria
- [ ] Every feature has defined error handling
- [ ] All edge cases have specified behavior
- [ ] Success metrics are specific and measurable
- [ ] Non-functional requirements have clear thresholds
- [ ] No ambiguous terms without definitions

#### Quality Check
- [ ] Requirements focus on "what" not "how"
- [ ] All assumptions documented
- [ ] Dependencies identified
- [ ] Security considerations included
- [ ] Accessibility standards specified
- [ ] No conflicting requirements
- [ ] No over-specification or gold-plating

#### Launch Peer Review
Use `cc-workflows:review-plan` agent to validate PRD for:
- Missing requirements or user stories
- Over-engineered or unnecessarily complex features
- Conflicting requirements
- Ambiguities and unclear priorities
- Scope creep beyond MVP

**Action**: Revise PRD based on review findings before finalizing.

**Gate**: All validation checks pass, peer review complete


## Report

Generate markdown document following this structure:

```markdown
# Product Requirements Document: [Name]

## Executive Summary
- **Project**: [Title]
- **Problem**: [Statement with quantified impact]
- **Vision**: [Product vision]
- **Target Users**: [User personas]
- **Success Metrics**: [Measurable outcomes]

## Problem Definition
[Clear problem statement with evidence and context]

## Scope

### In Scope
- [Explicit inclusions]

### Out of Scope
- [Explicit exclusions]

### MVP Boundary
- [Minimum viable version definition]

## Functional Requirements

### User Stories
| ID | Story | Acceptance Criteria | Priority |
|----|-------|---------------------|----------|
| US01 | As a [user], I want [goal], so that [benefit] | [Criteria] | P0/P1/P2 |

### Feature Specifications

#### [Feature Name]
- **Description**: [What and why]
- **Acceptance Criteria**: [Testable criteria]
- **Inputs**: [Expected inputs]
- **Outputs**: [Expected outputs]
- **Validation**: [Rules and constraints]
- **Error Handling**: [Error scenarios and recovery]
- **Priority**: P0/P1/P2

### User Flows
1. [Primary flow with steps]

### UI Wireframes
<!-- Include only if PRD involves UI work -->
```
+----------------------------------+
|  [Screen Name]                   |
+----------------------------------+
|  [Header/Nav]                    |
+----------------------------------+
|                                  |
|  [Main Content Area]             |
|  - Key element 1                 |
|  - Key element 2                 |
|                                  |
+----------------------------------+
|  [Actions/Footer]                |
+----------------------------------+
```

### Data Requirements
- [Data models, fields, constraints]

## Non-Functional Requirements

### Performance
- [Response times, throughput, scalability]

### Reliability
- [Uptime, recovery, backup]

### Security
- [Auth, access control, compliance]

### Usability
- [Accessibility, compatibility, i18n]

## Edge Cases
| Scenario | Expected Behavior |
|----------|------------------|
| [Edge case] | [Handling] |

## Constraints & Assumptions

### Constraints
- [Technical, resource, regulatory]

### Assumptions
- [User, technical, business assumptions]

### Dependencies
| Dependency | Purpose | Risk |
|------------|---------|------|
| [System/API] | [Why needed] | [Risk level] |

## Decisions Log
| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| [Choice] | [Why] | [Other options rejected] |
```

Store PRD in: `OUTPUT_DIR/<feature-name>/prd.md`

Inform user of report location when complete.


## Follow-Up Actions

After completion, ask user if they'd like to:
1. Generate implementation plan with stories (`/spec-plan`)
2. Create wireframes (`/wireframes`)
3. Review specific sections in more depth
4. Share with stakeholders for validation
