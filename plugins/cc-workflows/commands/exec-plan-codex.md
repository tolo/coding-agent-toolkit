---
description: Executes an implementation plan through Agent Teams, delegating coding and review to Codex CLI instances
argument-hint: <path-to-plan-directory>
---

# Execute Plan with Codex CLI Delegation

Execute ALL stories in an implementation plan (from `/cc-workflows:plan`) through a parallelized Agent Team pipeline: **spec → exec-spec → review-gap** per story.

**Hybrid model**: Claude Code Agent Teams handle orchestration and spec creation. **Codex CLI** handles implementation and review — launched as headless subprocesses via `codex exec`.

**Uses Agent Teams** — Falls back to sequential execution if Teams unavailable.

**Requires**:
- `codex` CLI installed and authenticated (`OPENAI_API_KEY` set or `codex login` completed)
- Simple-commands installed as Codex prompts (accessible via `/prompts:<command_name>`, e.g. `/prompts:exec-spec`, `/prompts:review-gap`, `/prompts:troubleshoot`)


## Variables
PLAN_DIR: $ARGUMENTS


## Usage

```
/exec-plan-codex PLAN_DIR="path/to/plan"
```


## Instructions

Make sure `PLAN_DIR` is provided — otherwise **STOP** immediately and ask the user to provide the path to the plan directory.

### Core Rules
- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section in CLAUDE.md (and/or system prompt) before starting work, including but not limited to:
  - **Foundational Rules and Guardrails** (absolute must-follow rules)
  - **Foundational Development Guidelines and Standards** (e.g. Development, Architecture, UI/UX Guidelines etc.)
- **Complete Implementation**: All stories in plan must be implemented
- **Plan is source of truth** — follow phase ordering, dependencies, and parallel markers exactly
- **Agent Team for pipeline** — use Agent Teams for parallel story execution
- **Per-story pipeline**: spec → exec-spec → review-gap (with fix loop)
- **Codex for coding** — Implementers, Reviewers, and Troubleshooters delegate to `codex exec`

### Orchestrator Role
**You are the orchestrator.** Your job is to:
- Parse the plan and extract stories, phases, dependencies, parallel markers
- Size and create the Agent Team
- Create pipeline tasks with correct dependency chains
- Monitor progress via TaskList and coordinate agents
- Handle failures and escalate when needed
- Run final verification after all stories complete

**You do NOT:**
- Write implementation code directly
- Let your context get bloated with implementation details
- Skip final verification due to context exhaustion


## Codex CLI Reference

### Invocation Pattern

All Codex work uses the `exec` subcommand (non-interactive, headless mode):

```bash
codex exec \
  -C <working-directory> \
  --full-auto \
  -o <output-file> \
  "<prompt>"
```

### Key Flags
| Flag | Purpose |
|---|---|
| `exec` | Non-interactive / headless mode (required) |
| `-C <dir>` | Set working directory |
| `--full-auto` | Auto-approve commands, sandbox to workspace writes |
| `-o <file>` | Write agent's final message to file |
| `--json` | Emit JSONL events to stdout (for progress monitoring) |
| `--ephemeral` | Don't persist session files |
| `--color never` | Disable ANSI colors (clean output capture) |

### Prompt Commands
The simple-commands are pre-installed as Codex prompts, invocable via `/prompts:<name>`:
- `/prompts:exec-spec <path-to-fis>` — execute a Feature Implementation Specification
- `/prompts:review-gap <context>` — gap analysis / review against requirements
- `/prompts:review-code <context>` — code review
- `/prompts:troubleshoot <scope>` — systematic troubleshooting and root cause analysis

### Context Injection
- Codex automatically reads `AGENTS.md` files in the project root — use this for persistent project context
- Task-specific instructions go in the prompt string or via `/prompts:` commands
- Use `--image <file>` to attach screenshots for visual context


## Workflow

### Step 1: Preflight Checks

1. Verify Agent Teams available (`TeamCreate` tool exists)
2. Verify Codex CLI installed: run `codex --version`
3. Verify Codex authenticated: run `codex exec -C /tmp "echo hello"` (quick smoke test)

If Agent Teams unavailable:
- Inform user: requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
- Suggest manual alternative: `/cc-workflows:spec` → run codex exec for implementation → run codex exec for review, per story
- Exit

If Codex unavailable:
- Inform user: `npm install -g @openai/codex` or `brew install --cask codex`
- Suggest falling back to standard `/cc-workflows:exec-plan` (all Claude Code)
- Exit

**Gate**: Agent Teams and Codex CLI confirmed available


### Step 2: Parse Plan

