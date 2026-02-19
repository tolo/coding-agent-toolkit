#!/usr/bin/env python3
"""PreToolUse(Bash) hook: blocks dangerous git operations."""

import json
import re
import sys

BLOCKED = [
    (r"\bgit\s+push\b.*(--(force|force-with-lease)|\s-f(\s|$))", "Force push blocked. Use normal push."),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard blocked. Use --soft or stash."),
    (r"\bgit\s+branch\s+-D\b", "git branch -D blocked. Use -d for safe delete."),
    (r"\bgit\s+config\s+--global\s+(?!--get)", "git config --global write blocked. Use local config."),
    (r"\bgit\s+rebase\s+--skip\b", "git rebase --skip blocked. Resolve conflicts properly."),
    (r"\bgit\s+clean\s+-[a-zA-Z]*f[a-zA-Z]*(?!.*-n)(?!.*--dry-run)", "git clean -f blocked. Use -n first."),
]


def strip_single_quotes(cmd):
    """Remove contents of single-quoted strings (bash literals are safe)."""
    return re.sub(r"'[^']*'", "", cmd)


def split_commands(cmd):
    """Split on &&, ||, ; to get individual command segments."""
    return re.split(r"\s*(?:&&|\|\||;)\s*", cmd)


def check_command(command):
    """Check command against git safety patterns. Returns (blocked, message) or (False, None)."""
    processed = strip_single_quotes(command)
    segments = split_commands(processed)

    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue
        for regex, message in BLOCKED:
            try:
                if re.search(regex, segment):
                    return True, message
            except re.error:
                continue

    return False, None


def main():
    try:
        data = json.load(sys.stdin)
        command = data.get("tool_input", {}).get("command", "")
    except (json.JSONDecodeError, AttributeError, TypeError):
        print("Hook error: blocking unknown command for safety", file=sys.stderr)
        sys.exit(2)

    if not command:
        sys.exit(0)

    blocked, message = check_command(command)

    if blocked:
        print(f"BLOCKED: {message}", file=sys.stderr)
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
