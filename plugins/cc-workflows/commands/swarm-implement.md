---
description: Swarm-based feature implementation with parallel sub-agents and task tracking. Use for multi-step features, GitHub issue implementation (--issue), or spec-driven development requiring parallelization.
argument-hint: <description> | --issue <number> | <spec file path>
disable-model-invocation: true
---

# Swarm Implement

Task-driven implementation using parallel sub-agents for maximum throughput. Main agent acts as orchestrator/coordinator while sub-agents execute work concurrently.

**Key principles:**
- **Task-first**: All work tracked via TaskCreate/TaskUpdate
- **Parallelization**: Independent tasks execute via parallel sub-agents
- **Orchestration**: Main agent coordinates, delegates, never executes implementation directly
- **Verification**: Separate validation agents ensure quality


## Variables

ARGUMENTS: $ARGUMENTS


## Usage

```
/swarm-implement <feature description>        # Implement from inline description
/swarm-implement --issue 123                  # Implement from GitHub issue (auto-PR)
/swarm-implement --issue 123 --no-pr          # From issue, skip PR creation
/swarm-implement docs/specs/feature.md        # Implement from spec file
/swarm-implement <description> --pr           # Inline description + create PR
```


## Instructions

- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section in CLAUDE.md before starting work
- **Act as orchestrator** - delegate ALL implementation work to sub-agents
- **Maximize parallelization** - identify independent tasks and execute concurrently
- **Use task management** - track every piece of work via TaskCreate/TaskUpdate
- **Verify independently** - use separate sub-agents for validation vs implementation
- **NEVER STOP until complete** - this is a continuous workflow from planning through implementation to completion
- **Auto-integrate feedback** - plan review findings are automatically incorporated, not waiting for approval
- **Self-correcting** - if issues are found, fix them and continue; only stop if fundamentally blocked


## Workflow


### Phase 1: Analysis & Task Planning

#### 1.1 Parse Input & Load Requirements

**If `--issue` flag present (or ARGUMENTS refer to GitHub issue numbers):**
1. Extract issue number(s) from ARGUMENTS
2. Use `gh issue view <number>` to fetch issue details (title, body, labels, comments)
3. If issue references other issues, fetch those too for context
4. Set `CREATE_PR=true` (unless `--no-pr` specified)
5. Store issue number(s) for reference in commits/PR
6. Create feature branch: `git checkout -b feature/issue-<number>-<short-name>`

**If ARGUMENTS is a file path (spec file):**
1. Read the specification file
2. Extract requirements, scope, success criteria
3. Check if spec references GitHub issues - if so, fetch those for additional context

**If ARGUMENTS is inline text:**
1. Parse requirements from description
2. Set `CREATE_PR=true` only if `--pr` flag present
3. Clarify ambiguities if critical (otherwise proceed with reasonable assumptions)

#### 1.2 Codebase Analysis (Parallel)

Launch **parallel exploration sub-agents** (foreground, `run_in_background=false`):

```
Agent 1: "Explore project structure, identify key directories, entry points"
Agent 2: "Find existing patterns related to [feature area] - classes, conventions, styles"
Agent 3: "Identify test patterns, existing test infrastructure"
```

Synthesize findings into implementation context.

#### 1.3 Task Decomposition

Break work into **atomic tasks** using these categories:

| Category | Parallelizable | Agent Type |
|----------|----------------|------------|
| **Foundation** (setup, scaffolding) | No - sequential | general-purpose |
| **Implementation** (feature code) | Yes - parallel | general-purpose |
| **Testing** (unit tests) | Yes - parallel | qa-test-engineer |
| **Integration** (connecting parts) | Partially | general-purpose |
| **Validation** (review, QA) | Yes - parallel | code-reviewer |

**For each task, define:**
- Clear scope and deliverables
- Success criteria (how to verify completion)
- Dependencies (which tasks must complete first)
- Whether parallelizable with other tasks

#### 1.4 Create Task List

Use **TaskCreate** for EVERY task identified:

```
TaskCreate:
  subject: "Implement UserAuthService"
  description: "Create authentication service following existing service patterns in Services/. Must include: login, logout, token refresh. Success: compiles, unit tests pass."
  activeForm: "Implementing UserAuthService"
```

Then use **TaskUpdate** to set dependencies:

```
TaskUpdate:
  taskId: "2"
  addBlockedBy: ["1"]  // Task 2 depends on Task 1
```

**Output**: Complete task list with dependencies visualized via TaskList.

#### 1.5 Plan Review & Auto-Integration

Validate and automatically integrate improvements into the plan:

1. **Save plan to temporary file** for review:
   - Write task list with descriptions, dependencies, and execution order to `.agent_temp/swarm-plan-<feature>.md`

2. **Use `/review-plan` command** to validate:
   - Completeness: All requirements covered by tasks?
   - Dependencies: Correct ordering and parallelization opportunities?
   - Scope: No over-engineering or unnecessary tasks?
   - Clarity: Each task has clear success criteria?

