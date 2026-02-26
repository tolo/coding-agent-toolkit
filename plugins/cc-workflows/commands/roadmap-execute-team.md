---
description: Executes an entire implementation roadmap through an Agent Team pipeline (spec-create → spec-execute → review-gap per story)
argument-hint: <path-to-roadmap-directory>
---

# Execute Roadmap with Agent Team Pipeline

Execute ALL stories in an implementation roadmap (from `/cc-workflows:roadmap`) through a parallelized Agent Team pipeline: **spec-create → spec-execute → review-gap** per story.

**Uses Agent Teams** — Falls back to sequential execution (manual per-story loop) if Teams unavailable.


## Variables
ROADMAP_DIR: $ARGUMENTS


## Instructions

### Core Rules
- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section in CLAUDE.md (and/or system prompt) before starting work, including but not limited to:
  - **Foundational Rules and Guardrails** (absolute must-follow rules)
  - **Foundational Development Guidelines and Standards** (e.g. Development, Architecture, UI/UX Guidelines etc.)
- **Complete Implementation**: All stories in roadmap must be implemented
- **Roadmap is source of truth** — follow phase ordering, dependencies, and parallel markers exactly
- **Agent Team for pipeline** — use Agent Teams for parallel story execution
- **Per-story pipeline**: spec-create → spec-execute → review-gap (with fix loop)

### Orchestrator Role
**You are the orchestrator.** Your job is to:
- Parse the roadmap and extract stories, phases, dependencies, parallel markers
- Size and create the Agent Team
- Create pipeline tasks with correct dependency chains
- Monitor progress via TaskList and coordinate agents
- Handle failures and escalate when needed
- Run final verification after all stories complete

**You do NOT:**
- Write implementation code directly
- Let your context get bloated with implementation details
- Skip final verification due to context exhaustion


## Workflow

### Step 1: Check Agent Teams Availability

Verify Agent Teams are available by checking that the `TeamCreate` tool exists in your available tools.

If the `TeamCreate` tool is NOT available (experimental feature not enabled):
- Inform user that roadmap-execute-team requires Agent Teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)
- Suggest manual alternative: execute stories sequentially with `/cc-workflows:spec-create` → `/cc-workflows:spec-execute` → `/cc-workflows:review-gap` per story
- Exit


### Step 2: Parse Roadmap

1. Read `ROADMAP_DIR/roadmap.md`
2. If roadmap file missing, **STOP** and recommend `/cc-workflows:roadmap` first
3. Extract:
   - **Stories**: ID, name, scope, acceptance criteria, dependencies
   - **Phases**: Phase groupings and execution order
   - **Parallel markers**: `[P]` flags for concurrent execution
   - **Dependencies**: Cross-story dependency graph
4. Build execution plan respecting phase ordering and dependency chains


### Step 3: Size Team

Scale team based on total story count:

| Roadmap Size | Stories | Spec Creators | Implementers | Reviewers | Total |
|---|---|---|---|---|---|
| Small | 1-4 | 1 | 1 | 1 | 3 |
| Medium | 5-10 | 2 | 2 | 2 | 6 |
| Large | 11+ | 3 | 3 | 2 | 8 |


### Step 4: Create Team and Spawn Agents

**IMPORTANT — Use Agent Team tools, NOT regular sub-agents.**
You MUST use the `TeamCreate` tool. Do NOT use `Task` alone (without `team_name`).

**Required tool sequence:**
1. `TeamCreate` — Create the team (e.g., `team_name: "roadmap-pipeline"`)
2. `TaskCreate` — Create pipeline tasks per story
3. `Task` with `team_name` param — Spawn each teammate INTO the team
4. `TaskUpdate` — Set dependencies, assignments, track completion
5. `SendMessage` — Inter-agent coordination
6. `SendMessage(type: "shutdown_request")` — Graceful shutdown when done
7. `TeamDelete` — Clean up team resources

#### Agent Roles

**Spec Creators** — Claim `spec-{story_id}` tasks and run `/cc-workflows:spec-create` with story scope as input. Output: FIS document.

**Implementers** — Claim `impl-{story_id}` tasks (blocked by corresponding spec task) and run `/cc-workflows:spec-execute` on the generated FIS. Output: implemented story.

