---
description: Executes a Feature Implementation Specification (simple, no sub-agents)
argument-hint: [Path to FIS file]
---

# Execute Feature Implementation Specification (Simple)

Execute a fully-defined FIS document with direct, systematic implementation and validation.

## Variables
FIS_FILE_PATH: $ARGUMENTS


## Instructions

- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section as defined in CLAUDE.md, AGENTS.md, etc. before starting work, including but not limited to:
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


### Phase 2: Execute Implementation

Execute the implementation and validation as detailed in the *Implementation Plan* section of the FIS. 

*For each task:*
- Read relevant docs and context as defined under *Critical Documentation & Context* in the FIS
- Execute each task in sequence
- Update todos/tasks using task management tools and mark each task complete *in the FIS* when successfully implemented
- Verify task against relevant success criteria before moving on

**Gate**: All implementation tasks complete


### Step 3: Evaluation, Iteration and Completion
- Check all success criteria in the FIS are met
- Ensure all checkboxes in FIS are marked complete (- [x])
- Update progress summary in the FIS

#### Additional Iterations
- If the implementation does not meet the success criteria, or there are defects, analysis and review feedback that needs addressing, plan another Implementation Iteration:
  - Analyze the problems and use feedback from code reviews and testing to inform the next iteration
  - **Update task tracking**: Use task management tools to create new tasks for implementation and validation (using the _Validation Strategy_) as needed
  - Execute next iteration (i.e. *steps 2-3*)


### Step 4: Update Implementation Notes documents with important learnings and decsisions
After completed implementation, update the *Implementation Notes* document (`fis-implementation-notes.md`, in the same directory as the FIS file) with important learnings and decisions made during implementation.

For instance: 
- Description of what was implemented and how different parts of the implementation relate and integrate with each other
- Key challenges faced and how they were overcome
- Important decisions made and their rationale
- Any deviations from the original plan and why
- Suggestions for future improvements or related features