3. **Automatically integrate review findings** (DO NOT STOP - continue immediately):
   - **Critical/High issues**: Update affected tasks via TaskUpdate (modify description, add missing tasks, fix dependencies)
   - **Medium/Low issues**: Note in task descriptions for handling during implementation
   - If review identifies missing DataService methods, missing integration details, etc. → add to relevant task descriptions

4. **Example auto-integration**:
   ```
   Review finding: "FlowEngine ↔ TimerModel integration not specified"
   Action: TaskUpdate taskId="3" description="[original] + Integration: FlowEngine.onSessionComplete called by TimerModel; FlowEngine.startNextSession() calls timerModel.start()"
   ```

**NO GATE - Continue immediately to Phase 2 after integrating findings**


### Phase 2: Parallel Execution

#### 2.1 Execution Strategy

Execute tasks in **waves** based on dependencies:

```
Wave 1: Foundation tasks (sequential or parallel if independent)
  └─ Execute via sub-agents
  └─ Wait for completion
  └─ Verify success criteria

Wave 2: Implementation tasks (parallel where possible)
  └─ Launch multiple Task calls in single message
  └─ Each sub-agent handles one task
  └─ Monitor via TaskList

Wave 3: Integration tasks
  └─ Connect implemented components
  └─ May require sequential execution

Wave 4: Validation tasks (parallel)
  └─ Code review via code-reviewer agent
  └─ Test execution via qa-test-engineer
  └─ Visual validation if UI (screenshot-validation-specialist)
```

#### 2.2 Sub-Agent Delegation Pattern

For EACH implementation task:

1. **Mark task in-progress:**
   ```
   TaskUpdate: { taskId: "X", status: "in_progress" }
   ```

2. **Launch sub-agent** with full context:
   ```
   Task:
     subagent_type: general-purpose
     description: "[Task subject]"
     prompt: |
       TASK: [Full task description from TaskGet]

       CONTEXT:
       - Project: [project info]
       - Patterns: [relevant patterns from Phase 1]
       - Dependencies: [what was completed before this]

       SUCCESS CRITERIA:
       [Specific verification steps]

       IMPORTANT:
       - Follow existing code patterns exactly
       - Run tests/linting before completing
       - Report any blockers immediately
   ```

3. **On completion, mark task done:**
   ```
   TaskUpdate: { taskId: "X", status: "completed" }
   ```

#### 2.3 Parallel Execution Rules

**DO launch parallel sub-agents when:**
- Tasks have no dependencies on each other
- Tasks modify different files/modules
- Tasks are read-only (exploration, review)

**DO NOT parallelize when:**
- Tasks modify same files (merge conflicts)
- One task depends on another's output
- Tasks involve compilation/building (resource contention)
- Tasks share test infrastructure

**Parallel launch syntax** (multiple Task calls in ONE message):
```
<Task 1: Implement FeatureA>
<Task 2: Implement FeatureB>
<Task 3: Write tests for ModuleC>
```

#### 2.4 Progress Monitoring

After each wave:
1. Run **TaskList** to see current status
2. Identify blocked tasks and their blockers
3. Handle any failed tasks before proceeding
4. Synthesize outputs from completed tasks

**If task fails:**
1. Analyze failure reason
2. Create fix task with TaskCreate
3. Set dependency on failed task
4. Re-execute with updated context


### Phase 3: Verification Wave

#### 3.1 Code Quality Validation

Launch **parallel validation sub-agents**:

```
Agent 1 (code-reviewer):
  "Review all implemented code for quality, security, patterns adherence"

Agent 2 (qa-test-engineer):
  "Run full test suite, verify coverage, identify gaps"

Agent 3 (build-troubleshooter) [if build issues]:
  "Diagnose and fix any compilation or runtime errors"
```

**CRITICAL**: Validation agents MUST be different from implementation agents for independent verification.

#### 3.2 Visual Validation (if UI changes)

Use **screenshot-validation-specialist**:
```
Task:
  subagent_type: cc-workflows:screenshot-validation-specialist
  prompt: "Validate UI changes against requirements. Capture screenshots, compare to baselines if available."
```

#### 3.3 Issue Resolution Loop

For each issue found:
1. **TaskCreate** for the fix
2. Delegate to sub-agent
3. Re-run relevant validation
4. **TaskUpdate** when resolved

#### 3.4 Implementation Review

After code-level issues are resolved, perform requirements-level validation:

1. **Use `/review-impl` command** to analyze implementation against requirements:
   - Gap analysis: functionality, integration, consistency gaps
   - Requirement mismatches
   - Holistic sanity check

2. **Evaluate review findings**:
   - **Critical/High gaps**: Create tasks, loop back to Phase 2 execution
   - **Medium/Low gaps**: Document for follow-up or fix if quick
   - **No significant gaps**: Proceed to completion

**Gate**: Implementation verified against requirements, no critical gaps remain


### Phase 4: Completion

#### 4.1 Final Status Check

1. Run **TaskList** - verify all tasks completed
2. Ensure no pending or blocked tasks remain
3. Confirm all success criteria met

#### 4.2 Summary Report

