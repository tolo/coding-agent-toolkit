# Claude Code Common

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

## License

MIT