1. Read `PLAN_DIR/plan.md`
2. If plan file missing, **STOP** and recommend `/cc-workflows:plan` first
3. Extract:
   - **Stories**: ID, name, scope, acceptance criteria, dependencies
   - **Phases**: Phase groupings and execution order
   - **Parallel markers**: `[P]` flags for concurrent execution
   - **Dependencies**: Cross-story dependency graph
4. Build execution plan respecting phase ordering and dependency chains

**Gate**: Plan parsed and phases identified


### Step 3: Size Team

Scale team based on total story count:

| Plan Size | Stories | Spec Creators | Codex Implementers | Codex Reviewers | Total |
|---|---|---|---|---|---|
| Small | 1-4 | 1 | 1 | 1 | 3 |
| Medium | 5-10 | 2 | 2 | 2 | 6 |
| Large | 11+ | 3 | 3 | 2 | 8 |

**Gate**: Team sized based on story count


### Step 4: Create Team and Spawn Agents

**IMPORTANT — Use Agent Team tools, NOT regular sub-agents.**
You MUST use the `TeamCreate` tool. Do NOT use `Task` alone (without `team_name`).

**Required tool sequence:**
1. `TeamCreate` — Create the team (e.g., `team_name: "codex-pipeline"`)
2. `Task` with `team_name` param — Spawn each teammate INTO the team
3. `TaskCreate` — Create pipeline tasks per phase (in Step 5)
4. `TaskUpdate` — Set dependencies, assignments, track completion
5. `SendMessage` — Inter-agent coordination
6. `SendMessage(type: "shutdown_request")` — Graceful shutdown when done
7. `TeamDelete` — Clean up team resources

#### Agent Roles

**Spec Creators** — Claim `spec-{story_id}` tasks and run `/cc-workflows:spec` with story scope as input. Output: FIS document. *(Runs natively in Claude Code — no Codex delegation.)*

**Codex Implementers** — Claim `impl-{story_id}` tasks (blocked by corresponding spec task). Delegate implementation to Codex CLI. Output: implemented story. See **Codex Implementer Protocol** below.

**Codex Reviewers** — Claim `review-{story_id}` tasks (blocked by corresponding impl task). Delegate review to Codex CLI. If issues found: delegate fixes to Codex, then re-validate. **Max 2 fix attempts** — escalate to orchestrator if issues persist. See **Codex Reviewer Protocol** below.

Each agent loops: **claim task → execute (via Codex) → mark done → claim next**.

**Troubleshooter (on-demand)** — NOT spawned upfront. Orchestrator spawns when an agent escalates. Delegates diagnosis and fixes to Codex CLI. See **Codex Troubleshooter Protocol** below. Shut down after resolution.


### Codex Implementer Protocol

The Implementer agent is a Claude Code teammate that delegates coding work to Codex CLI.

**Prerequisite**: The `exec-spec` simple-command is installed as a Codex prompt (`/prompts:exec-spec`).

**Workflow per claimed task:**

1. **Read the FIS** for the story (generated by Spec Creator) — note the file path
2. **Launch Codex** with the installed prompt command:
   ```bash
   codex exec \
     -C <project-root> \
     --full-auto \
     -o .agent_temp/codex-impl-{story_id}.md \
     --color never \
     "/prompts:exec-spec <path-to-fis>"
   ```
3. **Read the output file** (`.agent_temp/codex-impl-{story_id}.md`) to check Codex's completion report
4. **Verify basic success** — check that expected files were created/modified (quick `git status` or `git diff --stat`)
5. **Report result** — mark task complete via TaskUpdate, or escalate via SendMessage if Codex failed


### Codex Reviewer Protocol

The Reviewer agent is a Claude Code teammate that delegates review work to Codex CLI.

**Prerequisite**: The `review-gap` simple-command is installed as a Codex prompt (`/prompts:review-gap`).

**Workflow per claimed task:**

1. **Identify what to review** — read the story scope, FIS, and check `git diff` for what was implemented
2. **Launch Codex for review** with the installed prompt command:
   ```bash
   codex exec \
     -C <project-root> \
     --full-auto \
     -o .agent_temp/codex-review-{story_id}.md \
     --color never \
     "/prompts:review-gap Story {story_id}: {story_name}. FIS: {path-to-fis}"
   ```
3. **Read the review output** and assess findings:
   - If **no issues**: mark task complete
   - If **issues found**: proceed to fix loop (below)

**Fix loop** (max 2 attempts):
1. Prepare a targeted fix prompt with the specific issues from the review
2. Launch Codex to fix:
   ```bash
   codex exec \
     -C <project-root> \
     --full-auto \
     -o .agent_temp/codex-fix-{story_id}-{attempt}.md \
     --color never \
     "Fix the following issues found during review of story {story_id}:\n{issues_from_review}\n\nRefer to FIS at {path-to-fis} for requirements."
   ```
