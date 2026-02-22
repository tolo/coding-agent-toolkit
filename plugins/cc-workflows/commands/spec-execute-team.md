---
description: Executes a Feature Implementation Specification with Agent Team-based validation (validate-fix loop)
argument-hint: <path-to-fis>
---

# Execute FIS with Agent Team Validation

Execute a fully-defined FIS document as an **orchestrator**, delegating implementation to sub-agents and validation to an **Agent Team** (Validation Council) that reviews, debates, fixes, and re-validates in a loop until clean.

**Uses Agent Teams** - Falls back to `/spec-execute` if Teams unavailable.


## Variables
FIS_FILE_PATH: $ARGUMENTS


## Instructions

### Core Rules
- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section in CLAUDE.md (and/or system prompt) before starting work, including but not limited to:
  - **Foundational Rules and Guardrails** (absolute must-follow rules)
  - **Foundational Development Guidelines and Standards** (e.g. Development, Architecture, UI/UX Guidelines etc.)
- **Complete Implementation**: 100% completion required - no partial work
- **FIS is source of truth** — follow it exactly
- **Sub-agents for implementation** — delegate all implementation tasks to sub-agents
- **Agent Team for validation** — use a Validation Council for all validation work

### Orchestrator Role
**You are the orchestrator.** Your job is to:
- Load and understand the FIS
- Delegate ALL implementation tasks to sub-agents (Steps 2-3)
- Create and coordinate the Validation Council (Agent Team) for validation (Step 4)
- Ensure final validation checklist is complete

**You do NOT:**
- Write implementation code directly
- Let your context get bloated with implementation details
- Skip final steps due to context exhaustion

**Context Injection Best Practice:**
Before spawning each sub-agent, prefer extracting the relevant task text, key references,
and ADR decision from the FIS and passing them directly in the prompt. This ensures
sub-agents get exactly the context they need without re-reading the full FIS independently.
When tasks are simple or context is small, referencing the FIS path is acceptable.

## Workflow

### Step 1: Check Agent Teams Availability

If Agent Teams not available (experimental feature not enabled):
- Inform user that spec-execute-team requires Agent Teams
- Automatically fall back to `/spec-execute` with same arguments
- Exit

### Step 2: Load FIS and Prepare
1. Read FIS at _`FIS_FILE_PATH`_
2. Fully understand: Success Criteria, Scope & Boundaries, Solution Architecture, Critical Documentation & Context, Implementation Plan
3. Analyse codebase structure (`tree -d`, `git ls-files | head -250`)
4. Read any _`fis-implementation-notes.md`_ for previous learnings
5. Create task tracking for ALL tasks (implementation + validation)

### Step 3: Execute Implementation Tasks

For each implementation task (TI01, TI02, etc.) — **identical to spec-execute**:

**Sequential tasks:**
- Spawn sub-agents (foreground) with Input Template (see below)
- Wait for result, process output, update FIS, track context

**Parallel tasks [P]:**
- Spawn parallel sub-agents (foreground)
- Ensure no file conflicts
- Collect all results, update FIS

**Sub-agent selection:**
- Default: `general-purpose` agent
- Build issues: `cc-workflows:build-troubleshooter`
- UI work: `cc-workflows:ui-ux-designer`
- Complex architecture: `cc-workflows:solution-architect`

Follow the **Sub-Agent Protocol** (Input Template, Expected Output, Handling Results) defined in `spec-execute`.

### Step 4: Create and Run Validation Council

Create an Agent Team with the following members, mapped to FIS validation tasks:

#### Council Composition

**Core Validators (mapped to TV0X):**

| Member | Maps to | Responsibility |
|---|---|---|
| **Code Reviewer** | TV01 | Use `/cc-workflows:review-code` skill. Static analysis, linting, formatting, type checking, code quality, architecture, security (OWASP Top 10), UI/UX review |
| **QA Test Engineer** | TV02 | Run and verify unit, integration, E2E tests. Assess coverage. Write missing tests for new functionality |
| **Visual Validator** | TV03 | Screenshot comparison, design compliance, regression detection. Follow Visual Validation Workflow from CLAUDE.md. _Only include if FIS has UI changes_ |

**Enhanced Validators:**

| Member | Responsibility |
|---|---|
| **Requirements Verifier** | Check implementation against FIS success criteria, acceptance criteria, scope boundaries. Verify no scope creep or missed requirements |
| **Devil's Advocate** | Challenge ALL findings from other validators. Ask "is this actually a problem?" Question severity ratings. Filter false positives. Max 2-3 debate rounds per finding |
| **Synthesis Challenger** | After debates: review all findings holistically. Check severity consistency, find patterns, merge related issues, catch false positives in context. Quality gate |
| **Issue Resolver** | Fix all validated issues that survive debate. Report changes made. Must follow existing codebase patterns |

