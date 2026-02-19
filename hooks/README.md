# Claude Code Hooks Collection

Standalone Claude Code hooks. Pick the ones you need and add them to your settings individually.

## Available Hooks

| Script | Hook Event | Matcher | Purpose |
|--------|-----------|---------|---------|
| `block-dangerous-commands.py` | PreToolUse | `Bash` | Blocks destructive shell commands (rm -rf, fork bombs, pipe-to-shell, etc.) |
| `git-safety.py` | PreToolUse | `Bash` | Blocks dangerous git operations (force push, reset --hard, branch -D, etc.) |
| `protect-files.py` | PreToolUse | `Edit\|Write\|Read\|Bash` | Multi-level file protection (no_access, read_only, no_delete) |
| `url-allowlist.py` | PreToolUse | `Bash`, `mcp__.*` | Domain allowlisting for network access and MCP tools |
| `notify.sh` | Stop, Notification | -- | Desktop notifications when Claude finishes or needs attention |
| `notify-elevenlabs.sh` | Stop, Notification | -- | Voice notifications via ElevenLabs TTS API |
| `reinject-context.sh` | SessionStart | `compact` | Re-injects critical rules after context compaction |

## Prerequisites

- **Python 3.8+**
- **jq** (recommended; scripts have fallback to Python-based JSON parsing)
- **curl** (for ElevenLabs voice notifications)

## Installation

Two approaches — pick one per hook:

### Option A: Copy to `~/.claude/hooks/` (self-contained)

Copy scripts and configs to your user directory. Independent of the repo.

```bash
# Create directories
mkdir -p ~/.claude/hooks/scripts ~/.claude/hooks/configs

# Copy scripts you want (pick any combination)
cp hooks/scripts/block-dangerous-commands.py ~/.claude/hooks/scripts/
cp hooks/scripts/git-safety.py               ~/.claude/hooks/scripts/
cp hooks/scripts/protect-files.py            ~/.claude/hooks/scripts/
cp hooks/scripts/url-allowlist.py            ~/.claude/hooks/scripts/
cp hooks/scripts/notify.sh                   ~/.claude/hooks/scripts/
cp hooks/scripts/notify-elevenlabs.sh        ~/.claude/hooks/scripts/
cp hooks/scripts/reinject-context.sh         ~/.claude/hooks/scripts/

# Copy configs for the Python hooks you chose
cp hooks/configs/blocked-commands.json       ~/.claude/hooks/configs/
cp hooks/configs/protected-files.json        ~/.claude/hooks/configs/
cp hooks/configs/url-allowlist.json          ~/.claude/hooks/configs/

# Make scripts executable
chmod +x ~/.claude/hooks/scripts/*.py ~/.claude/hooks/scripts/*.sh
```

Then reference as `~/.claude/hooks/scripts/<script>` in settings.

### Option B: Reference from repo (auto-updates with pulls)

Point settings directly at the cloned repo. Replace `/path/to/repo` with the actual path.

Then reference as `/path/to/repo/hooks/scripts/<script>` in settings.

Config customization still works — scripts check `~/.claude/hooks/configs/` first (user override), then script-relative `../configs/` (repo defaults), then hardcoded defaults.

---

## Hook Details & Settings Configuration

Add entries to `~/.claude/settings.json` (or project-level `.claude/settings.json`) for each hook you want. Examples below use `~/.claude/hooks/scripts/` paths (Option A). For Option B, substitute with your repo path.

---

### block-dangerous-commands.py

Intercepts Bash commands and blocks destructive patterns: `rm -rf`, fork bombs, `chmod 777`, `dd` to devices, `mkfs`, pipe-to-shell (`curl | sh`), and interpreter escapes (`bash -c`, `eval`, `python3 -c`). Allows safe pipe targets like `jq`, `grep`, `sort`.

**Config**: `blocked-commands.json` — customize blocked patterns and safe pipe targets. Copy to `~/.claude/hooks/configs/` to override defaults.

**Add to `hooks.PreToolUse` array in settings:**

