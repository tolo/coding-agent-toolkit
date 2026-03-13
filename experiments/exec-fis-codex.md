---
description: Creates a FIS via spec, implements with Codex, dual-reviews (Claude Code + Codex), then fixes with Codex
argument-hint: <feature description or --issue N>
---

# Single-FIS Codex Pipeline

Create a Feature Implementation Specification, implement it with Codex CLI, run dual parallel reviews (Claude Code + Codex), then apply fixes with Codex.

**Pipeline**: `spec (claude) → implement (codex) → review×2 (claude + codex) → fix (codex)`

**Uses Agent Teams** for parallel review phase. Falls back to sequential if Teams unavailable.

**Requires**:
- `codex` CLI installed and authenticated (`OPENAI_API_KEY` set or `codex login` completed)
- Simple-commands installed as Codex prompts (`/prompts:exec-spec`, `/prompts:review-gap`)


## Variables
FEATURE_INPUT: $ARGUMENTS


## Usage

```
/exec-fis-codex "Add user profile page with avatar upload"
/exec-fis-codex --issue 42
/exec-fis-codex @docs/requirements/feature-x.md
```


## Instructions

Make sure `FEATURE_INPUT` is provided — otherwise **STOP** immediately and ask the user to provide the feature description.

### Core Rules
- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section in CLAUDE.md (and/or system prompt) before starting work, including but not limited to:
  - **Foundational Rules and Guardrails** (absolute must-follow rules)
  - **Foundational Development Guidelines and Standards** (e.g. Development, Architecture, UI/UX Guidelines etc.)
- **You are the orchestrator** — coordinate the pipeline, don't implement code directly
- **Codex for implementation** — all coding delegated to `codex exec`
- **Dual review model** — Claude Code and Codex review independently in parallel for broader coverage

> **BRIGHT LINE — No Silent Fallback to Direct Implementation:**
> This command delegates coding to Codex CLI. If Codex is unavailable or fails, **STOP and escalate** — never silently implement directly. Use `/cc-workflows:exec-spec` instead if all-Claude-Code execution is desired.


## Codex CLI Reference

### Invocation Pattern

```bash
codex exec \
  -C <working-directory> \
  --full-auto \
  -o <output-file> \
  --color never \
  "<prompt>"
```

### Key Flags
| Flag | Purpose |
|---|---|
| `exec` | Non-interactive / headless mode (required) |
| `-C <dir>` | Set working directory |
| `--full-auto` | Auto-approve commands, sandbox to workspace writes |
| `-o <file>` | Write agent's final message to file |
| `--color never` | Disable ANSI colors (clean output capture) |
| `--ephemeral` | Don't persist session files |

### Prompt Commands
- `/prompts:exec-spec <path-to-fis>` — execute a Feature Implementation Specification
- `/prompts:review-gap <context>` — gap analysis / review against requirements


## Workflow

### Step 1: Preflight — Codex CLI Availability (MANDATORY HARD GATE)

> **CRITICAL: No fallback mode. If any check fails → STOP. Do NOT proceed.**

Run these checks **in order**. If ANY fails → **STOP IMMEDIATELY and EXIT.**

**1a. Agent Teams check:**
- Verify `TeamCreate` tool exists in available tools
- If NOT available → STOP. Output: `"ABORT: Agent Teams not available. Enable with CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1. Use /cc-workflows:exec-spec instead."` → **EXIT.**

**1b. Shell sanity check:**
- Run: `echo "bash-ok"`
- If exit code ≠ 0 OR output does not contain `bash-ok` → STOP. Output: `"ABORT: Shell environment is broken."` → **EXIT.**

**1c. Codex CLI installed:**
- Run: `codex --version`
- If exit code ≠ 0 → STOP. Output: `"ABORT: Codex CLI not found. Install with 'npm install -g @openai/codex' or 'brew install --cask codex'."` → **EXIT.**

**1d. Codex authentication:**
- Run: `codex exec -C /tmp --full-auto --ephemeral --skip-git-repo-check "echo preflight-ok"`
- If exit code ≠ 0 OR output does not contain `preflight-ok` → STOP. Output: `"ABORT: Codex exec failed. Run 'codex login' or set OPENAI_API_KEY."` → **EXIT.**