**Selection logic:**
- Always include: Code Reviewer, QA Test Engineer, Requirements Verifier, Devil's Advocate, Synthesis Challenger, Issue Resolver (6 minimum)
- Add Visual Validator only if FIS contains UI changes (7 members)

#### Council Composition Template

Provide this when creating the Agent Team:

```
Create a Validation Council team with {N} members for FIS: {FIS_FILE_PATH}

Selected members:
{List each member with their responsibilities from the table above}

FIS context:
- Success criteria: {list from FIS}
- Scope: {brief summary}
- Implementation tasks completed: {list TI task IDs}
- Files changed during implementation: {consolidated list from sub-agent outputs}

Validation process (three phases + fix loop):

PHASE 1 - Specialist Validation:
Each core validator works in parallel through their specialized lens:
- Code Reviewer: Run /cc-workflows:review-code skill, report findings with severity (CRITICAL/HIGH/MEDIUM/LOW) and file:line references
- QA Test Engineer: Execute all tests, assess coverage, write missing tests, report failures and gaps
- Visual Validator (if UI): Capture screenshots, compare against design specs, check for regressions
- Requirements Verifier: Check each success criterion, verify acceptance criteria met, check scope boundaries

PHASE 2 - Adversarial Debate:
Devil's Advocate:
- Challenge ALL findings from Phase 1
- Ask "why is this actually a problem?"
- Question assumptions and severity ratings
- Force validation through debate (max 2-3 rounds per finding)
- If no consensus after 3 rounds, mark as "disputed"

Synthesis Challenger (after all debates):
- Review ALL validated findings holistically
- Question: "Are severity ratings consistent across findings?"
- Question: "Are multiple related findings actually one larger issue?"
- Question: "Did we miss patterns or systemic issues?"
- Question: "Are any validated findings actually false positives in context?"
- Act as quality gate — only findings surviving both phases get fixed

PHASE 3 - Fix-Validate Loop (max {MAX_ITERATIONS} iterations):
Issue Resolver:
- Receive list of validated findings (survived Phase 1+2)
- Fix each issue, following existing codebase patterns
- Report: files changed, what was fixed, any decisions made

Re-validation (scoped to changed files only):
- Affected validators (Code Reviewer, QA, Visual if applicable) re-check ONLY files changed by Issue Resolver
- Synthesis Challenger confirms fixes are correct and no new issues introduced
- NO full Devil's Advocate debate in re-validation (lightweight check only)

Loop exit conditions:
- ✅ Clean: No issues remain → exit loop, report success
- ✅ Max iterations reached → exit loop, report remaining issues to orchestrator
- ✅ No convergence: Same or more issues than previous iteration → exit loop, flag to orchestrator

Final output: Unified validation report with all findings, fixes applied, and remaining issues (if any).
```

#### Configuration

| Setting | Value | Rationale |
|---|---|---|
| MAX_ITERATIONS | 3 | Hard cap on fix-validate cycles to prevent runaway loops |

#### Handling Council Results

After the Validation Council completes:
1. **Read the unified report** — extract validated findings, fixes applied, remaining issues
2. **Update FIS** — check off validation task checkboxes based on results (TV01-TV03 map to council validators, TV04 is covered by the Issue Resolver)
3. **If remaining issues exist** — assess severity:
   - CRITICAL/HIGH: Flag to user, do not proceed
   - MEDIUM/LOW: Log in report, proceed with orchestrator verification

### Step 5: Final Quality Assurance
As orchestrator (not delegated):
- Review Validation Council results
- Check for functionality gaps or requirement mismatches
- Use `code-simplifier:code-simplifier` agent to look for simplification and quality improvement opportunities

### Step 6: Verify Completion
**Orchestrator performs directly:**
1. Verify ALL success criteria in FIS are met
2. Verify ALL task checkboxes marked complete (- [x])
3. Verify Final Validation Checklist items are satisfied
4. Update FIS with completion status
5. Include verification evidence in completion summary (as applicable):
   - **Build**: exit code or success/failure status
   - **Tests**: pass/fail counts (e.g., "42/42 pass")
   - **Linting/types**: error and warning counts
   - **Visual validation**: screenshot confirming UI matches expectations (if UI)
   - **Runtime**: confirmation app starts and key flows work

### Step 7: Iteration (if needed)
If success criteria not met or verification failed:
1. Analyze gaps from validation feedback
2. Create new tasks for fixes
3. Execute Steps 3-6 again

### Step 8: Clean Up
Request graceful shutdown of all Validation Council members and clean up team resources.


## Report: Update Implementation Notes

After completion, update `fis-implementation-notes.md` with important implementation notes (concise, no unnecessary verbosity):
- Brief description of what was implemented and how parts integrate
- Key challenges faced and how they were overcome
- Important decisions made and their rationale
- Deviations from plan
- Validation Council findings summary (what was caught and fixed)
- Unresolved issues or future suggestions
