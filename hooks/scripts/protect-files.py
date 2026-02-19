#!/usr/bin/env python3
"""Claude Code PreToolUse hook: multi-level file protection."""

import fnmatch
import json
import os
import re
import sys
from pathlib import Path

# Hardcoded self-protection patterns (write-block only, read allowed)
SELF_PROTECTION_PATTERNS = [
    os.path.expanduser("~/.claude/hooks/*"),
    os.path.expanduser("~/.claude/settings.json"),
    os.path.expanduser("~/.claude/settings.local.json"),
]

HARDCODED_DEFAULTS = {
    "no_access": [
        ".env", ".env.*", ".ssh/*", ".aws/credentials", ".aws/config",
        "credentials.json", "credentials.yaml", "*.pem", "*.key",
        ".kube/config", "secrets.yml", "secrets.yaml",
    ],
    "read_only": [
        "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
        "Cargo.lock", "poetry.lock", "go.sum",
    ],
    "no_delete": [
        ".git/*", "LICENSE", "README.md",
    ],
}

IS_MACOS = sys.platform == "darwin"

# Bash command categories
READ_CMDS = re.compile(r"\b(?:cat|head|tail|less|more|grep|egrep|fgrep|rg)\b")
WRITE_CMDS = re.compile(r"\b(?:tee)\b")
SED_CMD = re.compile(r"\bsed\b")
SED_INPLACE = re.compile(r"\bsed\b\s+(?:.*\s)?-i")
AWK_CMD = re.compile(r"\bawk\b")
DELETE_CMDS = re.compile(r"\b(?:rm|unlink|shred)\b")
MOVE_CMD = re.compile(r"\bmv\b")
CP_CMD = re.compile(r"\bcp\b")
REDIRECT_WRITE = re.compile(r">>?\s*(\S+)")


def _match_pattern(path_str, pattern):
    """Match a path against a fnmatch pattern, case-insensitive on macOS."""
    if IS_MACOS:
        return fnmatch.fnmatch(path_str.lower(), pattern.lower())
    return fnmatch.fnmatch(path_str, pattern)


def _normalize_path(file_path, cwd):
    """Normalize a path and return (original_abs, resolved) pair."""
    expanded = os.path.expanduser(file_path)
    if not os.path.isabs(expanded):
        expanded = os.path.join(cwd, expanded)
    original_abs = os.path.normpath(expanded)
    resolved = os.path.realpath(original_abs)
    return original_abs, resolved


def _path_forms(original_abs, resolved, cwd):
    """Return all path forms to check against patterns."""
    forms = {original_abs, resolved}
    home = os.path.expanduser("~")
    # Relative-to-cwd forms
    for p in [original_abs, resolved]:
        try:
            rel = os.path.relpath(p, cwd)
            forms.add(rel)
        except ValueError:
            pass
        # Relative-to-home forms (for patterns like .ssh/*, .aws/*)
        try:
            rel_home = os.path.relpath(p, home)
            forms.add(rel_home)
        except ValueError:
            pass
    # Basename for simple patterns like ".env", "LICENSE"
    forms.add(os.path.basename(original_abs))
    forms.add(os.path.basename(resolved))
    return forms


def _check_self_protection(original_abs, resolved, is_write_op):
    """Check hardcoded self-protection. Returns error message or None."""
    if not is_write_op:
        return None
    for pattern in SELF_PROTECTION_PATTERNS:
        for path_str in [original_abs, resolved]:
            if _match_pattern(path_str, pattern):
                return f"BLOCKED: {path_str} is protected (self-protection). Hook scripts and Claude settings cannot be modified."
    return None


def _is_parent_of_pattern(path_str, pattern):
    """Check if path_str is a parent directory of a pattern (e.g., .git is parent of .git/*)."""
    # Normalize: .git/* -> check if path_str is .git or a parent
    pattern_dir = pattern.rstrip("/*")
    if pattern_dir and (path_str == pattern_dir or pattern_dir.startswith(path_str + "/")):
        return True
    return False


