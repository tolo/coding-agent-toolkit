# AI Coding Agent Rules, Operating Procedures, Guidelines and Core Project Memory

This file provides guidance to AI coding agents when working with code in this project.


---


_**TODO**: Add Project Overview, Architecture, Tech Stack, Structure etc. here._


--- 


## Workflow Rules, Guardrails and Guidelines

### Foundational Rules and Guardrails
_Always fully read and understand this file before doing any work:_ @docs/rules/CRITICAL-RULES-AND-GUARDRAILS.md

> **Alternative (stronger adherence):** Instead of the `@` reference above, you can inject the rules
> directly into the system prompt via a shell alias. This keeps the rules in a privileged position
> that survives long sessions without drift. See the
> [System Prompt Rules Injection](#system-prompt-rules-injection) section in the
> `claude_code_common` README for setup instructions. If using that approach, **remove** the
> `@` reference above to avoid duplication.


### Foundational Development Guidelines and Standards
Always fully read relevant guidelines below as needed, based on the type of work being done:
- _`<repository_root>/docs/guidelines/DEVELOPMENT-ARCHITECTURE-GUIDELINES.md`_ when doing development work (coding, architecture, etc.)
- _`<repository_root>/docs/guidelines/UX-UI-GUIDELINES.md`_ when doing UX/UI related work
- _`<repository_root>/docs/guidelines/WEB-DEV-GUIDELINES.md`_ when doing web development work


---


## Project specific Guidelines
- [Add references to project-specific guidelines here (don't @ them, just list the paths)]


## Visual Validation Workflow
- [Describe any project-specific visual validation workflow here, or reference documentation files]


---


## Vital Documentation Resources
- [Add references to other important documentation files here (don't @ them, just list the paths)]

**IMPORTANT**: When lookup of documentation (such as API documentation, user guides, language references, etc.) is needed, or when user asks to lookup documentation directly, _always_ execute the documentation lookup in a separate background sub task (use the _`cc-workflows:documentation-lookup`_ agent). This is **CRITICAL** to reduce the load on the main context window and ensure that the main agent can continue working without interruptions.


---


## Useful Tools and MCP Servers

### Command line file search and code exploration tools
- **ripgrep (rg)**: Fast recursive search. Example: `rg "createServerSupabaseClient"`. _Use instead of grep_ for better search performance.
- **ast-grep**: Search by AST node types. Example: `ast-grep 'import { $X } from "supabase"' routes/`
- **tree**: Directory structure visualization. Example: `tree -L 2 routes/`

### Context7 MCP - Library and Framework Documentation Lookup (https://github.com/upstash/context7)
Context7 MCP pulls up-to-date, version-specific documentation and code examples straight from the source.
**Only** use Context7 MCP via the _`cc-workflows:documentation-lookup`_ sub-agent for documentation retrieval tasks.

### Fetch (https://github.com/modelcontextprotocol/servers/tree/main/src/fetch)
Retrieves and processes content from web pages, converting HTML to markdown for easier consumption.
**Only** use Fetch MCP via the _`cc-workflows:documentation-lookup`_ sub-agent for documentation retrieval tasks.

### Code Analysis and Style (Analysis, Linting and Formatting)

**Automatically use the IDE's built-in diagnostics tool to check for analysis, linting and type errors:**
- Run `mcp__ide_getDiagnostics` to check all files for diagnostics
- Fix any linting or type errors before considering the task complete
- Do this for any file you create or modify

### Tools and MCP Servers for visual validation and UI testing/exploration

#### Agent Browser (`https://github.com/vercel-labs/agent-browser`)

Use `agent-browser` for web automation and quick and efficient visual validation.

Run `agent-browser --help` for all commands.
Core workflow:
1. `agent-browser open <url>` - Navigate to page
2. `agent-browser snapshot -i` - Get interactive elements with refs (@e1, @e2)
3. `agent-browser click @e1` / `fill @e2 "text"` - Interact using refs
4. Re-snapshot after page changes

See also this skill: `agent-browser`

#### Chrome DevTools MCP (`https://github.com/ChromeDevTools/chrome-devtools-mcp`)
Use the `chrome-devtools` for deeper visual validation and UI testing/exploration, as well as debugging, analysis/execution of JavaScript etc.

See also this skill: `chrome-devtools`


---


## Key Development Commands

See `<repository_root>/docs/rules/KEY_DEVELOPMENT_COMMANDS.md` for key commands related to development, running, deployment, testing, formatting, linting, and UI testing.


---


## External Agent Application Delegation Protocol _[TODO: OPTIONAL]_

When requested, delegate specific tasks to multiple AI coding agents (external applications), running each review in **parallel background** `Bash` tool processes to speed up the process while keeping the main agent free to continue working.

### codex CLI
Execute the `codex` command via the `Bash` tool.

```bash
# Example:
codex exec --full-auto --config hide_agent_reasoning="true" "<PROMPT_TEXT>"
```
