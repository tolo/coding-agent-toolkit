---
description: Review implementation against requirements - includes code review and gap analysis with actionable report.
argument-hint: [Additional Context]
---

# Review Implementation
Comprehensive post-execution review that validates implementation against requirements, performs code review, and identifies gaps. Generates actionable report with findings and remediation plan.


## Variables

ADDITIONAL_CONTEXT: $ARGUMENTS
*(Optional: Additional requirements or context beyond what's in the codebase)*


## Instructions

- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section as defined in AGENTS.md, etc. before starting work, including but not limited to:
  - **Foundational Rules and Guardrails**
  - **Foundational Development Guidelines and Standards** (e.g. Development, Architecture, UI/UX Guidelines etc.)
- **Read-only analysis** - No code changes, commits, or modifications during analysis
- **Be thorough** - Don't skip steps or rush analysis; completeness is critical
- **Use `code-review` skill if available** - Delegate code review to the skill if your agent supports it
- **Document everything** - All findings and recommendations must be captured in final report


## Workflow

### 1. Compile and Analyze Requirements

Gather and understand all requirements from multiple sources:

- **Code Context** - Review recent commits, branches, and work-in-progress to understand what's being implemented
- **Documentation** - Check specs, ADRs, design docs, PRDs, or feature documentation in the codebase
- **Issue/Ticket References** - Look for referenced issues, tickets, or PRs that define requirements
- **Code Comments** - Review TODO comments, function documentation, or inline requirement notes
- **ADDITIONAL_CONTEXT** - If specified via arguments, these requirements take precedence and should be the primary focus
- **Read additional guidelines and documentation** - Read additional relevant guidelines and documentation (API, guides, reference, etc.) as needed

Create a clear, consolidated view of:
- What functionality should be implemented
- What success criteria must be met
- What constraints or non-functional requirements apply
- What the expected behavior and user experience should be

**Gate**: All requirements compiled, understood, and documented


### 2. Analyze Current Implementation

Map the current state of the implementation:

- **Implementation Status**
  - Use `git status --porcelain` to identify modified, added, and deleted files
  - Use `git diff` to see actual code changes
  - Use `git log` with options like `--since="1 week ago"` or `--author` to review recent commit history
  - Check for work-in-progress branches or uncommitted changes

- **Codebase Understanding**
  - Use `tree -d -L 3` to understand directory structure
  - Use `git ls-files` to see all tracked files
  - Identify relevant files and components affected by the implementation
  - Look for existing patterns, conventions, and similar implementations to understand expected approach

- **Implementation Inventory**
  - List all components, modules, or features that have been added or modified
  - Identify what's completed vs. what appears incomplete
  - Map relationships and dependencies between modified components

**Gate**: Current implementation state fully mapped and documented


### 3. Review Solution Quality

Review general quality, soundness and adherence to guidelines, standards and best practices of current implementation.

#### Code Analysis
- Run static analysis, linting, type checking as per project guidelines
- Use IDE diagnostics (`mcp__ide__getDiagnostics`) if available

#### Comprehensive Code Review
**Use the `code-review` skill if available** to perform thorough review covering:
- Code quality (correctness, readability, best practices, performance)
- Architecture (CUPID principles, DDD patterns, anti-patterns)
- Security (OWASP Top 10, injection prevention, auth, data protection)
- UI/UX (if applicable)

If the skill is available, it runs in a forked context and generates a detailed report. Incorporate findings into the gap analysis.

**Gate**: Quality reviews complete, over-engineering identified, all issues documented


### 4. Gap Analysis

Systematically identify all gaps between requirements and implementation:

- **Functionality Gaps**
  - Missing features or capabilities that were required
  - Incomplete implementations (partially done features)
  - Unfulfilled success criteria or acceptance criteria
  - Missing error handling, edge cases, or validation

- **Integration Gaps**
  - Missing integration points between components
  - Incomplete data flows or communication paths
  - Missing API endpoints, database migrations, or configuration
  - Broken or incomplete dependencies between modules

- **Requirement Mismatches**
  - Implemented features that don't match requirements
  - Incorrect behavior or logic
  - Performance, scalability, or security requirements not met
  - Non-functional requirements (accessibility, internationalization, etc.) not addressed

- **Consistency Gaps**
  - Inconsistencies with existing codebase patterns
  - Style or convention violations
  - Documentation gaps (missing docs for new features)
  - Test coverage gaps (missing unit/integration/e2e tests)

- **Holistic Sanity Check**
  - Zoom out and review the complete picture
  - Does the implementation make sense as a whole?
  - Are there obvious missing pieces when looking end-to-end?
  - Would the feature actually work for end users?
  - Are there hidden assumptions or technical debt introduced?

**Gate**: All gaps comprehensively identified and documented


### 5. Retrospective Review

Reflect on the implementation process, approach, and decisions to extract learnings and identify process improvements:

- **Implementation Approach Analysis** - Evaluate the technical approach and methodology used. Was it sound? Were there better alternatives?

- **What Went Well** - Identify successful patterns, decisions, or practices that should be repeated in future work.

- **What Didn't Go Well** - Identify problems, inefficiencies, or missteps that occurred during implementation.

- **Deviation Analysis** - Compare actual implementation against any original plans, designs, or architectural decisions. Understand why deviations occurred and whether they were justified.

- **Root Cause Analysis** - For any significant gaps or issues found, perform root cause analysis to understand why they occurred (e.g., unclear requirements, technical complexity, time pressure, missing knowledge).

- **Process Improvements** - Identify specific process, workflow, or practice improvements that could prevent similar issues in future implementations.

- **Knowledge Gaps** - Document any areas where lack of knowledge or documentation led to issues.

**Gate**: Retrospective complete with actionable insights documented


### 6. Remediation Plan

Create a comprehensive, prioritized plan for addressing all identified gaps and issues:

- **Issue Categorization** - Group all identified issues into logical categories:
  - Critical: Blocks core functionality, security vulnerabilities, data loss risks
  - High: Significant functionality gaps, major quality issues, architectural problems
  - Medium: Minor functionality gaps, code quality issues, maintainability concerns
  - Low: Nice-to-have improvements, minor optimizations, cosmetic issues

- **Dependency Analysis** - Identify dependencies between fixes. Which issues must be resolved before others? Which can be done in parallel?

- **Risk Assessment** - Evaluate risk for each remediation item:
  - Complexity: How difficult is the fix?
  - Blast radius: How much code will be affected?
  - Uncertainty: Are requirements/solutions clear?
  - Breaking changes: Will this affect existing functionality?

- **Sequencing Strategy** - Determine optimal order for addressing issues:
  - Resolve blockers first (critical items that block other work)
  - Group related fixes together for efficiency
  - Consider quick wins that provide immediate value
  - Balance risk vs. impact

- **Remediation Steps** - For each issue/gap, define:
  - Clear description of the problem
  - Proposed solution approach
  - Affected components/files
  - Dependencies on other fixes
  - Acceptance criteria

- **Rollout Considerations** - Consider how fixes should be delivered:
  - Can issues be fixed incrementally or require big-bang approach?
  - Are there rollback strategies for risky changes?
  - What testing/validation is needed for each fix?

**Gate**: Comprehensive, actionable remediation plan created


## Report

Your job is *ONLY* to analyze and generate report. Do *NOT* make any code changes or commits.

Generate markdown report with:
- **Executive Summary** - What was analyzed, overall assessment, high-level findings
- **Requirements Analysis** - Requirements identified, ambiguities or unclear items
- **Implementation Overview** - What was implemented, components/files modified, approach taken
- **Quality Review Findings** - Code quality, security, architecture, maintainability, UI/UX, performance issues
- **Over-Engineering Analysis** - Unnecessary complexity, premature optimizations, excessive layering, feature bloat, technology overkill, pattern misapplication (with simpler alternatives)
- **Gap Analysis Results** - Functionality gaps, integration gaps, requirement mismatches, consistency issues, missing tests/docs
- **Retrospective Insights** - What went well/didn't go well, root causes, process improvements, lessons learned
- **Remediation Plan** - Categorized/prioritized issues (Critical/High/Medium/Low), dependencies, sequencing, risk assessment, specific remediation steps, acceptance criteria
- **Appendix** (if needed) - Code snippets, technical details, reference materials

Store report in: `<project_root>/docs/temp/gap-analysis/<feature-name>-gap-analysis-<coding-agent-name>-<YYYY-MM-DD>.md`

Inform user of report location when complete.
