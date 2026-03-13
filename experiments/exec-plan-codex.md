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

> **BRIGHT LINE — No Silent Fallback to Direct Implementation:**
> This command exists specifically to delegate coding/review to Codex CLI. If Codex is unavailable or fails, the correct action is to **STOP and escalate** — never to silently implement or review directly in Claude Code. Common rationalizations to reject: "Bash seems broken, I'll implement directly", "Codex failed so I'll just write the code myself", "It's faster if I do it directly". If you find yourself writing implementation code or performing reviews without `codex exec`, you are violating this command's contract. Use `/cc-workflows:exec-plan` instead if all-Claude-Code execution is desired.

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

### Step 1: Preflight — Codex CLI Availability (MANDATORY HARD GATE)

> **CRITICAL: There is NO fallback mode in this command. If any preflight check fails, you MUST stop. Do NOT silently switch to direct Claude Code implementation. Do NOT rationalize past failures. Do NOT "implement directly instead."**

Run these checks **in order**. If ANY check fails → **STOP IMMEDIATELY. Do NOT proceed to Step 2. Output the error and EXIT.**

**1a. Agent Teams check:**
- Verify `TeamCreate` tool exists in available tools
- If NOT available → STOP. Output: `"ABORT: Agent Teams not available. Enable with CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1. Use /cc-workflows:exec-plan instead."` → **EXIT.**

**1b. Shell sanity check:**
- Run: `echo "bash-ok"`
- If exit code ≠ 0 OR output does not contain `bash-ok`:
  → STOP. Output: `"ABORT: Shell environment is broken (Bash returned non-zero). Cannot invoke Codex CLI. Use /cc-workflows:exec-plan instead."` → **EXIT. Do not continue.**

**1c. Codex CLI installed:**
- Run: `codex --version`
- If exit code ≠ 0 OR output is empty:
  → STOP. Output: `"ABORT: Codex CLI not found. Install with 'npm install -g @openai/codex' or 'brew install --cask codex'."` → **EXIT. Do not continue.**
- Record the version string for the preflight confirmation.

**1d. Codex authentication:**
- Run: `codex exec -C /tmp --full-auto --ephemeral --skip-git-repo-check "echo preflight-ok"`
- If exit code ≠ 0 OR output does not contain `preflight-ok`:
  → STOP. Output: `"ABORT: Codex exec failed. Run 'codex login' or set OPENAI_API_KEY."` → **EXIT. Do not continue.**

**Only if ALL four checks pass** → output: `"Preflight passed: Codex <version> available and authenticated."` → proceed to Step 2.

**Gate**: ALL preflight checks passed — Agent Teams, Shell, Codex CLI, and Codex auth confirmed


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

> **BRIGHT LINE: You MUST NOT write implementation code yourself. ALL coding is done by Codex CLI. If Codex fails, you escalate — you do NOT implement directly.**

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
3. **Post-exec verification (MANDATORY)** — immediately after `codex exec` returns:
   - Check exit code: `echo "codex-exit: $?"`
   - Check output file exists and is non-empty: `wc -c .agent_temp/codex-impl-{story_id}.md`
   - Check that files were actually changed: `git diff --stat`
   - If exit code ≠ 0 OR output file is empty/missing OR no files changed:
     → **Do NOT implement the story yourself.**
     → **Do NOT attempt workarounds.**
     → Escalate immediately via SendMessage: `"CODEX FAILED: story={id}, exit={code}, output_bytes={N}, error={stderr snippet}"`
     → Set task status to `failed` and wait for orchestrator instructions.
4. **Read the output file** to confirm Codex's completion report looks valid
5. **Report result** via SendMessage — MUST include:
   - `codex_exit_code: <N>`
   - `codex_output_bytes: <N>`
   - `files_changed: <count>`
   - Mark task complete via TaskUpdate


### Codex Reviewer Protocol

The Reviewer agent is a Claude Code teammate that delegates review work to Codex CLI.

**Prerequisite**: The `review-gap` simple-command is installed as a Codex prompt (`/prompts:review-gap`).

> **BRIGHT LINE: You MUST NOT perform reviews yourself. ALL review work is done by Codex CLI. If Codex fails, you escalate — you do NOT manually review and mark as passed.**

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
3. **Post-exec verification (MANDATORY)** — immediately after `codex exec` returns:
   - Check exit code: `echo "codex-exit: $?"`
   - Check output file exists and is non-empty: `wc -c .agent_temp/codex-review-{story_id}.md`
   - If exit code ≠ 0 OR output file is empty/missing:
     → **Do NOT review the story yourself.**
     → Escalate immediately via SendMessage: `"CODEX FAILED: story={id}, role=review, exit={code}, output_bytes={N}"`
     → Set task status to `failed` and wait for orchestrator instructions.
4. **Read the review output** and assess findings:
   - If **no issues**: report via SendMessage with `codex_exit_code`, `codex_output_bytes`, mark task complete
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
3. **Verify fix** — same mandatory post-exec check (exit code + output file). If Codex failed → escalate, do NOT fix manually.
4. Re-run review via Codex (`/prompts:review-gap`) with same post-exec verification
5. If issues persist after 2 fix attempts → escalate to orchestrator via SendMessage


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