**Only if ALL four checks pass** → output: `"Preflight passed: Codex available and authenticated."` → proceed.

**Gate**: ALL preflight checks passed


### Step 2: Create FIS

Run `/cc-workflows:spec` with `FEATURE_INPUT` as arguments.

This creates the Feature Implementation Specification and saves it to `docs/specs/{feature-name}.md`.

After spec creation:
1. Note the FIS file path (you'll need it for all subsequent steps)
2. Read the FIS to understand the scope and tasks
3. Confirm with user before proceeding to implementation

**Gate**: FIS created and path recorded


### Step 3: Create Team and Implement via Codex

#### 3a. Create Team

Use `TeamCreate` to create the team (e.g., `team_name: "fis-codex-pipeline"`).

#### 3b. Spawn Codex Implementer

Spawn a single teammate to implement the FIS via Codex CLI.

**Codex Implementer** — spawned via `Task(team_name: "fis-codex-pipeline", name: "implementer", ...)`:
```
Role: Codex Implementer
Team: fis-codex-pipeline

BRIGHT LINE: You MUST NOT write implementation code yourself. ALL coding is done by Codex CLI.
If Codex fails, you escalate — you do NOT implement directly. No exceptions.

Your task:
1. Read the FIS at {FIS_FILE_PATH} to understand the full scope
2. Ensure .agent_temp/ directory exists: mkdir -p .agent_temp
3. Launch Codex to implement:
   codex exec -C <project-root> --full-auto -o .agent_temp/codex-impl.md --color never "/prompts:exec-spec {FIS_FILE_PATH}"
4. MANDATORY post-exec verification:
   - Check exit code: echo "codex-exit: $?"
   - Check output file: wc -c .agent_temp/codex-impl.md
   - Check files changed: git diff --stat
   - If exit ≠ 0 OR output empty OR no files changed:
     → Do NOT implement yourself.
     → Report failure via SendMessage: "CODEX FAILED: exit=<code>, output_bytes=<N>"
     → Wait for orchestrator.
5. Read the output file to confirm completion looks valid
6. Report via SendMessage with: codex_exit_code, codex_output_bytes, files_changed
7. Mark task complete

Important:
- NEVER write code directly — Codex does ALL implementation
- Read the Workflow Rules, Guardrails and Guidelines in CLAUDE.md before starting
```

#### 3c. Monitor Implementation

- Wait for the implementer to complete
- Verify Codex evidence:
  - `codex_exit_code: 0` reported
  - `.agent_temp/codex-impl.md` exists and is non-empty
  - Files were actually changed
- If Codex evidence missing → mark as failed → escalate to user

**Gate**: Implementation complete and Codex-verified


### Step 4: Dual Parallel Reviews

Spawn **two review teammates in parallel** — one using Claude Code natively, one delegating to Codex CLI.

#### 4a. Claude Code Reviewer

**Claude Code Reviewer** — spawned via `Task(team_name: "fis-codex-pipeline", name: "reviewer-claude", ...)`:
```
Role: Claude Code Reviewer
Team: fis-codex-pipeline

Your task: Perform a comprehensive gap analysis review using Claude Code.

1. Run /cc-workflows:review-gap with context:
   "FIS: {FIS_FILE_PATH} — Review the implementation against the FIS requirements."
2. The review command will generate a report in .agent_temp/reviews/
3. Read the generated report
4. Report findings via SendMessage — include:
   - report_path: path to the generated review report
   - overall_assessment: pass/fail
   - critical_issues: count
   - high_issues: count
   - summary: brief description of key findings
5. Mark task complete

Important:
- This is a READ-ONLY review — do NOT make any code changes
- Be thorough — this review complements the Codex review for broader coverage
- Read the Workflow Rules, Guardrails and Guidelines in CLAUDE.md before starting
```

#### 4b. Codex CLI Reviewer

**Codex Reviewer** — spawned via `Task(team_name: "fis-codex-pipeline", name: "reviewer-codex", ...)`:
```
Role: Codex Reviewer
Team: fis-codex-pipeline

BRIGHT LINE: You MUST NOT perform reviews yourself. ALL review work is done by Codex CLI.
If Codex fails, you escalate — you do NOT manually review. No exceptions.

Your task: Perform a gap analysis review by delegating to Codex CLI.

1. Ensure .agent_temp/ directory exists: mkdir -p .agent_temp
2. Launch Codex for review:
   codex exec -C <project-root> --full-auto -o .agent_temp/codex-review.md --color never "/prompts:review-gap FIS: {FIS_FILE_PATH} — Review the implementation against the FIS requirements."
3. MANDATORY post-exec verification:
   - Check exit code: echo "codex-exit: $?"
   - Check output file: wc -c .agent_temp/codex-review.md
   - If exit ≠ 0 OR output empty:
     → Do NOT review yourself.
     → Report failure via SendMessage: "CODEX FAILED: role=review, exit=<code>, output_bytes=<N>"
     → Wait for orchestrator.
4. Read the review output
5. Report findings via SendMessage — include:
   - codex_exit_code: <N>
   - codex_output_bytes: <N>
   - report_path: .agent_temp/codex-review.md
   - overall_assessment: pass/fail
   - critical_issues: count
   - high_issues: count
   - summary: brief description of key findings
6. Mark task complete

Important:
- NEVER review code directly — Codex does ALL review work
- Read the Workflow Rules, Guardrails and Guidelines in CLAUDE.md before starting
```

#### 4c. Collect Review Results

- Wait for BOTH reviewers to complete
- Consolidate findings from both reviews:
  - Read the Claude Code review report
  - Read the Codex review report (`.agent_temp/codex-review.md`)
- Deduplicate overlapping findings
- Merge into a unified remediation list, prioritized by severity:
  - Critical → High → Medium → Low
- **Filter findings** — before passing issues to the fixer, the orchestrator MUST triage each finding:
  - **Include** only issues that are clearly aligned with the FIS requirements and project intent
  - **Exclude** findings that would introduce scope creep, over-engineering, or misalignment with the FIS
  - **Exclude** suggestions for added abstraction layers, premature generalization, speculative future-proofing, or refactoring beyond what the FIS calls for
  - When in doubt, ask: *"Would the FIS author have included this?"* — if not, drop it
- If BOTH reviews report no issues (or all findings are filtered out) → skip Step 5, proceed to Step 6

**Gate**: Both reviews complete, findings consolidated and filtered for alignment


### Step 5: Fix via Codex

If any Critical, High, or Medium issues remain after filtering in Step 4c, spawn a fix agent.

**Codex Fixer** — spawned via `Task(team_name: "fis-codex-pipeline", name: "fixer", ...)`:
```
Role: Codex Fixer
Team: fis-codex-pipeline

BRIGHT LINE: You MUST NOT write fix code yourself. ALL coding is done by Codex CLI.
If Codex fails, you escalate — you do NOT implement directly. No exceptions.

Your task: Fix issues identified during dual review.

1. Ensure .agent_temp/ directory exists: mkdir -p .agent_temp
2. Launch Codex to fix:
   codex exec -C <project-root> --full-auto -o .agent_temp/codex-fix.md --color never \
     "Fix the following issues found during review of the implementation.

FIS: {FIS_FILE_PATH}

{CONSOLIDATED_ISSUES_FROM_STEP_4}

Fix Critical, High, and Medium severity issues. Refer to the FIS for requirements context.

IMPORTANT CONSTRAINTS:
- ONLY fix issues that are aligned with the FIS requirements and project intent
- Do NOT introduce new abstractions, patterns, or architectural changes beyond what the FIS specifies
- Do NOT over-engineer fixes — apply the minimum change needed to resolve each issue
- Do NOT add speculative future-proofing, extra configurability, or scope beyond the FIS
- If a fix would require significant new code or architectural changes not in the FIS, skip it and note it as deferred"
3. MANDATORY post-exec verification:
   - Check exit code: echo "codex-exit: $?"
   - Check output file: wc -c .agent_temp/codex-fix.md
   - Check files changed: git diff --stat
   - If exit ≠ 0 OR output empty OR no files changed:
     → Do NOT fix yourself.
     → Report failure via SendMessage: "CODEX FAILED: role=fixer, exit=<code>, output_bytes=<N>"
     → Wait for orchestrator.
4. Read the fix output to confirm resolution
5. Report via SendMessage with: codex_exit_code, codex_output_bytes, files_changed, issues_addressed
6. Mark task complete

Important:
- NEVER write code directly — Codex does ALL fix work
- Read the Workflow Rules, Guardrails and Guidelines in CLAUDE.md before starting
```

After fixer completes:
- Verify Codex evidence (exit code, output file, files changed)
- If Codex failed → escalate to user with details

**Gate**: Fixes applied and verified (or no fixes needed)


### Step 6: Final Verification

**Orchestrator performs directly** (not delegated):

1. Run build — verify it succeeds
2. Run tests — verify all pass
3. Quick integration sanity check across the implementation
4. Include verification evidence in completion summary:
   - **Build**: exit code or success/failure status
   - **Tests**: pass/fail counts
   - **Linting/types**: error and warning counts

**Gate**: Build, tests, and verification pass


### Step 7: Update FIS

Update the FIS document:
- Mark all completed task checkboxes (`- [ ]` → `- [x]`)
- Mark success criteria checkboxes as checked
- Mark Final Validation Checklist items as checked

If this FIS was created for a story from a `plan.md`, also update the plan:
- Set the story's **Status** field to `Done`
- Set the story's **FIS** field to the FIS file path
- Check off completed acceptance criteria


### Step 8: Clean Up

1. Use `SendMessage(type: "shutdown_request")` for each teammate
2. Wait for shutdown confirmations
3. Use `TeamDelete` to remove team
4. Optionally clean up Codex output files: `rm .agent_temp/codex-*.md`


## Completion Summary

Output a summary including:
- **FIS**: path to the specification
- **Implementation**: Codex exit code, files changed
- **Claude Code Review**: assessment, issue counts, report path
- **Codex Review**: assessment, issue counts, report path
- **Fixes Applied**: count of issues addressed (if any)
- **Build/Tests**: verification status
- **Codex output files**: paths to `.agent_temp/codex-*.md` files


## Failure Handling

- **Codex process fails** → agent MUST escalate via `SendMessage` with `CODEX FAILED:` prefix → orchestrator escalates to user with details. Do NOT fall back to direct implementation.
- **Agent bypasses Codex** (reports completion without `codex_exit_code`) → orchestrator marks as failed and escalates to user.
- **Both reviews find no issues** → skip fix step, proceed to final verification.
- **All findings filtered out** (misaligned with FIS, over-engineering) → skip fix step, include filtered findings in completion summary as informational notes.
- **Only Low issues remain after filtering** → inform user of findings but skip automated fix step. User can address manually.
- **Codex authentication failure** → stop immediately, ask user to run `codex login` or set `OPENAI_API_KEY`.


## Fallback: No Agent Teams

If Agent Teams unavailable (Step 1 check fails), suggest running the steps manually:

```bash
# 1. Create FIS
/cc-workflows:spec "feature description"

# 2. Implement via Codex
codex exec -C . --full-auto -o .agent_temp/codex-impl.md "/prompts:exec-spec docs/specs/feature-name.md"

# 3. Review with Claude Code
/cc-workflows:review-gap "FIS: docs/specs/feature-name.md"

# 4. Review with Codex
codex exec -C . --full-auto -o .agent_temp/codex-review.md "/prompts:review-gap FIS: docs/specs/feature-name.md"

# 5. Fix issues (if any)
codex exec -C . --full-auto -o .agent_temp/codex-fix.md "Fix issues: <paste findings>"
```


## Fallback: No Codex CLI

If Codex unavailable (Step 1 check fails), suggest the standard Claude Code alternative:

```bash
# Create FIS, then execute entirely with Claude Code:
/cc-workflows:spec "feature description"
/cc-workflows:exec-spec docs/specs/feature-name.md
```
