---
description: Executes a Feature Implementation Specification (simple, no sub-agents)
argument-hint: [Path to FIS file]
---

# Execute Feature Implementation Specification (Simple)

Execute a fully-defined FIS document with direct, systematic implementation and validation.

## Variables
FIS_FILE_PATH: $ARGUMENTS


## Instructions

- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section as defined in AGENTS.md, etc. before starting work, including but not limited to:
  - **Foundational Rules and Guardrails**
  - **Foundational Development Guidelines and Standards** (e.g. Development, Architecture, UI/UX Guidelines etc.)
- Use `code-review` skill for validation if available
- **Complete Implementation**: 100% completion required - no partial work
- **Fix-forward approach** - address issues immediately
- The FIS is the source of truth - follow it exactly
- No planning or decision-making beyond what's in the FIS
- If something is unclear, the FIS is incomplete (not this command)
- **IMPORTANT**: The *Final Validation Checklist* must be completed (each item verified and checked off in the FIS) before considering implementation done


## Workflow

### Phase 1: Load FIS and Plan Execution

1. Read the FIS document at _`FIS_FILE_PATH`_
2. Understand Success Criteria, Scope & Boundaries, ADR, implementation plan, and validation strategies
3. **Read additional guidelines and documentation** - Read additional relevant guidelines and documentation (API, guides, reference, etc.) as needed
4. Analyze codebase to understand project structure and relevant patterns
   - Use `tree -d` and `git ls-files | head -250` for overview
5. Read any `fis-implementation-notes.md` document for additional context from previous work
6. Use task management tools to create todos for ALL tasks from the FIS (both implementation and validation tasks)

**Gate**: FIS understood, todos created


### Phase 2: Execute Implementation Tasks

Execute the implementation tasks (TI01, TI02, etc.) from the FIS.

*For each task:*
- Read relevant docs and context as defined under *Critical Documentation & Context* in the FIS
- Execute each task in sequence
- Update todos and mark each task complete *in the FIS* when implemented
- Verify task against relevant success criteria before moving on

**Gate**: All implementation tasks complete


### Phase 3: Execute Validation Tasks

Execute the validation tasks (TV01-TV04) as defined in the FIS *Validation Strategy*.
- Follow the FIS validation levels in order
- Run all applicable validation (code review, testing, visual)
- Address issues found during validation before proceeding
- Mark each validation task complete in the FIS

**Gate**: All validation tasks complete, issues addressed


### Phase 4: Final QA and Completion
- Check for functionality gaps or requirement mismatches
- Verify ALL success criteria in FIS are met
- Verify ALL task checkboxes marked complete (- [x])
- Verify *Final Validation Checklist* items satisfied

#### Additional Iterations
If success criteria not met:
- Analyze gaps from validation feedback
- Create new tasks for fixes
- Re-execute Phases 2-4


## Report: Update Implementation Notes documents with important learnings and decsisions
After completion, update `fis-implementation-notes.md` with important implementation, making sure to keep them very concise and to the point (avoid any unnecessary verbosity and code listings etc).

Including details like:
- What was implemented and how parts integrate
- Key challenges and solutions
- Decisions and deviations from plan
- Unresolved issues or future suggestions