def _check_protection(path_forms, patterns_by_level, tool_name, bash_op=None):
    """Check file against protection levels. Returns error message or None.

    bash_op: 'read', 'write', or 'delete' for Bash commands.
    """
    for form in path_forms:
        # no_access: block everything
        for pattern in patterns_by_level.get("no_access", []):
            if _match_pattern(form, pattern):
                return f"BLOCKED: {form} is protected (no_access). All access denied."
            # Deleting a parent directory of a no_access pattern
            if bash_op == "delete" and _is_parent_of_pattern(form, pattern):
                return f"BLOCKED: {form} contains protected files (no_access). Deletion not allowed."

        # read_only: block writes/deletes
        for pattern in patterns_by_level.get("read_only", []):
            if _match_pattern(form, pattern):
                if tool_name in ("Edit", "Write"):
                    return f"BLOCKED: {form} is protected (read_only). Editing/writing not allowed."
                if tool_name == "Bash" and bash_op in ("write", "delete"):
                    return f"BLOCKED: {form} is protected (read_only). Modification not allowed."
                return None  # read allowed

        # no_delete: block deletion only
        for pattern in patterns_by_level.get("no_delete", []):
            if _match_pattern(form, pattern):
                if tool_name == "Bash" and bash_op == "delete":
                    return f"BLOCKED: {form} is protected (no_delete). Deletion not allowed."
                return None  # read/edit allowed
            # Deleting a parent directory of a no_delete pattern
            if bash_op == "delete" and _is_parent_of_pattern(form, pattern):
                return f"BLOCKED: {form} contains protected files (no_delete). Deletion not allowed."

    return None


def _load_config(cwd):
    """Load and merge config files. Project extends global (additive)."""
    patterns_by_level = {k: set(v) for k, v in HARDCODED_DEFAULTS.items()}

    # Load global config: user override first, then repo defaults
    user_config = Path.home() / ".claude" / "hooks" / "configs" / "protected-files.json"
    repo_config = Path(__file__).resolve().parent.parent / "configs" / "protected-files.json"
    global_config_path = str(user_config) if user_config.is_file() else str(repo_config)
    global_loaded = _merge_config_file(patterns_by_level, global_config_path)

    # Load project config (additive)
    if cwd:
        project_config_path = os.path.join(cwd, ".claude", "hooks", "protected-files.json")
        _merge_config_file(patterns_by_level, project_config_path)

    if not global_loaded:
        # No global config found, use hardcoded defaults only (already set)
        pass

    return {k: list(v) for k, v in patterns_by_level.items()}


def _merge_config_file(patterns_by_level, config_path):
    """Merge a config file into patterns_by_level. Returns True if loaded."""
    try:
        if not os.path.isfile(config_path):
            return False
        with open(config_path, "r") as f:
            config = json.load(f)
        levels = config.get("protection_levels", {})
        for level_name, level_data in levels.items():
            pats = level_data.get("patterns", [])
            if level_name not in patterns_by_level:
                patterns_by_level[level_name] = set()
            patterns_by_level[level_name].update(pats)
        return True
    except (json.JSONDecodeError, TypeError, KeyError) as e:
        print(f"WARNING: Malformed config {config_path}: {e}", file=sys.stderr)
        return False


def _extract_file_args(args_str):
    """Extract file path arguments from a command argument string.

    Strips flags, handles --, returns remaining args as potential file paths.
    """
    parts = args_str.split()
    files = []
    past_flags = False
    for part in parts:
        if part == "--":
            past_flags = True
            continue
        if not past_flags and part.startswith("-"):
            continue
        files.append(part)
    return files


