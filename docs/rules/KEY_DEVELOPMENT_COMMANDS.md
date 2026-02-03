# Key Development Commands

## Running the Application
```bash
# Start development server
[TODO: YOUR_START_COMMAND]  # e.g., deno task dev, ./gradlew bootRun, python app.py

# Application URL for testing
[TODO: YOUR_APP_URL]  # e.g., http://localhost:3000
```


## Code Quality (Formatting, Linting and Type Checking)
```bash
# Format modified code (run after each task)
[TODO: YOUR_FORMAT_COMMAND]  # e.g., deno fmt routes/index.tsx

# Linting and type checking (run after each task)
[TODO: YOUR_LINT_COMMAND]  # e.g., deno lint routes/index.tsx
```


## Testing (Unit, Integration, E2E)
```bash
# Run all tests
[TODO: YOUR_TEST_COMMAND]  # e.g., deno task test, pytest, mvn test

# Run specific test
[TODO: YOUR_SPECIFIC_TEST_COMMAND]  # e.g., deno task test tests/unit/components-basic.test.tsx
```


---


## Visial Validation _[TODO: If applicable]_

**Launch** app and test at [YOUR_APP_URL]

### Visual Validation Tools _[TODO: Update with relevant tools]_
- **Playwright MCP**: If available, use `mcp__playwright__*` commands
- **Screenshots**: [YOUR_SCREENSHOT_TOOL] # e.g., peekaboo, screenshot cli

### Visual Validation Guidelines _[TODO: Update with relevant guidelines]_
When performing visual validation, always follow this process:
- Get semantic page/screen structure first
- Capture screenshots - prefer capturing only relevant sections/components if possible
- **Always** use _`visual-validation-specialist`_ agent for screenshot analysis and comparison against baselines (if available)
- Make targeted fixes to specific components based on visual diffs
- Re-capture and re-validate only the affected components until no unexpected diffs remain
