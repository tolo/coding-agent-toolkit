---
description: Perform thorough standalone code review with embedded checklists
argument-hint: [Additional Context]
---

# Standalone Code Review Command (v3)

Comprehensive review covering code quality, security, architecture, and UI/UX aspects.
Self-contained with all checklists embedded as appendices.

## Variables

ADDITIONAL_CONTEXT: $ARGUMENTS


## Instructions

- **Non-modifying analysis only** - Do not make code changes
- Follow project guidelines from AGENTS.md, etc. if available
- Use embedded checklists (see [Appendices](#appendices)) for systematic assessment
- No sub-agents required (direct review approach)


## Workflow

### Phase 1: Context Analysis

1. **Determine review scope**:
   - If specific files/dirs in ADDITIONAL_CONTEXT: Focus on those
   - If PR number mentioned: Run `gh pr diff <number>` to get changes
   - If focus area specified (security, architecture, ui): Emphasize in Phase 2
   - Otherwise: Use git status/diff for scope
2. Run `git status --porcelain` and `git diff` to identify changes
3. Run `git log -10 --oneline` to understand recent commits
4. Use `tree -d -L 3` and `git ls-files | head -250` for codebase overview
5. Identify applicable review types based on changed files
6. Read project guidelines if available (CLAUDE.md, docs/guidelines/, etc.)

**Gate**: Scope determined, relevant files identified


### Phase 2: Review Execution

Perform applicable reviews using the embedded checklists.

#### Code Analysis
- Run static analysis, linting, type checking per project config
- Use IDE diagnostics if available

#### Code Review
**Checklist**: [Appendix A - Code Review](#appendix-a---code-review-checklist)

Assess:
- Correctness, logic errors, edge cases, error handling
- Readability, naming, code organization
- Best practices, DRY, design patterns, anti-patterns
- Performance (N+1 queries, algorithms, caching)
- Maintainability, testability, documentation, tech debt

#### Security Review
**Checklist**: [Appendix B - Security Review](#appendix-b---security-review-checklist)

Assess:
- Input validation & sanitization
- Injection prevention (SQL, command, XSS, path traversal)
- Authentication & authorization
- Cryptography (encryption, hashing, key management)
- Data protection (secrets, logging exposure)
- API security, headers, CORS, CSRF
- OWASP Top 10 coverage

#### Architecture Review
**Checklist**: [Appendix C - Architecture Review](#appendix-c---architectural-review-checklist)

Assess:
- CUPID principles (Composable, Unix philosophy, Predictable, Idiomatic, Domain-aligned)
- DDD patterns (bounded contexts, aggregates, domain events)
- Pattern adherence (clean architecture, service boundaries, API design)
- Anti-patterns, performance, scalability, resilience

#### UI/UX Review (when applicable)
**Checklist**: [Appendix D - UI/UX Review](#appendix-d---uiux-review-checklist)

Assess:
- Visual quality (layout, typography, color/contrast, responsive)
- Usability (5-second clarity, touch targets, cognitive load)
- Platform conventions (iOS HIG, Material Design, web standards)
- Accessibility (WCAG 2.2), performance, interaction patterns

**Gate**: All applicable reviews complete


### Phase 3: Analysis & Findings

1. Categorize findings by priority:
   - **CRITICAL**: Security vulnerabilities, data loss risks, broken functionality
   - **HIGH**: Performance issues, maintainability concerns, minor security issues
   - **SUGGESTIONS**: Improvements, optimizations, enhancements

2. Identify obsolete/temporary files and code requiring cleanup
3. Check for unmotivated complexity, over-engineering, or duplication
4. Verify adherence to project guidelines and patterns

**Gate**: Findings categorized and validated


## Report

Your job is *ONLY* to review and generate report. Do *NOT* make any code changes or commits.

Generate markdown report:

```markdown
# Review Report - [Date]

## Summary
[2-3 sentence overview of review scope and overall assessment]

## CRITICAL ISSUES
[Each issue: Title, Impact, Location, Fix Required]

## HIGH PRIORITY
[Each issue: Title, Impact, Location, Recommendation]

## SUGGESTIONS
[Brief list of improvements]

## Cleanup Required
- [Obsolete/temporary files to remove]
- [Dead code to remove]

## Compliance
- Guidelines adherence: [Assessment]
- Architecture patterns: [Assessment]
- Security best practices: [Assessment]
- [UI/UX if applicable]: [Assessment]

## Next Steps
1. [Prioritized action items]
```

Store report at: `<project_root>/.agent_temp/reviews/<feature-name>-code-review-<YYYY-MM-DD>.md`

Return report location to user.


---


# Appendices

## Appendix A - Code Review Checklist

### Pre-Review
- [ ] Understand code's purpose and context
- [ ] Review changed files (`git diff` or equivalent)
- [ ] Check project guidelines if available

### Code Quality

#### Correctness & Logic
- [ ] No bugs or logical errors
- [ ] Edge cases handled (null/undefined, empty arrays, boundary conditions)
- [ ] Error handling comprehensive (try/catch, error propagation, user-friendly messages)
- [ ] Async operations handled correctly (promises, race conditions, error handling)
- [ ] Business logic correct and complete

#### Readability & Clarity
- [ ] Code is simple, clear, self-documenting
- [ ] Naming is descriptive, consistent, follows conventions
- [ ] Functions/methods focused, reasonably sized
- [ ] Complex logic explained with comments where needed
- [ ] Magic numbers/strings replaced with named constants

#### Best Practices
- [ ] Language/framework idioms followed
- [ ] DRY principle applied pragmatically
- [ ] SOLID/CUPID principles respected
- [ ] No code duplication without justification
- [ ] Appropriate design patterns used
- [ ] No anti-patterns (god objects, circular dependencies, tight coupling)

#### Performance
- [ ] No obvious performance issues (N+1 queries, inefficient algorithms)
- [ ] Appropriate data structures used
- [ ] Resource usage reasonable (memory, CPU, network)
- [ ] Caching applied where beneficial
- [ ] Database queries optimized (indexes, pagination)

### Maintainability

#### Code Organization
- [ ] Separation of concerns clear
- [ ] Responsibilities well-distributed (no god objects)
- [ ] Layer boundaries respected
- [ ] Module/package structure logical
- [ ] Files/classes reasonably sized

#### Testability
- [ ] Code testable (dependency injection, pure functions where possible)
- [ ] Test coverage adequate (critical paths, edge cases)
- [ ] Tests pass and are meaningful
- [ ] Tests are maintainable and readable

#### Documentation
- [ ] Public APIs documented
- [ ] Complex algorithms explained
- [ ] Assumptions and constraints documented
- [ ] No obsolete comments or TODOs without context

#### Technical Debt
- [ ] No new technical debt without explicit acknowledgment
- [ ] Workarounds documented with reason and follow-up plan
- [ ] Deprecated code usage avoided
- [ ] Code complexity reasonable

### Additional Checks

#### Regression Prevention
- [ ] Existing functionality still works
- [ ] Tests updated/added for changes
- [ ] Backward compatibility maintained or migration path clear

#### Operational Concerns
- [ ] Logging appropriate (level, content, no sensitive data)
- [ ] Monitoring/observability supported
- [ ] Error messages actionable and user-friendly
- [ ] Resource cleanup (connections, files, memory)

### Issue Classification
- **CRITICAL**: Data loss/corruption risks, breaking changes, critical bugs
- **HIGH**: Performance issues, maintainability concerns, incorrect error handling
- **SUGGESTIONS**: Code style, refactoring opportunities, test coverage gaps


---


## Appendix B - Security Review Checklist

Based on [OWASP Top 10:2025](https://owasp.org/Top10/2025/).

### Pre-Review
- [ ] Identify trust boundaries, attack surface, and sensitive data flows
- [ ] Review threat model and security requirements
- [ ] Check compliance needs (GDPR, HIPAA, PCI-DSS, etc.)

### A01:2025 - Broken Access Control
- [ ] Server-side access control enforced (not client-side only)
- [ ] Default deny - explicit allow required for each resource
- [ ] IDOR prevented - object references validated against user context
- [ ] Horizontal/vertical privilege escalation prevented
- [ ] CORS configured restrictively (no wildcard in production)
- [ ] CSRF protection on state-changing operations
- [ ] SSRF prevented - URL destinations validated
- [ ] Rate limiting on sensitive endpoints

### A02:2025 - Security Misconfiguration
- [ ] Hardened default configurations applied
- [ ] Unnecessary features, ports, services disabled
- [ ] Security headers configured (CSP, HSTS, X-Content-Type-Options)
- [ ] Error pages don't leak stack traces or internal details
- [ ] Directory listing disabled, .git and backup files not exposed
- [ ] Debug endpoints disabled in production

### A03:2025 - Software Supply Chain Failures
- [ ] Transitive dependencies tracked and scanned
- [ ] Automated vulnerability scanning in CI/CD
- [ ] Dependencies from trusted sources, integrity verified
- [ ] Unused dependencies removed
- [ ] Patch management process in place

### A04:2025 - Cryptographic Failures
- [ ] Sensitive data classified and minimized
- [ ] TLS 1.2+ enforced for all connections
- [ ] Strong algorithms only (no MD5, SHA-1, DES, RC4)
- [ ] Passwords hashed with Argon2id, bcrypt, or scrypt
- [ ] Encryption keys properly managed (not in code, rotation supported)
- [ ] No sensitive data in URLs, logs, or error messages

### A05:2025 - Injection
- [ ] Parameterized queries / prepared statements used
- [ ] Input validated with allowlists, type/bounds checking
- [ ] Output encoding context-appropriate (HTML, JS, URL, CSS)
- [ ] ORM/safe APIs preferred over raw queries
- [ ] Command execution avoided; if needed, arguments as arrays
- [ ] CSP configured to mitigate XSS impact

### A06:2025 - Insecure Design
- [ ] Threat modeling performed
- [ ] Secure design patterns applied
- [ ] Business logic tested for abuse scenarios
- [ ] Resource limits prevent DoS
- [ ] Tenant segregation verified (multi-tenant systems)

### A07:2025 - Authentication Failures
- [ ] No default or weak credentials
- [ ] Brute force protection (lockout, rate limiting)
- [ ] No username enumeration (generic error messages)
- [ ] Session invalidated on logout/password change
- [ ] Session cookies: HttpOnly, Secure, SameSite
- [ ] MFA available for sensitive operations

### A08:2025 - Software or Data Integrity Failures
- [ ] CI/CD pipeline secured (access control, audit logging)
- [ ] Code review required for critical changes
- [ ] Unsigned code/updates rejected
- [ ] Deserialization of untrusted data avoided or strictly validated

### A09:2025 - Security Logging and Alerting Failures
- [ ] Auth events logged (login, logout, failures)
- [ ] Access control failures logged
- [ ] No sensitive data in logs (passwords, tokens, PII)
- [ ] Log injection prevented
- [ ] Alerting configured for suspicious patterns

### A10:2025 - Mishandling of Exceptional Conditions
- [ ] Fail securely / fail closed (deny access on error)
- [ ] Transactions rolled back completely on failure
- [ ] Resource exhaustion prevented (limits, quotas, timeouts)
- [ ] Race conditions addressed in critical operations
- [ ] Errors logged server-side, generic messages to users

### Issue Classification
- **CRITICAL**: RCE, SQL injection, auth bypass, privilege escalation, credential exposure
- **HIGH**: Stored XSS, CSRF, IDOR, session fixation, missing headers, vulnerable deps
- **MEDIUM**: Reflected XSS, info disclosure, missing rate limiting, verbose errors
- **LOW**: Best practice deviations, defense-in-depth improvements


---


## Appendix C - Architectural Review Checklist

### Pre-Review
- [ ] Understand architectural scope and intent
- [ ] Review project architectural guidelines (ADRs if available)
- [ ] Identify changed components and their relationships

### CUPID Principles Assessment

#### C - Composable
- [ ] Components work together with minimal dependencies
- [ ] Clear, well-defined interfaces between components
- [ ] Minimal coupling, easy to swap/extend components
- [ ] Plugin architectures where appropriate

#### U - Unix Philosophy
- [ ] Each component/service does one thing well
- [ ] Appropriate granularity (not too fine, not too coarse)
- [ ] Clear separation of concerns
- [ ] Focused APIs without feature creep

#### P - Predictable
- [ ] System behavior consistent and unsurprising
- [ ] Consistent error handling patterns
- [ ] Predictable performance characteristics
- [ ] Well-defined failure modes and recovery

#### I - Idiomatic
- [ ] Industry-standard patterns followed
- [ ] Consistent technology choices
- [ ] Familiar deployment and operational patterns
- [ ] Convention-over-configuration where beneficial

#### D - Domain-Aligned
- [ ] System structure reflects business domains
- [ ] Service boundaries match business capabilities
- [ ] Business-meaningful names and interfaces

### DDD Assessment

#### Strategic Level
- [ ] Bounded contexts clearly defined and appropriately sized
- [ ] Context mapping reflects business relationships
- [ ] Anti-corruption layers for external integrations
- [ ] Ubiquitous language used consistently

#### Tactical Level
- [ ] Entities properly identified (unique identity, mutable state)
- [ ] Value objects used appropriately (immutable, compared by value)
- [ ] Aggregates enforce business invariants correctly
- [ ] Domain events capture important business occurrences

### Pattern Adherence

#### Clean Architecture / Layering
- [ ] Dependency rule respected (dependencies point inward)
- [ ] Domain layer pure (no framework/infrastructure dependencies)
- [ ] Layer boundaries not crossed inappropriately

#### Service Architecture
- [ ] Service boundaries clear and well-justified
- [ ] High cohesion within services, low coupling between
- [ ] Communication patterns appropriate (sync/async)
- [ ] Shared database anti-pattern avoided

#### API Design
- [ ] Clear API contracts (OpenAPI, GraphQL schema, etc.)
- [ ] RESTful principles followed (or GraphQL/gRPC as appropriate)
- [ ] Proper HTTP status codes
- [ ] Versioning strategy for breaking changes

#### Data Architecture
- [ ] Database choice appropriate
- [ ] Schema design reflects domain model
- [ ] Proper indexing strategy
- [ ] Transaction boundaries appropriate

### Anti-Pattern Detection
- [ ] No god objects
- [ ] No circular dependencies
- [ ] No tight coupling
- [ ] No framework coupling in business logic
- [ ] No chatty interfaces
- [ ] No shotgun surgery (changes requiring many file edits)

### Performance & Scalability
- [ ] Horizontal/vertical scaling strategy clear
- [ ] Stateless design where appropriate
- [ ] No obvious performance bottlenecks
- [ ] Database queries optimized
- [ ] Background processing for long-running tasks

### Resilience & Reliability
- [ ] Circuit breaker pattern for external dependencies
- [ ] Retry logic with exponential backoff
- [ ] Timeout handling appropriate
- [ ] Graceful degradation for failures

### Observability
- [ ] Logging strategy comprehensive (structured logging)
- [ ] Monitoring metrics defined
- [ ] Health check endpoints available
- [ ] No sensitive data in logs

### Issue Classification
- **CRITICAL**: Architectural violations causing serious issues, security vulns, data loss risks
- **HIGH**: Anti-patterns requiring refactoring, maintainability concerns, coupling issues
- **SUGGESTIONS**: Refactoring opportunities, pattern improvements, optimizations


---


## Appendix D - UI/UX Review Checklist

### Pre-Review
- [ ] Identify screens/components to review
- [ ] Capture screenshots across target devices (mobile, tablet, desktop)
- [ ] Capture all relevant states (idle, active, loading, error, empty)
- [ ] Compare against design specs if available

### Visual Quality & Layout

#### Layout Integrity
- [ ] No overlapping elements or broken layouts
- [ ] Consistent spacing follows 8px grid system
- [ ] Proper alignment (left/center/right justification)
- [ ] Respects safe areas (notch, system bars, navigation)

#### Typography
- [ ] Minimum sizes met (12pt mobile, 14px desktop)
- [ ] Clear hierarchy (max 3 sizes per screen)
- [ ] No text truncation blocking functionality
- [ ] Readable content width (≤65ch)

#### Color & Contrast
- [ ] Text contrast ≥4.5:1 (WCAG AA)
- [ ] Large text contrast ≥3:1 (18pt+ or 14pt+ bold)
- [ ] Interactive elements contrast ≥3:1
- [ ] Color not sole indicator (icons/patterns used)

#### Responsive Behavior
- [ ] Content reflows gracefully at all breakpoints
- [ ] Images scale appropriately
- [ ] No horizontal scroll (unless intentional)

### Usability Excellence

#### 5-Second Clarity Test
- [ ] Screen purpose obvious within 5 seconds
- [ ] Primary action immediately identifiable
- [ ] Current location clear (breadcrumbs, active nav)
- [ ] Visual hierarchy guides attention correctly

#### Touch/Click Targets
- [ ] Mobile minimum: 44pt × 44pt
- [ ] Desktop minimum: 32px × 32px
- [ ] Spacing between targets: ≥8pt/px
- [ ] Thumb-zone optimization (primary actions in bottom 60%)

#### Cognitive Load
- [ ] ≤7 simultaneous choices per screen
- [ ] Clear visual hierarchy reduces mental effort
- [ ] Related items grouped with whitespace
- [ ] Progressive disclosure for complex features

#### Task Efficiency
- [ ] Primary flows achievable in ≤3 taps/clicks
- [ ] Minimal scrolling for core actions
- [ ] Smart defaults and auto-fill where possible
- [ ] Clear path to task completion

#### System Feedback
- [ ] Immediate response to all interactions (<100ms visual)
- [ ] Loading states for operations (spinner/skeleton)
- [ ] Progress bars for long operations
- [ ] Success/error messages clear and actionable

### Platform Conventions

#### iOS (HIG)
- [ ] Tab bar at bottom (≤5 items)
- [ ] Back button top-left or swipe-right
- [ ] Primary action top-right
- [ ] Respects safe areas

#### Android (Material Design)
- [ ] Bottom navigation or drawer
- [ ] FAB for primary action (bottom-right)
- [ ] Ripple effect on taps

#### Web
- [ ] Logo top-left links to home
- [ ] Horizontal menu (desktop) or hamburger (mobile)
- [ ] Standard web conventions followed

### Accessibility (WCAG 2.2)

#### Visual
- [ ] All text ≥4.5:1 contrast
- [ ] Focus indicators visible on all interactive elements
- [ ] Color never sole indicator
- [ ] All images have descriptive alt text

#### Keyboard Navigation
- [ ] Tab order matches visual hierarchy
- [ ] All interactive elements keyboard accessible
- [ ] No keyboard traps
- [ ] Skip links for repetitive content

#### Screen Reader
- [ ] Semantic HTML (proper headings, landmarks)
- [ ] ARIA labels for icon-only buttons
- [ ] Form inputs properly labeled
- [ ] Error messages associated with fields

### Performance
- [ ] First Paint: <1 second
- [ ] Interactive: <3 seconds
- [ ] Images lazy-loaded below fold
- [ ] 60fps animations

### Issue Classification
- **IMMEDIATE**: Text truncation blocking tasks, elements outside safe areas, touch targets <44pt, broken layouts, critical a11y violations
- **HIGH**: Inconsistent spacing, minor alignment issues, >3 step paths, missing feedback, >3s load
- **ENHANCEMENT**: Visual refinements, micro-interaction improvements, animation polish