```json
{
  "matcher": "Bash",
  "hooks": [{
    "type": "command",
    "command": "python3 ~/.claude/hooks/scripts/block-dangerous-commands.py",
    "statusMessage": "Validating command safety..."
  }]
}
```

---

### git-safety.py

Blocks dangerous git operations that can cause data loss: `git push --force`, `git reset --hard`, `git branch -D`, `git config --global` writes, `git rebase --skip`, and `git clean -f` (without `--dry-run`). No config file — patterns are hardcoded to prevent weakening.

**Add to `hooks.PreToolUse` array in settings:**

```json
{
  "matcher": "Bash",
  "hooks": [{
    "type": "command",
    "command": "python3 ~/.claude/hooks/scripts/git-safety.py",
    "statusMessage": "Checking git safety..."
  }]
}
```

---

### protect-files.py

Enforces multi-level file protection across Read, Edit, Write, and Bash tools. Three protection levels:
- **no_access**: blocks all access (e.g., `.env`, `.ssh/*`, `*.pem`, `*.key`)
- **read_only**: allows reading, blocks editing (e.g., `package-lock.json`, `yarn.lock`)
- **no_delete**: allows read/edit, blocks deletion (e.g., `.git/*`, `LICENSE`)

Also includes hardcoded self-protection preventing modification of hook scripts and `~/.claude/settings.json`. Detects indirect access via Bash commands (`cat`, `grep`, `rm`, `sed -i`, etc.).

**Config**: `protected-files.json` — add/modify protected patterns per level. Copy to `~/.claude/hooks/configs/` to override. Project-level config (`.claude/hooks/protected-files.json`) extends global config additively.

**Add to `hooks.PreToolUse` array in settings:**

```json
{
  "matcher": "Edit|Write|Read|Bash",
  "hooks": [{
    "type": "command",
    "command": "python3 ~/.claude/hooks/scripts/protect-files.py",
    "statusMessage": "Checking file protection..."
  }]
}
```

---

### url-allowlist.py

Prevents unauthorized network access by validating URLs in Bash commands and MCP tool calls against a domain allowlist. Blocks direct IP access, data exfiltration patterns (`curl -d`, pipe-to-POST), and base64-encoded URL obfuscation. For MCP tools, validates both the server name and (for `mcp__fetch__fetch`) the target URL.

**Config**: `url-allowlist.json` — customize allowed domains (glob patterns supported, e.g., `*.github.com`), allowed MCP servers, blocked patterns, and IP blocking. Copy to `~/.claude/hooks/configs/` to override. Project-level config (`.claude/hooks/url-allowlist.json`) extends global config additively.

**Add both entries to `hooks.PreToolUse` array in settings** (one for Bash commands, one for MCP tools):

```json
{
  "matcher": "Bash",
  "hooks": [{
    "type": "command",
    "command": "python3 ~/.claude/hooks/scripts/url-allowlist.py",
    "statusMessage": "Checking network access..."
  }]
},
{
  "matcher": "mcp__.*",
  "hooks": [{
    "type": "command",
    "command": "python3 ~/.claude/hooks/scripts/url-allowlist.py",
    "statusMessage": "Checking network access..."
  }]
}
```

---

### notify.sh

Sends desktop notifications when Claude finishes a task (Stop event) or needs attention (permission prompt, idle). Uses macOS `osascript`, Linux `notify-send`, or terminal bell as fallback. Includes smart debouncing (5s) and suppresses Stop notifications for short sessions (<30s).

No config file. No dependencies beyond Bash (jq optional, has grep/sed fallback).

**Add both entries to settings** — one under `hooks.Stop`, one under `hooks.Notification`:

```json
"Stop": [{
  "hooks": [{
    "type": "command",
    "command": "bash ~/.claude/hooks/scripts/notify.sh",
    "timeout": 10
  }]
}],
"Notification": [{
  "matcher": "permission_prompt|idle_prompt",
  "hooks": [{
    "type": "command",
    "command": "bash ~/.claude/hooks/scripts/notify.sh",
    "timeout": 10
  }]
}]
```

