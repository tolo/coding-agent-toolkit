# GPT-Specific Prompt Engineering Guidelines

GPT-5+ specific behaviors, optimizations, and patterns.

**See Also**: [General Guidelines](PROMPT-ENGINEERING-GUIDELINES.md) - Model-agnostic core patterns

**Last Updated**: 2025-11-14

---

## Core GPT-5 Capabilities

GPT-5 represents substantial leap in:
- Agentic task performance
- Coding capabilities (leads all frontier models)
- Raw intelligence
- Steerability and instruction following

---

## Controlling Agentic Eagerness

GPT-5 operates on spectrum from highly autonomous to tightly controlled.

### Less Eager (Faster, More Controlled)

**Lower `reasoning_effort`**:
- Reduces exploration depth
- Improves efficiency and latency
- Many workflows work consistently at medium or low

**Define clear criteria**:
```xml
<context_gathering>
Goal: Get enough context fast. Parallelize discovery, stop as soon as you can act.

Method:
- Start broad, fan out to focused subqueries
- Launch varied queries in parallel; read top hits per query
- Deduplicate, cache; don't repeat queries
- Avoid over-searching

Early stop criteria:
- Can name exact content to change
- Top hits converge (~70%) on one area/path

Escalate once:
- If signals conflict or scope fuzzy, run one refined parallel batch, then proceed

Depth:
- Trace only symbols you'll modify or whose contracts you rely on

Loop:
- Batch search → minimal plan → complete task
- Search again only if validation fails
- Prefer acting over more searching
</context_gathering>
```

**Fixed tool call budgets** (maximally prescriptive):
```xml
<context_gathering>
- Search depth: very low
- Bias strongly towards correct answer as quickly as possible, even if might not be fully correct
- Usually, absolute maximum of 2 tool calls
- If need more time to investigate, update user with latest findings and open questions
</context_gathering>
```

**Escape hatches**: When limiting, provide flexibility:
```
"...even if it might not be fully correct"
```

### More Eager (Autonomous, Comprehensive)

**Increase `reasoning_effort`** and use persistence prompt:

```xml
<persistence>
- You are agent - keep going until user's query completely resolved before ending turn
- Only terminate when sure problem is solved
- Never stop when encountering uncertainty — research or deduce most reasonable approach and continue
- Do not ask human to confirm assumptions — decide most reasonable, proceed, document for user's reference after finishing
</persistence>
```

**Define stop conditions**:
- State clearly when agent should terminate
- Outline safe vs unsafe actions
- Define when acceptable to hand back to user

**Example**:
```
Shopping tools:
- Checkout/payment: Low uncertainty threshold (confirm with user)
- Search: High threshold (proceed autonomously)

Coding tools:
- Delete file: Low threshold (confirm)
- Grep search: High threshold (proceed)
```

---

## Tool Preambles

GPT-5 provides clear upfront plans and progress updates via "tool preamble" messages.

**Purpose**: For agentic trajectories monitored by users, intermittent updates improve UX.

**High-Quality Preamble Prompt**:
```xml
<tool_preambles>
- Begin by rephrasing user's goal in friendly, clear, concise manner before calling tools
- Immediately outline structured plan detailing each logical step
- As you execute file edits, narrate each step succinctly and sequentially, marking progress clearly
- Finish by summarizing completed work distinctly from upfront plan
</tool_preambles>
```

**Example Output**:
```
"I'm going to check live weather service for current conditions in San Francisco,
providing temperature in both Fahrenheit and Celsius."

[Tool call: get_weather(location="San Francisco, CA", unit="f")]
```

---

## Reasoning Effort Parameter

`reasoning_effort` controls how hard model thinks and how willingly it calls tools.

**Default**: `medium`

**When to adjust**:
- **Low/Medium**: Simple, clear tasks; minimize latency
- **High**: Complex, multi-step tasks; ensure best outputs
- **Peak performance**: Break separable tasks across multiple turns (one turn per task)

---

## Responses API

**Strong recommendation**: Use Responses API for GPT-5 agentic flows.

**Benefits**:
- Improved agentic flows
- Lower costs
- More efficient token usage
- Reasoning context persisted between tool calls

**Performance Gains**:
Example: Tau-Bench Retail score 73.9% → 78.2% by:
1. Switching to Responses API
2. Including `previous_response_id` to pass back previous reasoning

**Why**: Model refers to previous reasoning traces, conserves CoT tokens, eliminates need to reconstruct plan after each tool call.

---

## Coding Best Practices

GPT-5 leads all frontier models in coding: bug fixes, large diffs, multi-file refactors, new features, full apps.

### Frontend Stack (Recommended)
- **Frameworks**: Next.js (TypeScript), React, HTML
- **Styling/UI**: Tailwind CSS, shadcn/ui, Radix Themes
- **Icons**: Material Symbols, Heroicons, Lucide
- **Animation**: Motion
- **Fonts**: San Serif, Inter, Geist, Mona Sans, IBM Plex Sans, Manrope

### Zero-to-One App Generation

Use self-reflection for quality:

```xml
<self_reflection>
- First, spend time thinking of rubric until confident
- Think deeply about every aspect of world-class one-shot web app
- Create rubric with 5-7 categories (critical, but don't show user - for your purposes only)
- Use rubric to internally think and iterate on best possible solution
- Remember: if not hitting top marks across all categories, start again
</self_reflection>
```

