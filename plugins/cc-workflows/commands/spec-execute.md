---
description: Executes a Feature Implementation Specification that contains all implementation details
---

# Execute Feature Implementation Specification

Execute a fully-defined FIS document as an **orchestrator**, delegating all implementation and validation tasks to sub-agents.

## Variables
FIS_FILE_PATH: $ARGUMENTS


## Instructions

### Core Rules
- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section in CLAUDE.md (and/or system prompt) before starting work, including but not limited to:
  - **Foundational Rules and Guardrails** (absolute must-follow rules)
  - **Foundational Development Guidelines and Standards** (e.g. Development, Architecture, UI/UX Guidelines etc.)
- **Spec generation only** - No code changes, commits, or modifications during execution of this command
- **Complete Implementation**: 100% completion required - no partial work  
- **FIS is source of truth** — follow it exactly
- **Sub-agents for all tasks** — act as orchestrator and delegate all work to sub-agents

### Orchestrator Role
**You are the orchestrator.** Your job is to:
- Load and understand the FIS
- Delegate ALL implementation/validation tasks to sub-agents
- Track progress and collect results
- Ensure final validation checklist is complete

**You do NOT:**
- Write implementation code directly (delegate to sub-agents)
- Let your context get bloated with implementation details
 Skip final steps due to context exhaustion

### Sub-Agent Protocol

#### Input Template (provide to each sub-agent)
```
## Task: {TASK_ID} - {Task title}
{Task description and sub-items from FIS}

## FIS Reference
Path: {FIS_FILE_PATH}
Read sections: ADR, Critical Documentation & Context, relevant Implementation Notes

## Key References (from FIS)
{List specific file:line references relevant to THIS task}

## Previous Task Context (if sequential dependency)
{Brief summary of what previous tasks accomplished that this task depends on}

## Requirements
1. Complete the task fully per FIS spec
2. Follow patterns in referenced files
3. Report back: status, files changed, decisions made, issues encountered
```

#### Expected Output (sub-agent should provide)
```
Status: complete | partial | blocked
Files changed: {list of created/modified files}
Decisions: {any deviations or choices made}
Issues: {blockers, errors, concerns for orchestrator}
```

#### Handling Sub-Agent Results
After each sub-agent completes:
1. **Read the result** — extract status, files changed, issues
2. **Update FIS** — check off completed task checkbox
3. **Track context** — note key outputs needed by dependent tasks
4. **Handle issues** — if blocked/partial, assess and either retry or flag for user


## Workflow

### Step 1: Load FIS and Prepare
1. Read FIS at _`FIS_FILE_PATH`_
2. Fully Understand vital sections like Success Criteria, Scope & Boundaries, Solution Architecture and Design, Critical Documentation & Context, Implementation Plan, etc.
3. Analyse the codebase to properly understand the project structure, relevant files and similar patterns
  - Use command like `tree -d` and `git ls-files | head -250` to get an overview of the codebase structure
4. Read any _`fis-implementation-notes.md`_ document for additional context and learnings from previous specifications
5. Create task tracking for ALL tasks (implementation + validation)

### Step 2: Execute Implementation Tasks
For each implementation task (TI01, TI02, etc.):

**Sequential tasks:**
- Spawn **sub-agents** (foreground, i.e. `run_in_background=false`) with Input Template
- Wait for result
- Process output, update FIS, track context for next task

**Parallel tasks [P]:**
- Spawn **parallel sub-agents** (foreground, i.e. `run_in_background=false`)
- Ensure tasks don't have file conflicts
- Collect all results, update FIS

**Sub-agent selection:**
- Default: `general-purpose` agent
- Build issues: `cc-workflows:build-troubleshooter`
- UI work: `cc-workflows:ui-ux-designer`
- Complex architecture: `cc-workflows:solution-architect`

### Step 3: Execute Validation Tasks
**CRITICAL**: Execute all validation tasks (TV01-TV03) in **parallel sub-agents**, never directly from the main agent.
Important: Correct implementation of requirements and acceptance criteria must be verified through tests and visual validation (when applicable).

#### TV01 [P] — Level 1: Code Review
The sub-agent for code review (general-purpose) should use the `/cc-workflows:code-review` skill for comprehensive review and analysis covering:

- Static analysis, linting, formatting and type checking issues
- Code quality (correctness, readability, best practices, performance, maintainability)
- Architecture (pattern adherence, ADR compliance, anti-pattern detection)
- Security (input validation, injection prevention, auth, data protection, OWASP Top 10)
- UI/UX (if applicable - visual quality, usability, accessibility)

#### TV02 [P] — Level 2: Testing
Use the `cc-workflows:qa-test-engineer` sub-agent to execute tests fow new and existing functionality:
- Unit tests
- Integration tests (if applicable)
- E2E tests (if applicable)

#### TV03 [P] — Level 3: Visual Validation (if UI)
- Verify updated UI works correctly according to specified requirements
- Use the `cc-workflows:visual-validation-specialist` sub-agent for full visual validation
- This agent automatically follows any **Visual Validation Workflow** defined in CLAUDE.md
- Checks for visual regressions and ensures UI matches design specs

#### TV04 — Address Issues
- Collect all validation feedback from the validation task sub-agents
- Spawn sub-agents to fix identified issues, if any
- Re-run affected validation levels if needed

### Step 4: Final Quality Assurance
As orchestrator (not delegated to sub-agent):
- Review all sub-agent results
- Check for functionality gaps or requirement mismatches
- Use `code-simplifier:code-simplifier` agent to look for simplification, maintainability, and general quality of life improvement opportunities

### Step 5: Verify Completion
**Orchestrator performs directly:**
1. Verify ALL success criteria in FIS are met
2. Verify ALL task checkboxes marked complete (- [x])
3. Verify Final Validation Checklist items are satisfied
4. Update FIS with completion status

### Step 6: Iteration (if needed)
If success criteria not met or if previous step failed to successfully verify completion:
1. Analyze gaps from validation feedback
2. Create new tasks for fixes
3. Execute Steps 2-5 again


## Report: Update Implementation Notes documents with important learnings and decsisions
After completion, update `fis-implementation-notes.md` with important implementation notes, making sure to keep them very concise and to the point (avoid any unnecessary verbosity and code listings etc).

Including details like:
- Extremelty brief descripton of what was implemented and how parts integrate
- Key challenges faced and how they were overcome
- Important decisions made and their rationale
- Deviations from plan
- Unresolved issues or future suggestions
