# Claude-Specific Prompt Engineering Guidelines

Claude 4.5+ specific behaviors, optimizations, and patterns.

**See Also**: [General Guidelines](PROMPT-ENGINEERING-GUIDELINES.md) - Model-agnostic core patterns

**Last Updated**: 2025-11-14

---

## Format Preference

### XML vs Markdown
Claude is specifically tuned for XML tags - prefer XML over Markdown:

```xml
<system_context>Role and identity</system_context>
<instructions>What to do</instructions>
<examples>Canonical demonstrations</examples>
```

**Why**: Research shows up to 40% performance improvement. Claude's training emphasized XML structure.

**Override when**: Cross-model compatibility required, team strongly prefers Markdown.

---

## Claude 4.5 Behaviors

### Action vs Suggestion
Claude 4.5 follows instructions with **surgical precision** - be directive:

**For action** (Claude implements):
```
Change this function to improve performance
Implement the user registration feature
```

**For suggestions only**:
```
Can you suggest improvements?
What changes would you recommend?
```

### Default to Action Pattern
Add to system prompt for proactive behavior:

```xml
<default_to_action>
By default, implement changes rather than suggesting.
When intent unclear, infer most useful action and proceed.
Use tools to discover missing details instead of asking.
Try to infer whether a tool call (file edit, read) is intended and act accordingly.
</default_to_action>
```

### Conservative Action Pattern
For less proactive behavior:

```xml
<do_not_act_before_instructions>
Do not jump into implementation or change files unless clearly instructed.
When intent is ambiguous, default to information, research, and recommendations.
Only proceed with edits when explicitly requested.
</do_not_act_before_instructions>
```

---

## Context Awareness

