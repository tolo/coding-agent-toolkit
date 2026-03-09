# Changelog

All notable changes to the **Coding Agent Toolkit** are documented here as a unified timeline.
The `cc-workflows` plugin follows [Semantic Versioning](https://semver.org/) — version numbers are noted alongside plugin changes.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

---

## 2026-03-09 — cc-workflows [0.11.0]

### Added
- **`exec-plan-codex`**: New command — hybrid plan execution that uses Claude Code Agent Teams for orchestration and spec creation, but delegates implementation, review, and troubleshooting to **Codex CLI** instances via `codex exec`. Requires Codex CLI installed with simple-commands as `/prompts:` commands
- **`simple-commands/troubleshoot`**: Ported from `plugins/cc-workflows/commands/utils/troubleshoot.md` — standalone troubleshooting workflow for non-Claude-Code agents (no sub-agent dependencies)

---

## 2026-03-08 — cc-workflows [0.10.1]

### Changed
- **Multiple commands**: Improved FIS portability — clarified instructions to be less Claude-Code-specific
- **`exec-spec`**, **`spec`**, **`design-system`**, **`quick-implement`**, **`refactor`**, **`trade-off-analysis`**, **`troubleshoot`**: Removed explicit `run_in_background` instructions for sub-agents (agent decides autonomously)

---

## 2026-03-05 — cc-workflows [0.10.0]

### Changed
- **Command renames**: `implement` → `exec-spec`, `implement-plan` → `exec-plan` — establishes `exec-` prefix convention (create documents with `plan`/`spec`, execute them with `exec-plan`/`exec-spec`)
- **`plan`**: Added document references header to plan template — links to PRD, ADRs, design system, wireframes at top of generated plan

---

## 2026-03-04 — Repository

### Changed
- **Prompt engineering guidelines**: Major updates to general, Claude-specific, and GPT-specific guidelines — expanded with latest model capabilities and patterns
- **`exec-plan`**, **`exec-spec`**, **`plan`**, **`spec`**: Various corrections and improvements from review feedback

---

## 2026-03-03 — Repository

### Added
- **`dart-lsp`** plugin: New plugin for Dart/Flutter LSP integration

---

## 2026-03-03 — cc-workflows [0.9.2]

### Fixed
- **Stale references**: `FEATURE_REQUEST` → `ARGUMENTS` in `spec`, `create-design-system` → `design-system` in `wireframes`, `create-wireframes` → `wireframes` in `design-system`
- **Missing guards**: `code-simplifier` agent references now conditional "(if available)" in `refactor`, `implement`, `quick-implement`
- **`implement-plan`**: "Roadmap" → "Plan" terminology, race condition (tasks created before agents spawned), FIS output path → `docs/specs/`
- **Typos**: "stuctures", "Extremelty", "descripton", "the simply", double-dash bullets in `trade-off-analysis` and `troubleshoot`
- **`review-gap`**: MCP tool name `mcp__ide__getDiagnostics` → `mcp__ide_getDiagnostics`
- **`clarify`**: Duplicate step numbering in Section 3

### Added
- **`implement-plan`**: `## Usage` section, input validation guard, 8 `**Gate**` checkpoint markers, reviewer fix loop cap (max 2 attempts), `build-troubleshooter` reference in spawn template, scoped Step 7 documentation update
- **`spec`**, **`implement`**: Input validation guards (STOP if required argument missing)
- **`review-council`**: CRITICAL severity section in report template
- **`clarify`**: `spec` as follow-up option (for single features)
- **`review-gap`**: `[Optional]` marker on Phase 5 (Retrospective)
- **README**: External Dependencies section (`code-simplifier`, `frontend-design` plugins)

---

## 2026-02-27 — cc-workflows [0.9.0]

### Changed
- **Command renames for clarity**: `roadmap` → `plan`, `roadmap-execute-team` → `implement-plan`, `spec-create` → `spec`, `spec-execute` → `implement`, `simplify-refactor` → `refactor`
- **`plan`**: Removed "Approach" and "Key Notes" fields from story definitions — technical approach and implementation gotchas are now deferred to `spec` (cleaner separation of concerns between plan and spec)
- **`plan`**: Story scope field narrowed to what's included/excluded only (no implementation approach)

### Added
- **CLAUDE.md**: Added `simple-commands/` section noting agent-agnostic command versions for non-Claude-Code agents

---

## 2026-02-26 — cc-workflows [0.8.0]

### Added
- **`roadmap-execute-team`**: New command — executes entire implementation roadmap through Agent Team pipeline (spec-create → spec-execute → review-gap per story). Dynamic team sizing (3-8 agents), phase-aware dependency management, parallel story execution. Supersedes `spec-execute-team`

### Removed
- **`spec-execute-team`**: Superseded by `roadmap-execute-team` — Agent Teams are better leveraged for full roadmap parallelization than single-FIS validation

---

## 2026-02-22 — cc-workflows [0.7.0]

### Added
- **`troubleshoot`**: `BRIGHT LINE — 3-Fix Stop Condition` — agent must stop and escalate after 3 failed attempts on the same root cause instead of thrashing indefinitely
- **`spec-execute` / `spec-execute-team`**: "Context Injection Best Practice" — orchestrators should extract and inline relevant FIS context per sub-agent rather than having every sub-agent re-read the full FIS
- **`spec-create`**: Self-executing FIS header in template — generated specs include a `> To implement this spec, run: /cc-workflows:spec-execute <path>` callout for discoverability
- **`quick-implement` / `spec-execute` / `spec-execute-team` / `simplify-refactor` / `troubleshoot`**: Verification evidence requirements — completion summaries must include build status, test counts, lint/type errors, visual validation, and runtime confirmation (enforces "Evidence Before Claims" rule)

### Changed
- **`spec-execute`**: `## FIS Reference` block now instructs orchestrators to inline ADR decisions and constraints rather than directing sub-agents to re-read the FIS
- **`troubleshoot`**: §7.2 "Escalation Criteria" scoped to external-dependency and user-decision escalation only; architectural escalation moved to the Bright Line stop condition
- **`spec-create`**: Generation Guideline #5 — instructs the generating agent to substitute the actual output path into the self-executing callout
- **Review command/skill renames**: `review-plan` → `review-doc`, `review-impl` → `review-gap`, `code-review` skill → `review-code`
- **`review-doc`** and **`review-code`**: Converted from command to user-invocable skill (removed thin command wrappers)
- Review report filenames: `*-plan-review-*` → `*-doc-review-*`, `*-impl-review-*` → `*-gap-review-*`

---

## 2026-02-22 — Repository

### Added
- **Hooks** — safety and productivity hook scripts (`hooks/`): `block-dangerous-commands.py`, `protect-files.py`, `git-safety.py`, `url-allowlist.py`, `reinject-context.sh`, `notify.sh` / `notify-elevenlabs.sh`, and configuration files (`blocked-commands.json`, `protected-files.json`, `url-allowlist.json`)
- **CRITICAL-RULES**: Added Bright Line enforcement blocks (`No Bypassing Safety Checks`, `No Orphan Code`, `Verify Before Claiming`), "Evidence Before Claims" rule with rationalization rejection table, and rationalization prevention callout under "Small & Precise Changes" with Boy Scout Rule scope boundary

---

## 2026-02-19 — cc-workflows [0.6.1]

### Added
- **`spec-execute-team`**: New command — executes a FIS with an Agent Team Validation Council (Code Reviewer, QA Test Engineer, Visual Validator, Requirements Verifier, Devil's Advocate, Synthesis Challenger, Issue Resolver) running a validate-fix loop with configurable max iterations

### Changed
- **Command renames**: `clarify-requirements` → `clarify`, `create-design-system` → `design-system`, `review-report` → `review-code`, `spec-generate` → `spec-create`, `research-tradeoffs` → `trade-off-analysis`, `create-wireframes` → `wireframes`
- **README**: Updated with new commands and revised structure

---

## 2026-02-15 — cc-workflows [0.6.0]

### Added
- **`review-council`**: Multi-perspective code review using Agent Teams — spawns specialist reviewers (code quality, security, architecture, UI/UX) plus a Devil's Advocate and Synthesis Challenger for adversarial debate and validated findings

---

## 2026-02-15 — cc-workflows [0.5.1]

### Changed
- **Temp paths**: Standardized all temporary file paths to `<project_root>/.agent_temp/` across all commands
- **Review commands** (`review-impl`, `review-plan`, `code-review` skill): Added instructions to verify technical choices against authoritative/official documentation sources before reporting findings
- **`review-impl`**: Major refactor — significantly reduced verbosity, improved workflow clarity

---

## 2026-02-08 — Repository

### Added
- **CLAUDE.template.md / README**: Instructions for injecting `CRITICAL-RULES-AND-GUARDRAILS.md` via `append-system-prompt` as an alternative to CLAUDE.md inclusion

---

## 2026-02-04 — cc-workflows [0.5.0]

### Added
- **`roadmap`**: New command — creates implementation roadmap with story breakdown from a PRD, with JIT spec creation per story

### Changed
- **`ui-concept`**: Significantly simplified — reduced from ~360 to ~120 lines, focuses on core concept creation
- **`spec-execute`**: Improved sub-agent orchestration, cleaner workflow structure

### Removed
- **`spec-plan`**: Replaced by `roadmap`
- **`swarm-implement`**: Superseded by `spec-execute` + `spec-execute-team`

---

## 2026-02-03 — cc-workflows [0.4.0]

### Added
- **`visual-validation-specialist`** agent: Expanded-scope replacement for `screenshot-validation-specialist` — handles full visual validation workflow including baseline comparison, design compliance checking, and regression detection

### Changed
- **`spec-execute`**: Integrated `visual-validation-specialist` into TV03 validation task

### Removed
- **`screenshot-validation-specialist`** agent: Replaced by `visual-validation-specialist`

---

## 2026-01-30 — cc-workflows [0.3.3]

### Added
- **`simplify-refactor`**: New command — reviews recently modified code for simplification, clarity, and maintainability improvements using the `code-simplifier` agent
- **`quick-implement`**: Added to simple-commands alongside plugin version

### Changed
- **`spec-execute`**: Added `code-simplifier` step in final QA pass

---

## 2026-01-28 — cc-workflows [0.3.0]

### Added
- **`prd`**: New command — generates comprehensive Product Requirements Documents from refined requirements
- **`wireframes`**: Major enhancement — full wireframe generation workflow with validation, inspiration gathering, and HTML output

### Changed
- **`spec-create`**: Major simplification — removed ~250 lines of over-specified content, focused on essential structure
- **`spec-execute`**: Major overhaul — clearer orchestrator pattern, improved sub-agent protocol, validation task structure (TV01-TV04)
- **`clarify`**: Minor improvements to discovery workflow

### Removed
- **`xcode-build-runner`** agent

---

## 2026-01-27 — cc-workflows [0.2.10] _(initial public release)_

### Added
- Commands: `clarify`, `prd`, `spec-create`, `spec-execute`, `spec-plan`, `quick-implement`, `swarm-implement`, `review-plan`, `review-impl`, `review-code`, `trade-off-analysis`, `design-system`, `wireframes`, `utils/troubleshoot`, `utils/ui-concept`
- Specialized agents: `solution-architect`, `qa-test-engineer`, `build-troubleshooter`, `research-specialist`, `documentation-lookup`, `ui-ux-designer`, `screenshot-validation-specialist`, `whimsy-injector`
- `code-review` skill with comprehensive checklists (code quality, architecture, security, UI/UX)

---

## 2026-01-27 — Repository _(initial public release)_

### Added
- `docs/guidelines/` — development/architecture, UX/UI, web development, prompt engineering guidelines (Claude + GPT)
- `docs/rules/CRITICAL-RULES-AND-GUARDRAILS.md` — foundational agent guardrails
- `CLAUDE.md`, `CLAUDE.template.md`
- Simple-commands — standalone versions of core commands for projects not using the plugin system
