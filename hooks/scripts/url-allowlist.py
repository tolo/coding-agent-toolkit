#!/usr/bin/env python3
"""URL allowlisting hook for Claude Code PreToolUse events.

Validates network access in Bash commands and MCP tool calls against
a configurable domain allowlist. Fail-closed on errors.
"""
from __future__ import annotations

import fnmatch
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

# --- Hardcoded defaults (used when config file is missing) ---

DEFAULT_CONFIG = {
    "allowed_domains": [
        "github.com", "*.github.com",
        "npmjs.org", "registry.npmjs.org",
        "pypi.org",
        "api.anthropic.com",
    ],
    "allowed_mcp_servers": [],
    "blocked_patterns": [
        r"curl.*\|\s*sh",
        r"wget.*\|\s*sh",
        r"\|\s*curl\s+.*-X\s+POST",
    ],
    "block_direct_ip": True,
}

# Regex for URLs with protocol
URL_REGEX = re.compile(r"https?://([^\s/\"'`,;)}\]]+)", re.IGNORECASE)

# Regex for direct IPv4
IPV4_REGEX = re.compile(r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b")

# Network commands that warrant URL inspection
NETWORK_COMMANDS = re.compile(
    r"\b(?:curl|wget|fetch|nc|ncat|socat|http|telnet"
    r"|ssh|scp|rsync"
    r"|docker\s+pull"
    r"|openssl\s+s_client)"
    r"\b",
    re.IGNORECASE,
)

# Git network subcommands
GIT_NETWORK_REGEX = re.compile(
    r"\bgit\s+(?:clone|fetch|pull|push|remote\s+add)\b", re.IGNORECASE
)

# Package manager URL installs (not registry name installs)
PKG_URL_REGEX = re.compile(
    r"\b(?:pip|pip3)\s+install\s+.*https?://"
    r"|\b(?:npm|yarn|pnpm)\s+install\s+.*https?://",
    re.IGNORECASE,
)

# Base64 encoding patterns (suspicious)
BASE64_PATTERNS = re.compile(
    r"\bbase64\s+-d\b|echo\s+.*\|\s*base64\b", re.IGNORECASE
)


def load_config(project_root: str | None) -> dict:
    """Load and merge global + project configs. Fail-closed on malformed JSON."""
    # User override first, then repo defaults
    user_config = Path.home() / ".claude" / "hooks" / "configs" / "url-allowlist.json"
    repo_config = Path(__file__).resolve().parent.parent / "configs" / "url-allowlist.json"
    global_path = user_config if user_config.is_file() else repo_config
    config = None

    # Load global config
    if global_path.is_file():
        try:
            config = json.loads(global_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            print("Config parse error: ~/.claude/hooks/url-allowlist.json", file=sys.stderr)
            sys.exit(2)

    # Fallback to hardcoded defaults if no global config
    if config is None:
        config = dict(DEFAULT_CONFIG)
        config["allowed_domains"] = list(DEFAULT_CONFIG["allowed_domains"])
        config["allowed_mcp_servers"] = list(DEFAULT_CONFIG["allowed_mcp_servers"])
        config["blocked_patterns"] = list(DEFAULT_CONFIG["blocked_patterns"])

    # Load project-level config (additive only)
    if project_root:
        project_path = Path(project_root) / ".claude" / "hooks" / "url-allowlist.json"
        if project_path.is_file():
            try:
                proj = json.loads(project_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, ValueError):
                print(
                    f"Config parse error: {project_path}", file=sys.stderr
                )
                sys.exit(2)
            # Additive merge (union) - project cannot remove global entries
            if "allowed_domains" in proj:
                config["allowed_domains"] = list(
                    set(config.get("allowed_domains", []))
                    | set(proj["allowed_domains"])
                )
            if "allowed_mcp_servers" in proj:
                config["allowed_mcp_servers"] = list(
                    set(config.get("allowed_mcp_servers", []))
                    | set(proj["allowed_mcp_servers"])
                )
            if "blocked_patterns" in proj:
                config["blocked_patterns"] = list(
                    set(config.get("blocked_patterns", []))
                    | set(proj["blocked_patterns"])
                )
            # block_direct_ip: project cannot weaken (can only make stricter)
            if proj.get("block_direct_ip", False):
                config["block_direct_ip"] = True

    return config


def domain_allowed(domain: str, allowed_domains: list[str]) -> bool:
    """Check if domain matches any pattern in the allowlist (case-insensitive)."""
    domain_lower = domain.lower()
    for pattern in allowed_domains:
        if fnmatch.fnmatch(domain_lower, pattern.lower()):
            return True
    return False


def extract_domains_from_command(command: str) -> list[str]:
    """Extract domains from URLs found in a command string."""
    domains = []
    for match in URL_REGEX.finditer(command):
        host = match.group(1).split(":")[0].split("@")[-1].lower()
        if host:
            domains.append(host)
    return domains


def is_ip_address(host: str) -> bool:
    """Check if host looks like an IPv4 address."""
    return bool(re.fullmatch(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", host))


def has_network_command(command: str) -> bool:
    """Check if command contains any network-related tool."""
    return bool(
        NETWORK_COMMANDS.search(command)
        or GIT_NETWORK_REGEX.search(command)
        or PKG_URL_REGEX.search(command)
    )


def check_blocked_patterns(command: str, patterns: list[str]) -> str | None:
    """Check command against blocked patterns. Returns matching pattern or None."""
    for pattern in patterns:
        try:
            if re.search(pattern, command, re.IGNORECASE):
                return pattern
        except re.error:
            continue
    return None


def check_base64_suspicious(command: str) -> str | None:
    """Detect base64 encoding patterns that may hide URLs."""
    if BASE64_PATTERNS.search(command):
        return "base64 encoding detected (may hide URLs)"
    return None


def validate_bash(command: str, config: dict) -> None:
    """Validate a Bash command for unauthorized network access. Exits on block."""
    # Check blocked patterns first (data exfiltration)
    blocked = check_blocked_patterns(
        command, config.get("blocked_patterns", [])
    )
    if blocked:
        print(
            f"BLOCKED: Command matches dangerous pattern: {blocked}",
            file=sys.stderr,
        )
        sys.exit(2)

    # Only inspect URLs if command contains network tools
    if not has_network_command(command):
        return

    # Check base64 patterns (warning-level, still block)
    b64 = check_base64_suspicious(command)
    if b64:
        print(f"BLOCKED: {b64}", file=sys.stderr)
        sys.exit(2)

    # Extract and validate domains
    domains = extract_domains_from_command(command)
    allowed = config.get("allowed_domains", [])
    block_ip = config.get("block_direct_ip", True)

    for domain in domains:
        # Block direct IP access
        if block_ip and is_ip_address(domain):
            print(
                f"BLOCKED: Direct IP access not allowed: {domain}",
                file=sys.stderr,
            )
            sys.exit(2)

        if not domain_allowed(domain, allowed):
            print(
                f"BLOCKED: Domain not in allowlist: {domain}",
                file=sys.stderr,
            )
            sys.exit(2)

    # Also check for bare IPs not in URLs (e.g. "nc 192.168.1.1 80")
    if block_ip:
        for ip_match in IPV4_REGEX.finditer(command):
            ip = ip_match.group(1)
            # Skip if it's part of a URL we already checked
            if ip not in [d for d in domains if is_ip_address(d)]:
                # Verify it looks like it's used as a host (not a version number etc.)
                # Simple heuristic: if any octet > 255, skip
                octets = ip.split(".")
                if all(0 <= int(o) <= 255 for o in octets):
                    print(
                        f"BLOCKED: Direct IP access not allowed: {ip}",
                        file=sys.stderr,
                    )
                    sys.exit(2)


def validate_mcp(tool_name: str, tool_input: dict, config: dict) -> None:
    """Validate an MCP tool call. Exits on block."""
    # Extract server name: mcp__{server}__{method}
    parts = tool_name.split("__")
    if len(parts) < 2:
        print(
            f"BLOCKED: Malformed MCP tool name: {tool_name}",
            file=sys.stderr,
        )
        sys.exit(2)

    server = parts[1]
    allowed_servers = config.get("allowed_mcp_servers", [])

    if server not in allowed_servers:
        print(
            f"BLOCKED: MCP server not in allowlist: {server}",
            file=sys.stderr,
        )
        sys.exit(2)

    # Special handling for mcp__fetch__fetch: validate URL parameter
    if tool_name == "mcp__fetch__fetch":
        url = tool_input.get("url", "")
        if url:
            try:
                parsed = urlparse(url)
                domain = parsed.hostname
                if domain:
                    domain = domain.lower()
                    allowed_domains = config.get("allowed_domains", [])

                    if config.get("block_direct_ip", True) and is_ip_address(domain):
                        print(
                            f"BLOCKED: Direct IP access not allowed in fetch: {domain}",
                            file=sys.stderr,
                        )
                        sys.exit(2)

                    if not domain_allowed(domain, allowed_domains):
                        print(
                            f"BLOCKED: Fetch URL domain not in allowlist: {domain}",
                            file=sys.stderr,
                        )
                        sys.exit(2)
            except Exception:
                print(
                    f"BLOCKED: Could not parse fetch URL: {url}",
                    file=sys.stderr,
                )
                sys.exit(2)


def main() -> None:
    # Read stdin JSON
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        print("BLOCKED: Failed to parse hook input JSON", file=sys.stderr)
        sys.exit(2)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Determine project root
    project_root = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd")

    # Load config
    config = load_config(project_root)

    # Route by tool type
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if command:
            validate_bash(command, config)
    elif tool_name.startswith("mcp__"):
        validate_mcp(tool_name, tool_input, config)

    # If we get here, allow the action
    sys.exit(0)


if __name__ == "__main__":
    main()
