# AI Coding Agent Rules, Operating Procedures, Guidelines and Core Project Memory

This file provides guidance to AI coding agents when working with code in this project.


---


_**TODO**: Add Project Overview, Architecture, Tech Stack, Structure etc. here._


--- 


## Workflow Rules, Guardrails and Guidelines

### Foundational Rules and Guardrails
_Always fully understand and adhere to the "CRITICAL RULES and GUARDRAILS in this environment" (part of system prompt) before doing any work_.


### Foundational Development Guidelines and Standards
Always fully read relevant guidelines below as needed, based on the type of work being done:
- _`<repository_root>/docs/guidelines/DEVELOPMENT-ARCHITECTURE-GUIDELINES.md`_ when doing development work (coding, architecture, etc.)
- _`<repository_root>/docs/guidelines/UX-UI-GUIDELINES.md`_ when doing UX/UI related work
- _`<repository_root>/docs/guidelines/WEB-DEV-GUIDELINES.md`_ when doing web development work
- _`<repository_root>/docs/prompt-guidelines/PROMPT-ENGINEERING-GUIDELINES.md`_ when doing prompt engineering work
    - For Anthropic/Claude models, see also _`<repository_root>/docs/prompt-guidelines/PROMPT-ENGINEERING-GUIDELINES-CLAUDE.md`_
    - For OpenAI GPT models, see also _`<repository_root>/docs/prompt-guidelines/PROMPT-ENGINEERING-GUIDELINES-GPT.md`_


---

## Vital Documentation Resources
- [Add references to other important documentation files here]

**IMPORTANT**: When lookup of documentation (such as API documentation, user guides, language references, etc.) is needed, or when user asks to lookup documentation directly, _always_ execute the documentation lookup in a separate background sub task (use the _`documentation-lookup`_ agent). This is **CRITICAL** to reduce the load on the main context window and ensure that the main agent can continue working without interruptions.


---


## Useful Tools and MCP Servers

### Command line file search and code exploration tools
- **ripgrep (rg)**: Fast recursive search. Example: `rg "createServerSupabaseClient"`. _Use instead of grep_ for better search performance.
- **ast-grep**: Search by AST node types. Example: `ast-grep 'import { $X } from "supabase"' routes/`
- **tree**: Directory structure visualization. Example: `tree -L 2 routes/`

### Context7 MCP - Library and Framework Documentation Lookup (https://github.com/upstash/context7)
Context7 MCP pulls up-to-date, version-specific documentation and code examples straight from the source.
**Only** use Context7 MCP via the _`documentation-lookup`_ sub-agent for documentation retrieval tasks.

### Fetch (https://github.com/modelcontextprotocol/servers/tree/main/src/fetch)
Retrieves and processes content from web pages, converting HTML to markdown for easier consumption.
**Only** use Fetch MCP via the _`documentation-lookup`_ sub-agent for documentation retrieval tasks.

### Code Analysis and Style (Analysis, Linting and Formatting)

**Automatically use the IDE's built-in diagnostics tool to check for analysis, linting and type errors:**
- If available, use run IDE MCP (`mcp__ide_getDiagnostics`) to check all files for diagnostics
- Fix any linting or type errors before considering the task complete
- Do this for any file you create or modify


---
