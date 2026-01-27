---
description: Executes a Feature Implementation Specification that contains all implementation details
---

# Execute Feature Implementation Specification
Execute a fully-defined FIS document, focusing on autonomous, systematic and **COMPLETE** implementation with continuous validation.

## Variables
FIS_FILE_PATH: $ARGUMENTS


## Instructions

- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section in CLAUDE.md before starting work, including but not limited to:
  - **Foundational Rules and Guardrails**
  - **Foundational Development Guidelines and Standards** (e.g. Development, Architecture, UI/UX Guidelines etc.)
- **Autonomous Execution**: Agents work independently to complete tasks
- **Complete Implementation**: 100% completion required - no partial work  
- **No manual steps**: Make use of agents, tools and MCPs to ensure an autonomous process towards 100% completion - **MANUAL WORK = IMMEDIATE FAILURE**
- **Read and understand all instructions**: Read and understand all instructions in this command fully before proceeding!
- The FIS is the source of truth - follow it exactly
- No planning or decision-making - just execution
- Delegate as much work as possible to the available sub agents, and let the main claude code agent act as an orchestrator.
   - Use **foreground parallel agents (`run_in_background=false`)** when possible and there is no risk of conflicts - launch multiple Task calls in one message (**IMPORTANT:** Tasks such as compilation/building must typically not be done in parallel)
- If something is unclear, the FIS is incomplete (not this command)
- **IMPORTANT**: The *Final Validation Checklist* must be completed (each item must be verified to be completed and then checked off in the FIS) and all criteria must be met before considering the implementation done.
- **CRITICAL**: Validation tasks must be completed by different agents than implementation tasks to ensure independent verification


## Workflow


### Step 1: Load FIS and plan for execution
1. Read the FIS document at _`FIS_FILE_PATH`_, understand the Success Criteria, Scope & Boundaries, Architecture Decision Record (ADR), implementation plan, and validation strategies
2. Analyse the codebase to properly understand the project structure, relevant files and similar patterns
  - Use command like `tree -d` and `git ls-files | head -250` to get an overview of the codebase structure
3. Read any *`fis-implementation-notes.md`* document for additional context and learnings from previous stories
4. - **Read additional guidelines and documentation** - Read additional relevant guidelines and documentation (API, guides, reference, etc.) as needed
5. Use task management tools to create todos/tasks for ALL tasks from the FIS (both implementation and validation tasks)
6. **Think hard** before you execute the plan. Make sure the plan is comprehensive and addresses all requirements.


### Step 2: FIS Execution
Execute the implementation and validation as detailed in the *Implementation Plan* section of the FIS. 

*For each task:*
- Make sure relevant docs and context as defined under *Critical Documentation & Context* in the FIS are properly referenced and used
- Execute each task in sequence
- Make sure tasks marked with [P] are executed with **foreground parallel agents (`run_in_background=false`)** - launch multiple Task calls in one message.
- When possible, delegate tasks to appropriate sub-agents (e.g. `cc-workflows:qa-test-engineer`, `cc-workflows:build-troubleshooter`, `cc-workflows:solution-architect`, `cc-workflows:ui-ux-designer`, `cc-workflows:screenshot-validation-specialist`, `cc-workflows:documentation-lookup`, etc.)
- Update todos/tasks using task management tools and mark each task as complete *in the FIS* when successfully implemented and verified against success criteria
- If encountering build issues or runtime errors, delegate troubleshooting work to `cc-workflows:build-troubleshooter`


### Step 3: Final Quality Assurance
After all implementation and validation tasks are completed, perform a final quality assurance pass:

- **Check for Functionality Gaps and Requirement Mismatches**
  - Missing features or capabilities that were required
  - Implemented features that don't match requirements
  - Incomplete implementations (partially done features)
  - Missing error handling, edge cases, or validation

- **Code and Solution Correctness and Simplification Opportunities**
  - Given what was implemented, is there a better, simpler or more efficient way to achieve the same outcome?
  - Use the `code-simplifier` agent to optimize and improve code quality, focusing on consistency, maintainability and simplicity


### Step 4: Evaluation, Iteration and Completion
- Check all success criteria in the FIS are met
- Ensure all checkboxes in FIS are marked complete (- [x])
- Update progress summary in the FIS


#### Additional Iterations
- If the implementation does not meet the success criteria, or there are defects, analysis and review feedback that needs addressing, plan another Implementation Iteration:
  - Analyze the problems and use feedback from code reviews and testing to inform the next iteration
  - **Update task tracking**: Use task management tools to create new tasks for implementation and validation (using the _Validation Strategy_) as needed
  - Execute next iteration (i.e. *steps 2-3*)


### Step 5: Update Implementation Notes documents with important learnings and decsisions
After completed implementation, update the *Implementation Notes* document (`fis-implementation-notes.md`, in the same directory as the FIS file) with important learnings and decisions made during implementation.

For instance: 
- Description of what was implemented and how different parts of the implementation relate and integrate with each other
- Key challenges faced and how they were overcome
- Important decisions made and their rationale
- Any deviations from the original plan and why
- Suggestions for future improvements or related features