---

### notify-elevenlabs.sh

Voice notification variant using the ElevenLabs TTS API. Same events and debounce logic as `notify.sh`, but speaks the notification aloud instead of showing a desktop popup. Falls back silently if API key is not set or the API is unreachable.

No config file. Requires `ELEVENLABS_API_KEY` env var and `curl`. See [ElevenLabs Setup](#elevenlabs-setup).

**Add both entries to settings** — same structure as `notify.sh`:

```json
"Stop": [{
  "hooks": [{
    "type": "command",
    "command": "bash ~/.claude/hooks/scripts/notify-elevenlabs.sh",
    "timeout": 10
  }]
}],
"Notification": [{
  "matcher": "permission_prompt|idle_prompt",
  "hooks": [{
    "type": "command",
    "command": "bash ~/.claude/hooks/scripts/notify-elevenlabs.sh",
    "timeout": 10
  }]
}]
```

---

### reinject-context.sh

Re-injects critical rules from `docs/rules/CRITICAL-RULES-AND-GUARDRAILS.md` into Claude's context after automatic compaction. Without this, rules from CLAUDE.md can be lost when the conversation gets long and context is compressed. Triggers only on the `compact` matcher (i.e., when Claude Code compacts context).

No config file. Requires the rules file to exist at `$CLAUDE_PROJECT_DIR/docs/rules/CRITICAL-RULES-AND-GUARDRAILS.md`.

**Add to `hooks.SessionStart` in settings:**

```json
"SessionStart": [{
  "matcher": "compact",
  "hooks": [{
    "type": "command",
    "command": "bash ~/.claude/hooks/scripts/reinject-context.sh"
  }]
}]
```

## Full Example

Complete `~/.claude/settings.json` with all hooks enabled:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "python3 ~/.claude/hooks/scripts/block-dangerous-commands.py",
          "statusMessage": "Validating command safety..."
        }]
      },
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "python3 ~/.claude/hooks/scripts/git-safety.py",
          "statusMessage": "Checking git safety..."
        }]
      },
      {
        "matcher": "Edit|Write|Read|Bash",
        "hooks": [{
          "type": "command",
          "command": "python3 ~/.claude/hooks/scripts/protect-files.py",
          "statusMessage": "Checking file protection..."
        }]
      },
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "python3 ~/.claude/hooks/scripts/url-allowlist.py",
          "statusMessage": "Checking network access..."
        }]
      },
      {
        "matcher": "mcp__.*",
        "hooks": [{
          "type": "command",
          "command": "python3 ~/.claude/hooks/scripts/url-allowlist.py",
          "statusMessage": "Checking network access..."
        }]
      }
    ],
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "bash ~/.claude/hooks/scripts/notify.sh",
        "timeout": 10
      }]
    }],
    "Notification": [{
      "matcher": "permission_prompt|idle_prompt",
      "hooks": [{
        "type": "command",
        "command": "bash ~/.claude/hooks/scripts/notify.sh",
        "timeout": 10
      }]
    }],
    "SessionStart": [{
      "matcher": "compact",
      "hooks": [{
        "type": "command",
        "command": "bash ~/.claude/hooks/scripts/reinject-context.sh"
      }]
    }]
  }
}
```

## Config Customization

Default configs live in `hooks/configs/` (or `~/.claude/hooks/configs/` if you used Option A).

To customize, edit the configs at `~/.claude/hooks/configs/`. Scripts check:
1. `~/.claude/hooks/configs/<name>.json` (user override)
2. Script-relative `../configs/<name>.json` (repo defaults)
3. Hardcoded fail-closed defaults

## ElevenLabs Setup

1. Set the `ELEVENLABS_API_KEY` environment variable:
   ```bash
   export ELEVENLABS_API_KEY="your-api-key-here"
   ```

2. Optionally set `ELEVENLABS_VOICE_ID` (defaults to "Rachel"):
   ```bash
   export ELEVENLABS_VOICE_ID="your-preferred-voice-id"
   ```

3. Add both to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.) for persistence.
