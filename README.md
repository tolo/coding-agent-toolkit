# Coding Agent Toolkit

Reusable plugins, commands, agents, and skills for Claude Code.

## Plugins

| Plugin | Description |
|--------|-------------|
| [cc-workflows](plugins/cc-workflows/) | Development workflows: requirements → spec → implementation with review |

## Installation

```bash
# Install a plugin (user scope - all projects)
claude plugin install ./plugins/cc-workflows --scope user

# Install a plugin (project scope - current project only)
claude plugin install ./plugins/cc-workflows --scope project
```

## Repository Structure

```
├── plugins/
│   └── cc-workflows/        # Main workflow plugin
│       ├── commands/        # Slash commands
│       ├── agents/          # Specialized sub-agents
│       └── skills/          # Reusable skills
└── docs/
    ├── rules/               # Critical rules and guardrails
    └── guidelines/          # Development guidelines
```

## System Prompt Rules Injection

By default, projects reference `docs/rules/CRITICAL-RULES-AND-GUARDRAILS.md` from CLAUDE.md using an `@` include. This works well, but the rules are delivered as a user message — in long sessions they can drift as context grows and gets compacted.

For **stronger adherence**, you can inject the rules directly into Claude Code's system prompt via `--append-system-prompt`. System prompt content occupies a privileged, fixed position that never competes with conversation history.

### Setup

1. **Copy the rules file to your Claude config directory:**
   ```bash
   mkdir -p ~/.claude/rules
   cp docs/rules/CRITICAL-RULES-AND-GUARDRAILS.md ~/.claude/rules/
   ```

2. **Add a shell alias** (in `~/.bashrc`, `~/.zshrc`, or equivalent):
   ```bash
   alias claude='claude --append-system-prompt "$(cat ~/.claude/rules/CRITICAL-RULES-AND-GUARDRAILS.md)"'
   ```

3. **Remove the `@` reference** from your project's CLAUDE.md to avoid duplication:
   ```diff
   ### Foundational Rules and Guardrails
   - _Always fully read and understand this file before doing any work:_ @docs/rules/CRITICAL-RULES-AND-GUARDRAILS.md
   + _Rules and guardrails are injected via --append-system-prompt (see claude_code_common README)._
   ```

### Notes

- The alias reads the file fresh on each invocation, so edits to `~/.claude/rules/CRITICAL-RULES-AND-GUARDRAILS.md` take effect immediately.
- If you update the rules in this repo, remember to re-copy them to `~/.claude/rules/`.
- This approach is per-user (shell alias), not per-project. The rules apply to all Claude Code sessions regardless of which project you're in.
- Token cost is neutral — the same content that was in CLAUDE.md is now in the system prompt instead.

## License

MIT
