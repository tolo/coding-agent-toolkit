# Coding Agent Toolkit

Reusable plugins, commands, agents, and skills for Claude Code.

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

## Plugins

| Plugin | Description |
|--------|-------------|
| [cc-workflows](plugins/cc-workflows/) | Development workflows: requirements → spec → implementation with review |

## Installation

Add this repo as a [plugin marketplace](https://code.claude.com/docs/en/discover-plugins), then install plugins from it:

```bash
# Add as marketplace
/plugin marketplace add tolo/coding-agent-toolkit

# Install plugin
/plugin install cc-workflows@coding-agent-toolkit
```

**Scope options** — plugins install at `user` scope (all projects) by default:
```bash
/plugin install cc-workflows@coding-agent-toolkit --scope project  # current project only
```

**Local install** — if you have the repo cloned:
```bash
claude plugin install ./plugins/cc-workflows
```

See the [Claude Code plugin docs](https://code.claude.com/docs/en/discover-plugins) for more details.

## Repository Structure

```
├── hooks/
│   ├── scripts/             # Standalone hook scripts
│   ├── configs/             # Default hook configs
│   └── README.md            # Setup instructions
├── plugins/
│   └── cc-workflows/        # Main workflow plugin
│       ├── commands/        # Slash commands
│       ├── agents/          # Specialized sub-agents
│       └── skills/          # Reusable skills
└── docs/
    ├── rules/               # Critical rules and guardrails
    ├── guidelines/          # Development guidelines
    └── specs/               # Feature implementation specs
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
