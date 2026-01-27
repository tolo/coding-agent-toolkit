---
name: review-code
description: Perform a thorough review of code, architecture, UI, and security of the current implementation and generate a detailed report with prioritized findings. 
argument-hint: [Optional - specific files, PR number, or focus area]
---

# Review Report

Perform comprehensive code review and generate a detailed report with prioritized findings.

## Instructions

**Use the `code-review` skill** to review: $ARGUMENTS

If no arguments provided, review all recent changes (git status/diff).

**Argument types:**
- File paths → Review only those files
- PR number → Fetch and review PR changes via `gh pr diff`
- Focus area → Emphasize that aspect ("security", "architecture", "ui")