def _parse_bash_operations(command, cwd):
    """Parse a bash command and return list of (file_path, operation) tuples.

    operation is 'read', 'write', or 'delete'.
    """
    operations = []

    # Split on pipes and semicolons for multi-command parsing
    # Simple split - handles most common cases
    segments = re.split(r"[|;]|&&|\|\|", command)

    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue

        # Check for redirections (write) in the segment
        for m in REDIRECT_WRITE.finditer(segment):
            target = m.group(1)
            if target and not target.startswith("-"):
                operations.append((target, "write"))

        # Delete commands
        if DELETE_CMDS.search(segment):
            # Extract everything after the command
            m = re.search(r"\b(?:rm|unlink|shred)\b\s+(.*)", segment)
            if m:
                for f in _extract_file_args(m.group(1)):
                    operations.append((f, "delete"))

        # sed -i (write)
        elif SED_INPLACE.search(segment):
            m = re.search(r"\bsed\b\s+(.*)", segment)
            if m:
                for f in _extract_file_args(m.group(1)):
                    operations.append((f, "write"))

        # sed without -i (read)
        elif SED_CMD.search(segment):
            m = re.search(r"\bsed\b\s+(.*)", segment)
            if m:
                for f in _extract_file_args(m.group(1)):
                    operations.append((f, "read"))

        # tee (write)
        elif WRITE_CMDS.search(segment):
            m = re.search(r"\btee\b\s+(.*)", segment)
            if m:
                for f in _extract_file_args(m.group(1)):
                    operations.append((f, "write"))

        # mv (write - could overwrite target, and source access)
        elif MOVE_CMD.search(segment):
            m = re.search(r"\bmv\b\s+(.*)", segment)
            if m:
                files = _extract_file_args(m.group(1))
                for f in files:
                    operations.append((f, "write"))

        # cp (read source, write target - check both)
        elif CP_CMD.search(segment):
            m = re.search(r"\bcp\b\s+(.*)", segment)
            if m:
                files = _extract_file_args(m.group(1))
                if files:
                    # All args could be sources except last (target)
                    for f in files[:-1]:
                        operations.append((f, "read"))
                    if len(files) > 1:
                        operations.append((files[-1], "write"))

        # Read commands
        elif READ_CMDS.search(segment):
            m = re.search(r"\b(?:cat|head|tail|less|more|grep|egrep|fgrep|rg)\b\s+(.*)", segment)
            if m:
                for f in _extract_file_args(m.group(1)):
                    operations.append((f, "read"))

        # awk (read)
        elif AWK_CMD.search(segment):
            m = re.search(r"\bawk\b\s+(.*)", segment)
            if m:
                for f in _extract_file_args(m.group(1)):
                    operations.append((f, "read"))

    return operations


def main():
    input_data = json.loads(sys.stdin.read())
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    cwd = input_data.get("cwd", os.getcwd())

    # Quick exit for unrelated tools
    if tool_name not in ("Read", "Edit", "Write", "Bash"):
        sys.exit(0)

    patterns_by_level = _load_config(cwd)

    if tool_name in ("Read", "Edit", "Write"):
        file_path = tool_input.get("file_path", "")
        if not file_path:
            sys.exit(0)

        original_abs, resolved = _normalize_path(file_path, cwd)
        is_write = tool_name in ("Edit", "Write")

        # Self-protection check
        msg = _check_self_protection(original_abs, resolved, is_write)
        if msg:
            print(msg, file=sys.stderr)
            sys.exit(2)

        # Protection level check
        forms = _path_forms(original_abs, resolved, cwd)
        msg = _check_protection(forms, patterns_by_level, tool_name)
        if msg:
            print(msg, file=sys.stderr)
            sys.exit(2)

    elif tool_name == "Bash":
        command = tool_input.get("command", "")
        if not command:
            sys.exit(0)

        operations = _parse_bash_operations(command, cwd)

        for file_path, op in operations:
            if not file_path or file_path.startswith("-"):
                continue

            original_abs, resolved = _normalize_path(file_path, cwd)
            is_write = op in ("write", "delete")

            # Self-protection check
            msg = _check_self_protection(original_abs, resolved, is_write)
            if msg:
                print(msg, file=sys.stderr)
                sys.exit(2)

            # Protection level check
            forms = _path_forms(original_abs, resolved, cwd)
            msg = _check_protection(forms, patterns_by_level, "Bash", bash_op=op)
            if msg:
                print(msg, file=sys.stderr)
                sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        print(f"BLOCKED: Unhandled error in protect-files hook: {e}", file=sys.stderr)
        sys.exit(2)