3. Re-run review via Codex (`/prompts:review-gap`)
4. If issues persist after 2 fix attempts → escalate to orchestrator via SendMessage


### Codex Troubleshooter Protocol

Spawned on-demand when an agent escalates an issue.

**Prerequisite**: The `troubleshoot` simple-command is installed as a Codex prompt (`/prompts:troubleshoot`).

**Workflow:**
1. **Receive issue context** from orchestrator (error messages, failing tests, conflict details)
2. **Launch Codex to diagnose and fix**:
   ```bash
   codex exec \
     -C <project-root> \
     --full-auto \
     -o .agent_temp/codex-troubleshoot-{story_id}.md \
     --color never \
     "/prompts:troubleshoot {scope_description_with_issue_context}"
   ```
3. **Read result** — verify the fix resolves the issue (run build/tests)
4. **Report resolution** or escalate to user if Codex also fails


#### Spawn Templates

**Spec Creator** — spawned via `Task(team_name: "codex-pipeline", name: "spec-N", ...)`:
```
Role: Spec Creator
Team: codex-pipeline
Plan: {PLAN_DIR}/plan.md

Your workflow (loop until no tasks remain):
1. Check TaskList for available `spec-*` tasks
2. Claim an unblocked, unassigned task via TaskUpdate
3. Run /cc-workflows:spec with the story scope from plan. Save FIS to docs/specs/
4. Mark task completed via TaskUpdate
5. Check TaskList for next available task
6. If no tasks available, notify orchestrator via SendMessage

Important:
- Read the Workflow Rules, Guardrails and Guidelines in CLAUDE.md before starting
- Follow existing codebase patterns
- For issues you cannot resolve, escalate to orchestrator via SendMessage
```

**Codex Implementer** — spawned via `Task(team_name: "codex-pipeline", name: "impl-N", ...)`:
```
Role: Codex Implementer
Team: codex-pipeline
Plan: {PLAN_DIR}/plan.md

You delegate implementation work to Codex CLI via /prompts:exec-spec. Follow the Codex Implementer Protocol.

Your workflow (loop until no tasks remain):
1. Check TaskList for available `impl-*` tasks
2. Claim an unblocked, unassigned task via TaskUpdate
3. Read the FIS generated by the Spec Creator for this story — note the file path
4. Launch: codex exec -C <project-root> --full-auto -o .agent_temp/codex-impl-{story_id}.md --color never "/prompts:exec-spec <path-to-fis>"
5. Read the output, verify files were changed (git status/diff --stat)
6. Mark task completed via TaskUpdate (or escalate if Codex failed)
7. Check TaskList for next available task
8. If no tasks available, notify orchestrator via SendMessage

Important:
- Codex uses /prompts:exec-spec which references the FIS by path — Codex reads it internally
- Check git status after Codex completes to verify changes were made
- If Codex exits with errors or makes no changes, escalate via SendMessage
- Read the Workflow Rules, Guardrails and Guidelines in CLAUDE.md before starting
```

**Codex Reviewer** — spawned via `Task(team_name: "codex-pipeline", name: "review-N", ...)`:
```
Role: Codex Reviewer
Team: codex-pipeline
Plan: {PLAN_DIR}/plan.md

You delegate review and fix work to Codex CLI via /prompts:review-gap. Follow the Codex Reviewer Protocol.

Your workflow (loop until no tasks remain):
1. Check TaskList for available `review-*` tasks
2. Claim an unblocked, unassigned task via TaskUpdate
3. Gather review context: story scope, FIS path
4. Launch review: codex exec -C <project-root> --full-auto -o .agent_temp/codex-review-{story_id}.md --color never "/prompts:review-gap Story {story_id}: {story_name}. FIS: {path-to-fis}"
5. Read review output. If PASS → mark complete. If FAIL → enter fix loop:
   a. Launch fix: codex exec ... -o .agent_temp/codex-fix-{story_id}-{N}.md "<fix_prompt_with_issues>"
   b. Re-launch review via /prompts:review-gap. Max 2 fix attempts.
   c. If still failing → escalate to orchestrator via SendMessage
6. Mark task completed via TaskUpdate
7. Check TaskList for next available task
8. If no tasks available, notify orchestrator via SendMessage

Important:
- Codex uses /prompts:review-gap which performs the full gap analysis workflow
- Read the actual review output file to determine PASS/FAIL
- If Codex review is inconclusive, do a quick manual check before marking complete
- Read the Workflow Rules, Guardrails and Guidelines in CLAUDE.md before starting
```

**Gate**: Team created and all agents spawned


### Step 5: Phase Loop

For each phase in the plan:

