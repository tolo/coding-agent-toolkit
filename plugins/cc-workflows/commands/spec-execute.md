---
description: Executes a Feature Implementation Specification that contains all implementation details
---

# Execute Feature Implementation Specification

Execute a fully-defined FIS document as an **orchestrator**, delegating all implementation and validation tasks to sub-agents.

## Variables
FIS_FILE_PATH: $ARGUMENTS


## Instructions

### Orchestrator Role
**You are the orchestrator.** Your job is to:
- Load and understand the FIS
- Delegate ALL implementation/validation tasks to sub-agents
- Track progress and collect results
- Ensure final validation checklist is complete

**You do NOT:**
- Write implementation code directly (delegate to sub-agents)
- Let your context get bloated with implementation details
- Skip final steps due to context exhaustion

### Core Rules
- **Fully** read CLAUDE.md guidelines before starting
- **100% completion required** — no partial work
- **FIS is source of truth** — follow it exactly
- **Sub-agents for all tasks** — keep orchestrator context lean
- **Validation by different agents** than implementation (independent verification)


## Sub-Agent Protocol

### Input Template (provide to each sub-agent)
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

### Expected Output (sub-agent should provide)
```
Status: complete | partial | blocked
Files changed: {list of created/modified files}
Decisions: {any deviations or choices made}
Issues: {blockers, errors, concerns for orchestrator}
```

### Handling Sub-Agent Results
After each sub-agent completes:
1. **Read the result** — extract status, files changed, issues
2. **Update FIS** — check off completed task checkbox
3. **Track context** — note key outputs needed by dependent tasks
4. **Handle issues** — if blocked/partial, assess and either retry or flag for user


## Workflow

### Step 1: Load FIS and Prepare
1. Read FIS at _`FIS_FILE_PATH`_
2. Understand: Success Criteria, Scope, ADR, Implementation Plan
3. Quick codebase orientation: `tree -d`, `git ls-files | head -100`
4. Read any existing `fis-implementation-notes.md`
5. Create task tracking for ALL tasks (implementation + validation)

### Step 2: Execute Implementation Tasks
For each implementation task (TI01, TI02, etc.):

**Sequential tasks:**
- Spawn sub-agent with Input Template
- Wait for result
- Process output, update FIS, track context for next task

**Parallel tasks [P]:**
- Spawn multiple sub-agents in single message (`run_in_background=false`)
- Ensure tasks don't have file conflicts
- Collect all results, update FIS

**Sub-agent selection:**
- Default: `general-purpose` agent
- Build issues: `cc-workflows:build-troubleshooter`
- UI work: `cc-workflows:ui-ux-designer`
- Complex architecture: `cc-workflows:solution-architect`

### Step 3: Execute Validation Tasks
**CRITICAL**: Use different agents than implementation for independent verification.

#### TV01 [P] — Level 1: Code Review
Use `code-review` skill:
- Static analysis, linting, type checking
- Code quality, security, maintainability
- Architecture adherence to ADR
- Requirements coverage gaps

#### TV02 [P] — Level 2: Testing
Use `cc-workflows:qa-test-engineer`:
- Unit tests for new functionality
- Integration tests (if applicable)
- E2E tests (if applicable)

#### TV03 [P] — Level 3: Visual Validation (if UI)
Use `cc-workflows:screenshot-validation-specialist`:
- UI matches requirements/design specs
- No visual regressions

#### TV04 — Address Issues
- Collect all validation feedback
- Spawn sub-agents to fix identified issues
- Re-run affected validation levels if needed

### Step 4: Final Quality Assurance
As orchestrator (not delegated):
- Review all sub-agent results
- Check for functionality gaps or requirement mismatches
- If simplification opportunities exist, use `code-simplifier` agent

### Step 5: Verify Completion
**Orchestrator performs directly:**
1. Verify ALL success criteria in FIS are met
2. Verify ALL task checkboxes marked complete (- [x])
3. Verify Final Validation Checklist items are satisfied
4. Update FIS with completion status

### Step 6: Iteration (if needed)
If success criteria not met:
1. Analyze gaps from validation feedback
2. Create new tasks for fixes
3. Execute Steps 2-5 again


## Report: Implementation Notes
After completion, update `fis-implementation-notes.md`:
- What was implemented and how parts integrate
- Key challenges and solutions
- Decisions and deviations from plan
- Unresolved issues or future suggestions
