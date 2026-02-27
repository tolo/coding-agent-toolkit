# Coding Agent Toolkit

Development workflows, rules, guidelines, and safety hooks for Claude Code.

The centerpiece is the **[cc-workflows](#cc-workflows-plugin)** plugin — structured workflows that take you from requirements through implementation to review. Everything else (rules, guidelines, hooks) supports and enhances those workflows.

## Getting Started

### 1. Install the plugin (see [cc-workflows README](plugins/cc-workflows/README.md) for detailed instructions)

```bash
# Add as marketplace
/plugin marketplace add tolo/coding-agent-toolkit

# Install plugin
/plugin install cc-workflows@coding-agent-toolkit
```

This gives you slash commands like `/spec`, `/implement`, `/review-code`, `/quick-implement`, and more. See [cc-workflows commands](#commands) below.

### 2. Set up your project's CLAUDE.md

The plugin's commands reference a **"Workflow Rules, Guardrails and Guidelines"** section in your project's `CLAUDE.md`. Use the included template to set this up:

```bash
# Copy the template (or merge sections into your existing CLAUDE.md)
cp CLAUDE.template.md /path/to/your-project/CLAUDE.md
```

Then copy the rules and guidelines it references:

```bash
# Copy everything
cp -r docs/ /path/to/your-project/docs/

# Or pick only what you need
cp -r docs/rules/ /path/to/your-project/docs/rules/
cp -r docs/guidelines/ /path/to/your-project/docs/guidelines/
```

Fill in the `[TODO]` placeholders in your CLAUDE.md and `KEY_DEVELOPMENT_COMMANDS.md`, remove sections you don't need.

> All `docs/` paths in the template are relative to your project root, so the directory structure should match after copying.

### 3. Optionally add hooks

See [Hooks](#hooks) for safety and workflow automation scripts.

---

## cc-workflows Plugin

Structured development workflows — from requirements to implementation with built-in quality gates.

```
┌──────────────────────────────────────────────────────┐
│  FEATURE WORKFLOW (see cc-workflows README for more) │
│                                                      │
│  (optional)                            (optional)    │
│  clarify ────────────→ spec ─────────→ review-doc    │
│                              │                       │
│                              ▼                       │
│                         implement                    │
│                              │                       │
│                              ▼                       │
│                         review-gap                   │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│  QUICK PATH (small features/fixes)                   │
│                                                      │
│  quick-implement ──→ review-code (optional) ──→ done │
└──────────────────────────────────────────────────────┘
```

For the full plan workflow (MVP / multi-feature), see the [cc-workflows README](plugins/cc-workflows/).

### Commands / Skills

Invoke with `/cc-workflows:<command>` or just `/<command>` if unambiguous.

| Command | Purpose |
|---------|---------|
| `clarify` | Transform vague ideas into clear, actionable requirements |
| `prd` | Create comprehensive PRD from refined requirements |
| `spec` | Create implementation spec from feature requirements |
| `plan` | Create implementation plan with story breakdown from PRD |
| `implement` | Execute spec with validation loops until complete |
| `plan-execute-team` | Execute entire plan through Agent Team pipeline |
| `quick-implement` | Fast path for small features/fixes (supports `--issue` for GitHub) |
| `review-code` | Comprehensive code review (quality, security, architecture, UI/UX) |
| `review-gap` | Gap analysis: implementation vs requirements |
| `review-council` | Multi-perspective review with Agent Teams (5-7 reviewers + debate) |
| `trade-off-analysis` | Evaluate technical alternatives with structured comparison |
| `wireframes` | Generate HTML wireframes for UI planning |
| `design-system` | Create design tokens and component styles |
| `troubleshoot` | Diagnose and fix implementation issues systematically |

### Quick examples

```bash
# Implement a feature from scratch
/spec "user data export as CSV and JSON"
/implement
/review-gap

# Quick fix from GitHub issue
/quick-implement --issue 123

# Architectural decision
/trade-off-analysis "caching strategy for API responses"
```

Full usage examples, agents, skills, and key concepts are documented in the **[cc-workflows README](plugins/cc-workflows/)**.

### Plugin installation options

**Scope options** — installs at `user` scope (all projects) by default:
```bash
/plugin install cc-workflows@coding-agent-toolkit --scope project  # current project only
```

**Local install** — if you have the repo cloned:
```bash
claude plugin install ./plugins/cc-workflows
```

See the [Claude Code plugin docs](https://code.claude.com/docs/en/discover-plugins) for more details.

---

## CLAUDE.md Template

[`CLAUDE.template.md`](CLAUDE.template.md) is the starting point for your project's `CLAUDE.md`. It wires together all the rules and guidelines into a single file that Claude Code reads automatically.

**What's inside:**
- References to rules via `@` includes (so Claude always loads them)
- Conditional references to guidelines (loaded based on the type of work)
- Sections for project-specific info (architecture, tech stack, documentation, MCP servers, etc.)
- `[TODO]` markers for everything you need to fill in

---

## Rules

Files in [`docs/rules/`](docs/rules/) define behavioral rules and guardrails for the AI agent.

### CRITICAL-RULES-AND-GUARDRAILS.md

The core rules file. Covers safety checks, code quality standards, forbidden commands, and operational guardrails — prevents the agent from making destructive mistakes.

**Standard setup (per-project, via CLAUDE.md):**

The template already includes an `@` reference that loads the rules automatically:
```markdown
_Always fully read and understand this file before doing any work:_ @docs/rules/CRITICAL-RULES-AND-GUARDRAILS.md
```
This works well for most projects. Just make sure you've copied the rules file into your project's `docs/rules/` directory.

**Advanced setup (global, via system prompt injection):**

In long sessions, `@`-included content can drift as context gets compacted. For stronger adherence, you can inject the rules directly into the system prompt, where they occupy a fixed, privileged position.

1. Copy the rules file to your Claude config directory:
   ```bash
   mkdir -p ~/.claude/rules
   cp docs/rules/CRITICAL-RULES-AND-GUARDRAILS.md ~/.claude/rules/
   ```

2. Add a shell alias (in `~/.bashrc`, `~/.zshrc`, or equivalent):
   ```bash
   alias claude='claude --append-system-prompt "$(cat ~/.claude/rules/CRITICAL-RULES-AND-GUARDRAILS.md)"'
   ```

3. Remove the `@` reference from your project's CLAUDE.md to avoid duplication:
   ```diff
   - _Always fully read and understand this file before doing any work:_ @docs/rules/CRITICAL-RULES-AND-GUARDRAILS.md
   + _Always fully understand and adhere to the "CRITICAL RULES and GUARDRAILS in this environment" (part of system prompt) before doing any work.
   ```

> **Notes:** The alias reads the file fresh each invocation, so edits take effect immediately. This is per-user (applies to all projects). Token cost is neutral — same content, different delivery mechanism. If you update the rules in this repo, re-copy to `~/.claude/rules/`.

### KEY_DEVELOPMENT_COMMANDS.md

A **template** with `[TODO]` placeholders for your project's key commands (start, test, lint, format). Copy it, fill in your commands, and the agent will know how to run your project.

```bash
cp docs/rules/KEY_DEVELOPMENT_COMMANDS.md /path/to/your-project/docs/rules/
# Then fill in the [TODO] placeholders with your actual commands
```

The CLAUDE.md template already references this file, so the agent will find it automatically.

---

## Guidelines

Files in [`docs/guidelines/`](docs/guidelines/) provide development standards that the agent follows when doing specific types of work. Unlike rules (which are always loaded), guidelines are **loaded on demand** — the CLAUDE.md template tells the agent which guideline to read based on the task at hand.

| File | When it's used |
|------|---------------|
| [`DEVELOPMENT-ARCHITECTURE-GUIDELINES.md`](docs/guidelines/DEVELOPMENT-ARCHITECTURE-GUIDELINES.md) | General development and architecture work |
| [`UX-UI-GUIDELINES.md`](docs/guidelines/UX-UI-GUIDELINES.md) | UI/UX design and implementation |
| [`WEB-DEV-GUIDELINES.md`](docs/guidelines/WEB-DEV-GUIDELINES.md) | Web development (HTML, CSS, JS best practices) |

Additionally, [`docs/prompt-guidelines/`](docs/prompt-guidelines/) contains prompt engineering guidelines (general, Claude-specific, and GPT-specific) referenced by the template.

**How to use:** Copy the guidelines you need into your project's `docs/guidelines/` directory. Remove any you don't need — the agent will simply skip the reference if the file doesn't exist.

**Customization:** These are starting points. Edit them to match your project's conventions (e.g. add your preferred CSS framework rules to the web dev guidelines, or your architecture patterns to the dev guidelines).

---

## Hooks

Standalone [Claude Code hooks](hooks/) for security, notifications, and workflow automation. Pick individually — copy to `~/.claude/hooks/` or reference directly from this repo. See [hooks/README.md](hooks/README.md) for setup.

| Hook | Purpose |
|------|---------|
| `block-dangerous-commands.py` | Blocks destructive shell commands (rm -rf, fork bombs, etc.) |
| `git-safety.py` | Blocks dangerous git operations (force push, reset --hard, etc.) |
| `protect-files.py` | Multi-level file protection (no_access, read_only, no_delete) |
| `url-allowlist.py` | Domain allowlisting for network access and MCP tools |
| `notify.sh` | Desktop notifications on task completion |
| `notify-elevenlabs.sh` | Voice notifications via ElevenLabs TTS |
| `reinject-context.sh` | Re-injects critical rules after context compaction |

## Using with Other Coding Agents

The workflows in this toolkit aren't limited to Claude Code. Two directories contain standalone prompt files usable with **any AI coding agent** (Codex CLI, Aider, Cursor, etc.):

- **[`simple-commands/`](simple-commands/)** — standalone versions of the cc-workflows commands
- **[`plugins/cc-workflows/skills/`](plugins/cc-workflows/skills/)** — reusable skill prompts (e.g. `review-code`, `review-doc`), each in its own directory with a `SKILL.md` file

Use these as custom prompts or copy them into your agent's prompt/instruction directory:

```bash
# Use a command prompt with Codex CLI
codex exec --prompt simple-commands/review-code.md

# Use a skill prompt
codex exec --prompt plugins/cc-workflows/skills/review-code/SKILL.md

# Or copy into your agent's custom prompts directory
cp simple-commands/spec.md ~/.your-agent/prompts/
cp plugins/cc-workflows/skills/review-code/SKILL.md ~/.your-agent/prompts/review-code.md
```

Each file is self-contained — no plugin infrastructure required.

---

## Repository Structure

```
├── CLAUDE.template.md          # CLAUDE.md template for your projects
├── hooks/
│   ├── scripts/                # Standalone hook scripts
│   ├── configs/                # Default hook configs
│   └── README.md               # Setup instructions
├── plugins/
│   └── cc-workflows/           # Main workflow plugin
│       ├── commands/           # Slash commands
│       ├── agents/             # Specialized sub-agents
│       └── skills/             # Reusable skills
├── simple-commands/            # Standalone prompts for any AI coding agent
└── docs/
    ├── rules/                  # Rules and guardrails (copy to project)
    │   ├── CRITICAL-RULES-AND-GUARDRAILS.md
    │   └── KEY_DEVELOPMENT_COMMANDS.md
    ├── guidelines/             # Development guidelines (copy to project)
    │   ├── DEVELOPMENT-ARCHITECTURE-GUIDELINES.md
    │   ├── UX-UI-GUIDELINES.md
    │   └── WEB-DEV-GUIDELINES.md
    ├── prompt-guidelines/      # Prompt engineering guidelines
    └── specs/                  # Feature implementation specs
```

## License

MIT