**See [General Guidelines > Context Management](PROMPT-ENGINEERING-GUIDELINES.md#context-management) for full strategy.**

### Claude-Specific Behavior
Claude 4.5 tracks remaining context window ("token budget") throughout conversations.

**Natural wrapping**: Without guidance, Claude may wrap up work as it approaches context limit.

**Override for long tasks**:
```markdown
Your context will be compacted as needed, allowing indefinite work.
Never stop tasks early due to token concerns.
Save progress to memory before context refresh.
Complete tasks fully regardless of remaining context.
```

---

## State Management for Long Tasks

**See [General Guidelines > Context Management > State Management](PROMPT-ENGINEERING-GUIDELINES.md#state-management) for general approach.**

### Claude-Specific Strengths
Claude 4.5 excels at long-horizon reasoning with exceptional state tracking.

### Multi-Context Window Tasks

**First Window: Framework Setup**
```markdown
Use first context to establish foundation:
- Write tests in structured format (tests.json)
- Create setup scripts (init.sh for servers, tests, linters)
- Initialize state tracking files
```

**Future Windows: Iterate on Todo List**
```markdown
Subsequent windows focus on execution:
- Review progress from state files
- Continue from todo list
- Maintain test discipline
```

**Quality of Life Tools**
```bash
# init.sh example
#!/bin/bash
npm install && npm run lint && npm test
```

**Why**: Prevents repeated setup when continuing from fresh context.

**Test Discipline**
```markdown
Create tests before starting work, track in structured format.
Remind: "Unacceptable to remove/edit tests - could lead to missing functionality."
```

**Starting Fresh vs Compaction**
Claude 4.5 discovers state from filesystem excellently:
```markdown
When starting fresh context:
- Call pwd; only read/write files in this directory
- Review progress.txt, tests.json, git logs
- Manually run fundamental integration test before new features
```

**Encourage Full Context Usage**
```markdown
This is a very long task, so plan your work clearly.
Spend your entire output context working on the task.
Don't run out of context with significant uncommitted work.
Continue working systematically until you complete this task.
```

---

## Communication Style

Claude 4.5 has more concise, natural communication style:

**Characteristics**:
- **More direct**: Fact-based progress reports, not self-celebratory
- **More conversational**: Fluent, colloquial, less machine-like
- **Less verbose**: May skip detailed summaries for efficiency

**Balance verbosity** if you want updates:
```markdown
After completing a task with tool use, provide a quick summary of work done.
```

---

## Extended Thinking

### When to Use
- Complex, multi-step reasoning
- Deep problem analysis
- Tasks requiring exploration of multiple approaches

### Thinking Budget
- **Minimum**: 1024 tokens
- **Recommended**: Start at minimum, increase incrementally
- **High budgets** (>32K): Use batch processing to avoid timeouts

### Prompting
**Start with general instructions**:
```markdown
Think thoroughly and in great detail about this problem.
Consider multiple approaches, show complete reasoning.
Try different methods if first approach doesn't work.
```

**Why**: Claude's creativity may exceed human's ability to prescribe optimal thinking process.

**Add specifics only if needed** based on thinking output.

### Multishot Pattern
Include examples using `<thinking>` or `<scratchpad>` tags:

```markdown
Problem 1: What is 15% of 80?

<thinking>
To find 15% of 80:
1. Convert 15% to decimal: 0.15
2. Multiply: 0.15 × 80 = 12
</thinking>

Answer: 12

Now solve: What is 35% of 240?
```

Claude generalizes the pattern.

### Self-Reflection for Quality
```markdown
Write factorial function.
Before finishing, verify with test cases for n=0, n=1, n=5, n=10 and fix issues.
```

---

## Memory Tool

Claude has Memory tool (public beta) for persistent cross-session state:

```markdown
Throughout execution:
- Store knowledge outside context window using Memory tool
- Consult memory across sessions
- Build knowledge bases over time
```

**Benefits**: Cross-session persistence, historical learning, not just retrieval (RAG).

---

## Model Selection

| Model | Use When | Cost | Speed |
|-------|----------|------|-------|
| **Haiku 4** | Simple tasks; clear logic; utilities; orchestrators | Lowest | Fastest |
| **Sonnet 4.5** | Complex reasoning; multi-phase workflows; analysis | Medium | Medium |
| **Opus 4** | Very complex tasks; critical architectural decisions | Highest | Slowest |

---

## Performance Optimization

### Examples Are Critical
Claude 4.5+ pays **close attention** to example details:
- Curate diverse, canonical examples (not exhaustive edge cases)
- Examples show pattern, not every variation
- 2-3 well-chosen examples > 10 generic ones

### Context & Motivation
Explain WHY behaviors matter:

❌ Less effective: `NEVER use ellipses`

✅ More effective: `Your response will be read by text-to-speech. Never use ellipses since TTS engines can't pronounce them properly.`

Claude generalizes from explanations.

### Incremental Progress
Claude 4.5 focuses on "making steady advances on a few things at a time rather than attempting everything at once."

**Prompt for this**:
```markdown
Focus on incremental progress:
- Complete a few components thoroughly before moving on
- Don't attempt everything simultaneously
- Make steady, measurable advances
```

---

## Common Pitfalls

| Issue | Problem | Fix |
|-------|---------|-----|
| **Assumed Proactivity** | Expecting action from "suggest changes" | Be explicit: "Change this" vs "Can you suggest?" |
| **Not Leveraging Context Awareness** | Stopping tasks early, poor context transitions | Tell Claude about compaction, use Memory tool |
| **Missing State Management** | Losing progress across contexts | JSON for structure, text for notes, git for checkpoints |
| **Over-Prescriptive Thinking** | Restricting reasoning with rigid steps | Start high-level goals, add specifics only if needed |

---

## Key Insights

> "Claude 4.5 models excel at long-horizon reasoning with exceptional state tracking, making steady advances on a few things at a time."

> "Context engineering is the art and science of curating what will go into the limited context window."

> "Claude is smart enough to generalize from explanations."

---

## Further Reading

### Official Documentation
- [Claude 4 Best Practices](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Extended Thinking Tips](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips)
- [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Building Effective Agents](https://docs.anthropic.com/en/docs/agents-and-tools/building-effective-agents)

### General Patterns
- [Model-Agnostic Guidelines](PROMPT-ENGINEERING-GUIDELINES.md)
