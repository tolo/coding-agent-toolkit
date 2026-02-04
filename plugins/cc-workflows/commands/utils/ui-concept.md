---
description: Creates innovative UI concept showcases exploring a design direction/theme
argument-hint: <design-direction/theme> [count (default: 3)]
---

# UI Concept Design Exploration

Create _`COUNT`_ unique UI concept showcases exploring variations of the given design direction/theme.


## Inputs

**DIRECTION** = $1 - The design direction, theme, or aesthetic to explore.

**COUNT** = $2 _(default: 3, max: 8)_ - Number of unique concept variations to create


## Pre-Execution: Direction Selection

If DIRECTION is empty or unclear, use **AskUserQuestion** to prompt the user:

**Question**: "What design direction should we explore?"
**Header**: "Direction"
**multiSelect**: true
**Options** (select diverse set from):
- **Neo-Brutalist** - Raw concrete aesthetics, bold typography, harsh contrasts
- **Glassmorphism** - Translucent layers, frosted glass, depth and blur
- **Organic/Biomimetic** - Nature-inspired curves, growth patterns, living interfaces
- **Retro-Futurism** - 80s cyberpunk, CRT effects, neon aesthetics
- **Zen Minimalism** - Extreme reduction, perfect balance, whitespace
- **Maximalist** - Bold patterns, information density, visual celebration
- **Dark Mode OLED** - True blacks, high contrast, neon accents
- **Kinetic Typography** - Text-driven interfaces, animated type systems
- **Liquid/Fluid** - Water-like transitions, morphing shapes, flow states
- **Geometric Precision** - Mathematical beauty, grids, sacred geometry
- **Nostalgic/Vaporwave** - 90s web revival, gradient meshes, retro computing
- **3D/Spatial** - Depth, perspective, spatial navigation
- **Warm & Approachable** - Soft colors, rounded corners, friendly feel
- **Editorial/Magazine** - Typography-forward, sophisticated layouts

Combine user selections into the DIRECTION for research and showcase creation.


## Execution

### Phase 1: Research (Parallel)

Launch 2 research agents in parallel:

**Agent 1 (`cc-workflows:ui-ux-designer`)**: Research the specified direction
- Current trends and best examples of this aesthetic
- Color palettes, typography, and spacing patterns
- Key visual elements and characteristics
- Successful implementations to reference

**Agent 2 (`cc-workflows:whimsy-injector`)**: Find creative angles
- Unexpected twists on the direction
- Delightful micro-interactions fitting the aesthetic
- Cross-domain inspiration (gaming, film, architecture)
- Ways to make each variation distinctive

### Phase 2: Showcase Creation (Parallel)

After research completes, define _`COUNT`_ unique variations of the direction. Each should explore a different interpretation or aspect.

**Launch showcase agents in parallel** (batch ≤5 at a time):

For each variation, use the **`frontend-design:frontend-design`** skill (if available) or **`cc-workflows:ui-ux-designer`** agent with:
- The specific variation/interpretation to implement
- Research findings as context
- Output location: `docs/temp/ui-concepts/v{N}/`

**Each showcase produces:**
```
docs/temp/ui-concepts/v{N}/
├── index.html      # Main showcase
├── styles.css      # Styling
└── README.md       # Brief concept explanation
```

### Phase 3: Gallery & Summary

After all showcases complete:

1. **Create gallery** at `docs/temp/ui-concepts/gallery.html`
   - Links to all showcases with brief descriptions
   - Visual preview of each concept

2. **Summarize results** for user:
   - List of created concepts with descriptions
   - Which variations best capture the direction
   - Command to view: `open docs/temp/ui-concepts/gallery.html`


## Notes

- **Use `frontend-design:frontend-design` skill** when available - it produces higher quality, more distinctive designs
- **Parallel execution**: Launch all research agents together, then all showcase agents together (in batches of 5)
- **Lean output**: Each showcase should be focused - one compelling page demonstrating the concept
- **No duplicate aesthetics**: Each variation must be visually distinct