#### 5a. Create Pipeline Tasks

For each story in the current phase, create 3 tasks:
- `spec-{story_id}`: "Create FIS for {story_name}"
- `impl-{story_id}`: "Implement {story_name} (via Codex)"
- `review-{story_id}`: "Review and validate {story_name} (via Codex)"

#### 5b. Set Dependencies

Use `TaskUpdate(addBlockedBy)`:
- `impl-{story_id}` blocked by `spec-{story_id}`
- `review-{story_id}` blocked by `impl-{story_id}`
- Cross-story dependencies from plan: if S05 depends on S03, then `spec-S05` blocked by `review-S03`

#### 5c. Monitor Progress

- Poll `TaskList` periodically until all review tasks for the current phase are complete
- Handle agent messages (failures, questions, status updates)
- **Watch for Codex failures** — if an agent reports Codex exit errors or no-change results, consider spawning troubleshooter

#### 5d. Update Plan

After each story's pipeline completes (spec → impl → review), update `plan.md`:
- Set the story's **Status** field to `Done`
- Set the story's **FIS** field to the generated spec path (e.g. `**FIS**: docs/specs/story-name.md`)
- Check off completed acceptance criteria checkboxes (`- [ ]` → `- [x]`)
- Update the Story Catalog table: set the story's Status column to `Done`

Also update each completed FIS file:
- Mark all task checkboxes as checked (`- [x]`)
- Mark success criteria and Final Validation Checklist items as checked

Move to next phase only after ALL stories in current phase are complete and plan is updated.

**Create Phase N+1 tasks only after Phase N is fully complete.**

**Gate**: All stories in current phase completed and verified

#### Pipeline Flow Example

```
Phase 1 (Sequential): S01 → S02
  spec-S01(claude) → impl-S01(codex) → review-S01(codex) → spec-S02(claude) → impl-S02(codex) → review-S02(codex)

Phase 2 (Parallel [P]): S03[P], S04[P], S05 (depends on S03)
  spec-S03(claude) → impl-S03(codex) → review-S03(codex) → spec-S05(claude) → impl-S05(codex) → review-S05(codex)
  spec-S04(claude) → impl-S04(codex) → review-S04(codex)   (parallel with S03)
```

**Gate**: All phases complete, all stories implemented and reviewed


### Step 6: Final Verification

**Orchestrator performs directly** (not delegated):

1. Run build — verify it succeeds
2. Run tests — verify all pass
3. Review overall integration across stories
4. Include verification evidence in completion summary:
   - **Build**: exit code or success/failure status
   - **Tests**: pass/fail counts (e.g., "42/42 pass")
   - **Linting/types**: error and warning counts

**Gate**: Build, tests, and integration verification all pass


### Step 7: Documentation Update

Spawn a **general-purpose sub-agent** to update project documentation. Scope the update to:
- **README**: reflect any new features, changed APIs, or updated setup steps from the implementation
- **CHANGELOG**: add entries for all implemented stories (following existing changelog format)
- **Affected docs**: update any documentation files directly referenced or impacted by the plan's changes

**Gate**: Documentation updated


### Step 8: Clean Up

1. Use `SendMessage(type: "shutdown_request")` for each teammate
2. Wait for shutdown confirmations
3. Use `TeamDelete` to remove team and task files
4. Clean up Codex output files: `rm .agent_temp/codex-*.md` (if any remain)


## Failure Handling

- **Codex process fails** (non-zero exit, timeout, no changes made) → Implementer/Reviewer agent escalates via `SendMessage` with Codex output → orchestrator spawns **on-demand Troubleshooter** teammate → Troubleshooter delegates fix to Codex → shuts down after resolution → escalates to user only if Troubleshooter also fails
- **Dependent stories stay blocked** when a predecessor fails
- **If >50% of a phase fails** → pause execution, notify user with failure summary
- **Codex authentication failure** → stop immediately, ask user to run `codex login` or set `OPENAI_API_KEY`


## Fallback: No Agent Teams

If Agent Teams unavailable (Step 1 check fails), suggest the manual equivalent:

```bash
# For each story in plan order:
/cc-workflows:spec "S01: [Story Name]"
# Then delegate to Codex:
codex exec -C . --full-auto -o .agent_temp/codex-impl-S01.md "/prompts:exec-spec docs/specs/story-name.md"
codex exec -C . --full-auto -o .agent_temp/codex-review-S01.md "/prompts:review-gap Story S01. FIS: docs/specs/story-name.md"
# ... repeat for each story
```


## Fallback: No Codex CLI

If Codex unavailable (Step 1 check fails), suggest the standard Claude Code alternative:

```bash
/cc-workflows:exec-plan PLAN_DIR="path/to/plan"
```