Generate completion summary:
- Tasks completed: N
- Parallel waves executed: N
- Sub-agents spawned: N
- Issues found and resolved: N
- Final verification status

#### 4.3 Commit & PR (conditional)

**Only execute if `CREATE_PR=true` or `--issue` mode or `--pr` flag:**

1. **Stage and commit changes:**
   ```bash
   git add <relevant files>
   git commit -m "feat: <description>

   <If from issue: Fixes #<number> or Closes #<number>>

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

2. **Push to remote:**
   ```bash
   git push -u origin <branch-name>
   ```

3. **Create PR using `gh pr create`:**
   - Link to issue (include "Fixes #<number>" if applicable)
   - Brief description of implementation
   - Add relevant labels from original issue
   - Include summary of parallel execution stats

**If NOT creating PR:**
- Inform user of completed changes
- Suggest next steps (manual review, PR creation, etc.)


---


## Task Management Quick Reference

### Creating Tasks
```
TaskCreate:
  subject: "Brief imperative title"
  description: "Full details, context, success criteria"
  activeForm: "Present continuous form for spinner"
```

### Setting Dependencies
```
TaskUpdate:
  taskId: "2"
  addBlockedBy: ["1"]     # Task 2 waits for Task 1
  addBlocks: ["3", "4"]   # Tasks 3,4 wait for Task 2
```

### Status Updates
```
TaskUpdate:
  taskId: "X"
  status: "in_progress"   # Starting work
  status: "completed"     # Work done
```

### Monitoring
```
TaskList                  # See all tasks, statuses, blockers
TaskGet: { taskId: "X" }  # Full details of specific task
```


## Parallelization Patterns

### Pattern 1: Feature Modules
```
[P] Task: Implement AuthModule
[P] Task: Implement DataModule
[P] Task: Implement UIComponents
    Task: Integration (depends on all above)
```

### Pattern 2: Test-Driven
```
    Task: Write failing tests
[P] Task: Implement FeatureA (depends on tests)
[P] Task: Implement FeatureB (depends on tests)
    Task: Verify all tests pass
```

### Pattern 3: Review Pipeline
```
[P] Task: Code review - security
[P] Task: Code review - patterns
[P] Task: Code review - performance
    Task: Address findings (depends on all reviews)
```


## Sub-Agent Types Reference

| Agent | Use For |
|-------|---------|
| `general-purpose` | Implementation, research, multi-step tasks |
| `Explore` | Fast codebase exploration, file discovery |
| `code-reviewer` | Code quality, security, pattern review |
| `qa-test-engineer` | Test strategy, test writing, coverage |
| `build-troubleshooter` | Build failures, dependency issues |
| `screenshot-validation-specialist` | Visual UI validation |
| `solution-architect` | Architecture decisions, design |
| `documentation-lookup` | API docs, framework references |


## Example Execution Flows

### Example 1: From GitHub Issue

```
User: /swarm-implement --issue 42

Phase 1: Analysis
├─ Fetch issue #42 via `gh issue view 42`
├─ Extract requirements from issue body
├─ Fetch linked issues mentioned in #42
├─ Create branch: feature/issue-42-user-settings
├─ [Parallel] Explore: project structure
├─ [Parallel] Explore: existing patterns
├─ [Parallel] Explore: test infrastructure
└─ Create 6 tasks with dependencies

Phase 2: Execution
├─ Wave 1: Foundation
│   └─ Task 1: Create settings model
├─ Wave 2: Implementation [Parallel]
│   ├─ Task 2: Implement settings storage
│   └─ Task 3: Implement settings UI
├─ Wave 3: Integration
│   └─ Task 4: Connect to app state
└─ Wave 4: Testing [Parallel]
    ├─ Task 5: Unit tests
    └─ Task 6: UI tests

Phase 3: Verification [Parallel]
├─ Code review agent
├─ Test execution agent
└─ Visual validation agent

Phase 4: Completion
├─ Commit: "feat: add user settings - Fixes #42"
├─ Push to origin/feature/issue-42-user-settings
└─ Create PR linked to issue #42
```

### Example 2: From Inline Description

```
User: /swarm-implement Add user authentication with OAuth

Phase 1: Analysis
├─ Parse inline requirements
├─ [Parallel] Explore: project structure
├─ [Parallel] Explore: existing auth patterns
├─ [Parallel] Explore: test infrastructure
└─ Create 8 tasks with dependencies

Phase 2: Execution
├─ Wave 1: Foundation
│   └─ Task 1: Create auth service scaffold
├─ Wave 2: Implementation [Parallel]
│   ├─ Task 2: Implement OAuth provider
│   ├─ Task 3: Implement session management
│   └─ Task 4: Implement login/logout UI
├─ Wave 3: Integration
│   └─ Task 5: Connect auth to app state
└─ Wave 4: Testing [Parallel]
    ├─ Task 6: Unit tests
    └─ Task 7: Integration tests

Phase 3: Verification [Parallel]
├─ Code review agent
├─ Test execution agent
└─ Visual validation agent

Phase 4: Completion
└─ All 8 tasks completed, changes ready for review
```
