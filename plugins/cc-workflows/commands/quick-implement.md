---
name: quick-implement
description: Quick implementation path for small features or fixes with verification
argument-hint: <spec> | --issue <number>
---

# Quick Implement with Verification

Fast implementation path for small features, bug fixes, or GitHub issues. Bypasses FIS workflow for quick turnaround while maintaining verification quality.

**For larger features, use the full workflow:** `clarify` → `spec-create` → `spec-execute`


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

- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section in CLAUDE.md before starting work, including but not limited to:
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

1. Understand requirements and scope - interpret as *what* to implement, not *how*
2. Analyze codebase structure and relevant patterns
   - Use `tree -d` and `git ls-files | head -250` for overview
   - For complex exploration, use the Explore agent
3. Read relevant documentation (use `cc-workflows:documentation-lookup` as needed)
4. Identify roadblocks and plan mitigation
5. Break down into manageable todos/tasks and use task management tools to track them
6. **Think hard** - ensure plan is comprehensive

**Gate**: Plan complete, all requirements understood


### Phase 2: Implementation Loop

Iterative cycle: Implementation → Verification → Evaluation

#### Step 1: Implementation

- Write code following existing codebase patterns
- Follow project guidelines strictly
- Use **foreground parallel agents (`run_in_background=false`)** for independent tasks - multiple Task calls in one message
- Create/update tests alongside implementation
- Delegate build issues to `cc-workflows:build-troubleshooter`

#### Step 2: Verification

Run using **foreground parallel agents (`run_in_background=false`)** - multiple Task calls in one message:

##### 2.1. Code & Architecture Review
- Static analysis, linting, type checking
- Use the `/code-review` skill for comprehensive review (code quality, security, architecture, UI/UX)

##### 2.2. Run Tests
- Execute all tests
- Use project-specific test commands
- Fix issues that arise

##### 2.3. Visual Validation (if applicable)
- Follow Visual Validation Protocol from project guidelines
- Verify UI changes meet design specs

#### Step 3: Evaluation

- Verify implementation meets all requirements
- Review work against each task's acceptance criteria
- Mark completed todos in tracking

**If issues remain:**
- Analyze feedback from reviews and testing
- Request user clarification if needed
- Update todos for next iteration
- Execute another Implementation Loop

**Gate**: All validations pass - builds correctly, tests pass, no review issues, no regressions


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