### Matching Codebase Design Standards

```xml
<code_editing_rules>
<guiding_principles>
- Clarity and Reuse: Every component modular and reusable. Avoid duplication.
- Consistency: Adhere to design system—color tokens, typography, spacing unified
- Simplicity: Small, focused components. Avoid unnecessary complexity
- Demo-Oriented: Structure allows quick prototyping
- Visual Quality: High visual quality bar (spacing, padding, hover states)
</guiding_principles>

<frontend_stack_defaults>
- Framework: Next.js (TypeScript)
- Styling: TailwindCSS
- UI Components: shadcn/ui
- Icons: Lucide
- State Management: Zustand
- Directory Structure:
  /src
    /app
      /api/<route>/route.ts
      /(pages)
    /components/
    /hooks/
    /lib/
    /stores/
    /types/
    /styles/
</frontend_stack_defaults>

<ui_ux_best_practices>
- Visual Hierarchy: Limit typography to 4–5 font sizes and weights
- Color Usage: Use 1 neutral base (e.g., zinc) and up to 2 accent colors
- Spacing and Layout: Always use multiples of 4 for padding and margins
- State Handling: Use skeleton placeholders or animate-pulse for loading
- Accessibility: Use semantic HTML and ARIA roles
</ui_ux_best_practices>
</code_editing_rules>
```

---

## Verbosity Control

GPT-5 `verbosity` API parameter influences final answer length (not thinking length).

### Natural Language Override
While API parameter sets global default, GPT-5 responds to natural-language overrides for specific contexts:

**Example** (from Cursor):
```
Set verbosity=low globally

For code tools only:
"Write code for clarity first. Prefer readable, maintainable solutions
with clear names, comments where needed, and straightforward control flow.
Use high verbosity for writing code and code tools."
```

**Result**: Concise status updates + readable code diffs

---

## Instruction Following

GPT-5 follows instructions with **surgical precision** - enables flexibility but requires careful prompt construction.

### Contradictory Instructions Are Damaging

Poorly-constructed prompts with contradictory/vague instructions harm GPT-5 more than other models.

**Why**: Model expends reasoning tokens searching for way to reconcile contradictions.

**Bad Example**:
```
❌ "Never schedule appointment without explicit patient consent recorded in chart"
❌ "For high-acuity cases, auto-assign earliest same-day slot without contacting patient"

These directly conflict!
```

**Fix**: Review prompts for internal consistency. Remove contradictions.

### Prompt Tuning Example (Cursor)

**Original** (too general for GPT-5):
```xml
<maximize_context_understanding>
Be THOROUGH when gathering information. Make sure you have FULL picture
before replying. Use additional tool calls or clarifying questions as needed.
</maximize_context_understanding>
```

**Problem**: Caused excessive tool usage on small tasks.

**Refined**:
```xml
<context_understanding>
If you've performed edit that may partially fulfill USER's query,
but you're not confident, gather more information or use more tools before ending turn.
Bias towards not asking user for help if you can find answer yourself.
</context_understanding>
```

**Result**: Better decisions about when to use tools vs internal knowledge.

---

## Steering Best Practices

GPT-5 is extraordinarily steerable - responds well to:
- Verbosity control (API param + natural language)
- Tone adjustments
- Tool calling behavior
- User-defined custom rules/instructions

### Structured Specs
Using structured XML specs like `<[instruction]_spec>` improves instruction adherence:

```xml
<tool_use_spec>...</tool_use_spec>
<context_understanding>...</context_understanding>
<output_format_spec>...</output_format_spec>
```

Allows clear referencing of previous categories elsewhere in prompt.

---

## Model Parameters Summary

| Parameter | Purpose | Values |
|-----------|---------|--------|
| `reasoning_effort` | How hard model thinks | low, medium (default), high |
| `verbosity` | Final answer length | low, medium (default), high |
| `previous_response_id` | Reuse reasoning context | Response ID from previous call |

---

## Common Pitfalls

| Issue | Problem | Fix |
|-------|---------|-----|
| **Contradictory Instructions** | Internal conflicts in prompt | Review for consistency; remove contradictions |
| **Over-Restricting Autonomy** | Too many limitations on capable model | Start permissive, add constraints only when needed |
| **Ignoring Responses API** | Missing 5-10% performance gains | Use Responses API with `previous_response_id` |
| **Global Verbosity Everywhere** | Same verbosity for code, summaries, etc. | Set global default, override with natural language for specific contexts |

---

## Key Insights

> "GPT-5 responds well to direct and explicit instruction. Structured, scoped prompts yield most reliable results."

> "The model's creativity in approaching problems may exceed a human's ability to prescribe optimal thinking process."

> "Poorly-constructed prompts containing contradictory or vague instructions can be more damaging to GPT-5 than to other models."

---

## Further Reading

### Official Documentation
- [GPT-5 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide)
- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Responses API Documentation](https://platform.openai.com/docs/api-reference/responses)

### Production Examples
- [Cursor's GPT-5 Integration](https://cursor.com/blog/gpt-5) - Real-world prompt tuning

### General Patterns
- [Model-Agnostic Guidelines](PROMPT-ENGINEERING-GUIDELINES.md)
