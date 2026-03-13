---
description: Prime the context for development work
argument-hint: [Optional feature specification]
---

# Prime the context of the coding agent for development work
Prime the context by loading relevant information about the project, guidelines, rules, and any specific feature specifications or requirements.


## Variables

FEATURE_SPEC: $ARGUMENTS (_optional_)


## Workflow

### Phase 1: Load Rules and Guidelines
- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section as defined in AGENTS.md, etc. before starting work, including but not limited to _all_ of the following sub sections in detail:
  - **Foundational Rules and Guardrails**
  - **Foudational Development Guidelines and Standards** (e.g. Development, Architecture, UI/UX Guidelines etc.)
- **Fully read** and understand additional relevant guidelines and documentation as needed, depending on project context, or specific feature requirements (_`FEATURE_SPEC`_)


### Phase 2: Codebase Analysis

1. If specified, analyse the requirements of the requested feature/fix (see _`FEATURE_SPEC`_)
2. Analyse the codebase to properly understand the project structure, relevant files and similar patterns
   - Use commands like `tree -d` and `git ls-files | head -250` to get overview of codebase structure   
   - If the project is empty (besides basic AI coding agent files such as CLAUDE.md, AGENTS.md, etc.), just skip this step
   - For complex codebase exploration, consider using Explore agent (if available)
   - Identify potential roadblocks or challenges and plan for how to address them
4. Read and understand any documentation provided or linked to in the _`FEATURE_SPEC`_


### Report
- Summarize the loaded context, including key guidelines, rules, project structure, and any specific feature requirements
- Highlight any potential challenges or considerations for the development work

Finish with saying: "Context primed for development work!"