**Reviewers** — Claim `review-{story_id}` tasks (blocked by corresponding impl task) and run `/cc-workflows:review-gap` per story. If issues found: fix them, then re-validate. Output: validated story.

Each agent loops: **claim task → execute → mark done → claim next**.

#### Spawn Template

Use this as prompt context when spawning each teammate via `Task(team_name: "roadmap-pipeline", name: "<role-N>", ...)`:

```
Role: {Spec Creator | Implementer | Reviewer}
Team: roadmap-pipeline
Roadmap: {ROADMAP_DIR}/roadmap.md

Your workflow (loop until no tasks remain):
1. Check TaskList for available tasks matching your role ({spec-*|impl-*|review-*})
2. Claim an unblocked, unassigned task via TaskUpdate (set owner to your name)
3. Execute:
   - Spec Creator: Run /cc-workflows:spec-create with story scope from roadmap. Save FIS to {ROADMAP_DIR}/
   - Implementer: Run /cc-workflows:spec-execute on the FIS for this story
   - Reviewer: Run /cc-workflows:review-gap for this story. Fix any issues found, then re-validate
4. Mark task completed via TaskUpdate
5. Check TaskList for next available task
6. If no tasks available, notify orchestrator via SendMessage

Important:
- Read the Workflow Rules, Guardrails and Guidelines in CLAUDE.md before starting
- Follow existing codebase patterns
- Report failures immediately via SendMessage to orchestrator
```


### Step 5: Phase Loop

For each phase in the roadmap:

#### 5a. Create Pipeline Tasks

For each story in the current phase, create 3 tasks:
- `spec-{story_id}`: "Create FIS for {story_name}"
- `impl-{story_id}`: "Implement {story_name}"
- `review-{story_id}`: "Review and validate {story_name}"

#### 5b. Set Dependencies

Use `TaskUpdate(addBlockedBy)`:
- `impl-{story_id}` blocked by `spec-{story_id}`
- `review-{story_id}` blocked by `impl-{story_id}`
- Cross-story dependencies from roadmap: if S05 depends on S03, then `spec-S05` blocked by `review-S03`

#### 5c. Monitor Progress

- Poll `TaskList` periodically until all review tasks for the current phase are complete
- Handle agent messages (failures, questions, status updates)

#### 5d. Update Roadmap

- Check off completed story acceptance criteria in `roadmap.md`
- Move to next phase only after ALL stories in current phase are complete

**Create Phase N+1 tasks only after Phase N is fully complete.**

#### Pipeline Flow Example

```
Phase 1 (Sequential): S01 → S02
  spec-S01 → impl-S01 → review-S01 → spec-S02 → impl-S02 → review-S02

Phase 2 (Parallel [P]): S03[P], S04[P], S05 (depends on S03)
  spec-S03 → impl-S03 → review-S03 → spec-S05 → impl-S05 → review-S05
  spec-S04 → impl-S04 → review-S04   (parallel with S03)
```


### Step 6: Final Verification

**Orchestrator performs directly** (not delegated):

1. Run build — verify it succeeds
2. Run tests — verify all pass
3. Review overall integration across stories
4. Include verification evidence in completion summary:
   - **Build**: exit code or success/failure status
   - **Tests**: pass/fail counts (e.g., "42/42 pass")
   - **Linting/types**: error and warning counts


### Step 7: Documentation Update

Spawn a sub-agent to update project documentation:
- README updates (if applicable)
- Any docs referenced in the roadmap


### Step 8: Clean Up

1. Use `SendMessage(type: "shutdown_request")` for each teammate
2. Wait for shutdown confirmations
3. Use `TeamDelete` to remove team and task files


## Failure Handling

- **Agent reports failure** via `SendMessage` → orchestrator retries once with same or different agent → escalates to user if retry fails
- **Dependent stories stay blocked** when a predecessor fails
- **If >50% of a phase fails** → pause execution, notify user with failure summary
- **Build/test failures** after implementation → route to `cc-workflows:build-troubleshooter` agent


## Fallback: No Agent Teams

If Agent Teams unavailable (Step 1 check fails), suggest the manual equivalent:

```bash
# For each story in roadmap order:
/cc-workflows:spec-create "S01: [Story Name]"
/cc-workflows:spec-execute
/cc-workflows:review-gap
# ... repeat for each story
```