BRIGHT LINE: You MUST NOT write implementation code yourself. ALL coding is done by Codex CLI.
If Codex fails, you escalate — you do NOT implement directly. No exceptions.

Your workflow (loop until no tasks remain):
1. Check TaskList for available `impl-*` tasks
2. Claim an unblocked, unassigned task via TaskUpdate
3. Read the FIS generated by the Spec Creator for this story — note the file path
4. Launch: codex exec -C <project-root> --full-auto -o .agent_temp/codex-impl-{story_id}.md --color never "/prompts:exec-spec <path-to-fis>"
5. MANDATORY post-exec verification:
   - Check exit code: echo "codex-exit: $?"
   - Check output file: wc -c .agent_temp/codex-impl-{story_id}.md
   - Check files changed: git diff --stat
   - If exit ≠ 0 OR output empty OR no files changed:
     → Do NOT implement yourself. Escalate via SendMessage:
       "CODEX FAILED: story=<id>, exit=<code>, output_bytes=<N>"
     → Set task status to failed. Wait for orchestrator.
6. Report via SendMessage with: codex_exit_code, codex_output_bytes, files_changed
7. Mark task completed via TaskUpdate
8. Check TaskList for next available task
9. If no tasks available, notify orchestrator via SendMessage

Important:
- NEVER write code directly — Codex does ALL implementation
- Read the Workflow Rules, Guardrails and Guidelines in CLAUDE.md before starting
```

**Codex Reviewer** — spawned via `Task(team_name: "codex-pipeline", name: "review-N", ...)`:
```
Role: Codex Reviewer
Team: codex-pipeline
Plan: {PLAN_DIR}/plan.md

BRIGHT LINE: You MUST NOT perform reviews yourself. ALL review work is done by Codex CLI.
If Codex fails, you escalate — you do NOT manually review and mark as passed. No exceptions.

Your workflow (loop until no tasks remain):
1. Check TaskList for available `review-*` tasks
2. Claim an unblocked, unassigned task via TaskUpdate
3. Gather review context: story scope, FIS path
4. Launch review: codex exec -C <project-root> --full-auto -o .agent_temp/codex-review-{story_id}.md --color never "/prompts:review-gap Story {story_id}: {story_name}. FIS: {path-to-fis}"
5. MANDATORY post-exec verification:
   - Check exit code: echo "codex-exit: $?"
   - Check output file: wc -c .agent_temp/codex-review-{story_id}.md
   - If exit ≠ 0 OR output empty:
     → Do NOT review yourself. Escalate via SendMessage:
       "CODEX FAILED: story=<id>, role=review, exit=<code>, output_bytes=<N>"
     → Set task status to failed. Wait for orchestrator.
6. Read review output. If PASS → report with codex_exit_code, codex_output_bytes, mark complete.
   If FAIL → enter fix loop:
   a. Launch fix: codex exec ... -o .agent_temp/codex-fix-{story_id}-{N}.md "<fix_prompt>"
   b. Verify fix (same mandatory check). If Codex failed → escalate.
   c. Re-launch review via /prompts:review-gap. Max 2 fix attempts.
   d. If still failing → escalate to orchestrator via SendMessage
7. Mark task completed via TaskUpdate
8. Check TaskList for next available task
9. If no tasks available, notify orchestrator via SendMessage

Important:
- NEVER review or fix code directly — Codex does ALL review and fix work
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

#### 5c. Monitor Progress and Verify Codex Usage

- Poll `TaskList` periodically until all review tasks for the current phase are complete
- Handle agent messages (failures, questions, status updates)

**Per-story Codex verification (MANDATORY)** — before marking ANY story as Done:
- Verify Implementer reported `codex_exit_code: 0` (not just "implementation complete")
- Verify Reviewer reported `codex_exit_code: 0` (not just "review passed")
- Verify `.agent_temp/codex-impl-{story_id}.md` and `.agent_temp/codex-review-{story_id}.md` exist and are non-empty
- If any Codex evidence is missing or exit code non-zero → mark story as `failed-codex` → escalate to user with details
- **Do NOT accept "I implemented it directly" or "I reviewed it manually" from any agent — this means Codex was bypassed**

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

- **Codex process fails** (non-zero exit, timeout, no changes made) → agent MUST escalate via `SendMessage` with `CODEX FAILED:` prefix and exit code/output details → orchestrator spawns **on-demand Troubleshooter** teammate → Troubleshooter delegates fix to Codex → shuts down after resolution → escalates to user only if Troubleshooter also fails
- **Agent bypasses Codex** (reports completion without `codex_exit_code` in message) → orchestrator marks story as `failed-codex` and escalates to user
- **Codex output files missing** (`.agent_temp/codex-*.md` absent for a "completed" story) → orchestrator marks story as `unverified` and escalates to user
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
