---
description: Quick implementation path for small features or fixes with verification (simple, no sub-agents)
argument-hint: <spec> | --issue <number>
---

# Quick Implement with Verification (Simple)

Fast implementation path for small features, bug fixes, or GitHub issues. Bypasses FIS workflow for quick turnaround while maintaining verification quality.

**For larger features, use the full workflow:** `clarify-requirements` → `spec-generate` → `spec-execute`


## Variables

ARGUMENTS: $ARGUMENTS


## Usage

```
/quick-implement <feature description>        # Implement from inline spec
/quick-implement --issue 123                  # Implement from GitHub issue (auto-PR)
/quick-implement --issue 123 --no-pr          # From issue, skip PR creation
/quick-implement <spec> --pr                  # Inline spec + create PR
```


## Instructions

- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section as defined in AGENTS.md, etc. before starting work, including but not limited to:
  - **Foundational Rules and Guardrails**
  - **Foundational Development Guidelines and Standards** (e.g. Development, Architecture, UI/UX Guidelines etc.)
- **Autonomously and iteratively** implement with comprehensive verification
- **Iterate** until all requirements met, no defects remain, all reviews pass
- Use GitHub CLI (`gh`) for GitHub operations


## Workflow

### Phase 1: Analysis

#### 1.1. Parse Input & Get Requirements

**If `--issue` flag present:**
1. Extract issue number from arguments
2. Use `gh issue view <number>` to fetch issue details
3. Set `CREATE_PR=true` (unless `--no-pr` specified)
4. Create feature branch following project conventions

**Otherwise:**
1. Use inline specification from arguments
2. Set `CREATE_PR=true` only if `--pr` flag present

#### 1.2. Analyze & Plan

1. Understand requirements and scope — interpret as *what* to implement, not *how*
2. Analyze codebase structure and relevant patterns
   - Use `tree -d` and `git ls-files | head -250` for overview
3. Read relevant documentation and guidelines as needed
4. Identify roadblocks and plan mitigation
5. Break down into manageable tasks and use task management tools to track them

**Gate**: Plan complete, all requirements understood


### Phase 2: Implementation Loop

Repeat: Implementation → Verification → Evaluation until all requirements met.

#### Step 1: Implementation

- Write tests first where applicable, otherwise alongside implementation
- Write code following existing codebase patterns
- Follow project guidelines strictly

#### Step 2: Verification

##### 2.1. Code & Architecture Review
- Run static analysis, linting, type checking
- Use the `code-review` skill (if available) for comprehensive review
- Review code quality, security, architecture adherence

##### 2.2. Run Tests
- Execute all tests using project-specific test commands
- Fix issues that arise

##### 2.3. Visual Validation (if applicable)
- Follow Visual Validation Workflow from project guidelines
- Verify UI changes meet requirements by actual screenshot analysis

##### 2.4. Final Check
- Check for functionality gaps or requirement mismatches
- Look for simplification and maintainability improvements

#### Step 3: Evaluation

- Verify implementation meets all requirements
- Correct implementation must be verified through tests and visual validation (when applicable)
- Mark completed tasks in tracking

**If issues remain:**
- Analyze feedback from reviews and testing
- Request user clarification if needed
- Execute another Implementation Loop

**Gate**: All validations pass — builds correctly, tests pass, no review issues, no regressions


### Phase 3: Completion (conditional)

**Only execute if `CREATE_PR=true` or `--issue` mode:**

1. Commit changes with descriptive message
   - If from issue: reference issue number
2. Push branch to remote
3. Create PR using `gh pr create`:
   - Link to issue (include "Fixes #<number>" if applicable)
   - Brief description of implementation
   - Add relevant labels

**Gate**: PR created successfully (or changes committed if no PR)


## Report
After completed implementation, create concise *Implementation Notes* at the end of the original spec document (if present), or in a new file (e.g. `<feature-name>-implementation-notes.md`).

Keep notes very concise — include:
- Brief description of what was implemented
- Key challenges and solutions
- Decisions and deviations from plan
- Unresolved issues or future suggestions
