---
description: Conducts deep UI concept design research and creates innovative showcase prototypes with cutting-edge design approaches
argument-hint: [UI Concept Design Instructions, Direction and/or Theme] [Number of unique concepts to create (default: 5)]
---

# 🎨 UI Concept Design Research & Showcase Creation
Conduct deep UI concept design research and creates _`COUNT`_ innovative showcase prototypes with cutting-edge design approaches.


## Inputs

_UI Concept Design Instructions, Direction and/or Theme_:
THEME=$1

_Number of unique concepts to create_:
COUNT=$2 (defaults to 5 if not provided, max recommended: 10)


## Instructions

- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section in CLAUDE.md before starting work, including but not limited to:
  - **Foundational Rules and Guardrails**
  - **Foundational Development Guidelines and Standards** (e.g. Development, Architecture, UI/UX Guidelines etc.)
- **Design system only** - No wireframes or page layouts (use `create-wireframes` command for that)
- **Pragmatic approach** - Only create what's needed, avoid over-engineering
- **Delegate to sub-agents** for research and showcase creation
- Before beginning, **think hard** and engage in deep creative thinking about:
  - Emerging design paradigms beyond conventional patterns
  - Cross-industry design inspiration (gaming, film, architecture, fashion)
  - Emotional design principles and psychological impact
  - Future-forward interaction models (spatial, gestural, voice-hybrid)
  - Cultural and artistic movements that could inform UI design


## Execution Model

**Use foreground parallel agents (`run_in_background=false`)** - launch multiple Task tool calls in a single message to run agents concurrently.

**How it works:**
1. **Launch multiple agents in one message** - all Task calls in same response run in parallel
2. **Wait for all to complete** - conversation blocks until entire batch finishes
3. **Results return together** - process all results, then proceed to next phase

**Example workflow:**
```
1. Launch 3 research agents in parallel (one message, 3 Task calls)
2. Wait for all 3 to complete → results return together
3. Synthesize research, select themes
4. Launch 5 showcase agents in parallel (one message, 5 Task calls)
5. Wait for all 5 to complete → results return together
6. Proceed to Hybrid Fusion, then QA
```

**Batching Strategy** (for COUNT > 5):
- Launch first batch of up to 5 agents in parallel
- Wait for batch to complete
- Launch next batch
- Repeat until all showcases created


## PHASE 1: 🔬 Deep Design Research & Exploration

### 1.1 Research Execution (Parallel Agents)
Launch all research agents in parallel (multiple Task calls in one message):

**`cc-workflows:ui-ux-designer`**:
- Research cutting-edge UI design trends for 2025 and beyond
- Explore diverse design languages and movements (see suggested directions below for inspiration)
- Investigate micro-interaction patterns from leading design systems (Material 3, Fluent 2, iOS 18+)
- Study motion design principles from animation studios (Disney's 12 principles adapted to UI)
- Research accessibility-first design patterns
- Analyze the user's specific requirements and context from arguments

**`cc-workflows:ui-ux-designer`**:
- Analyze design psychology and emotional response patterns
- Study color theory evolution and modern palette approaches
- Investigate typography trends: Variable fonts, kinetic type, responsive typography
- Explore spatial design concepts: Depth, layering, z-axis interactions
- Research haptic and sensory feedback integration

**`cc-workflows:whimsy-injector`**:
- Discover unexpected design inspirations from nature (biomimicry)
- Find delightful micro-interactions from gaming interfaces
- Explore generative and procedural design patterns
- Investigate particle systems and physics-based animations
- Research easter eggs and surprise-delight moments

### 1.2 Synthesis & Implementation Plan
Create comprehensive documentation at _`<project_root>/docs/temp/ui-research/concept-research-report.md`_ containing:
- **User Requirements Analysis**: Interpretation of provided arguments and context
- **Design Opportunity Spaces**: Multiple potential directions discovered through research
- **Design Philosophy Options**: Various core principles and visions to explore
- **Visual Language Palette**: Range of typography, color, spacing approaches
- **Interaction Model Spectrum**: Different gesture, transition, feedback possibilities
- **Innovation Territories**: Novel approaches and unexplored areas
- **Technical Strategy Options**: Various CSS techniques and performance approaches
- **Accessibility Framework**: WCAG compliance with creative solutions

### 1.3 Asset Creation
Generate and download supporting assets:
- Mood boards and inspiration collages
- Color palette explorations
- Typography specimens
- Motion design references
- Store all assets in _`<project_root>/docs/temp/ui-research/assets/`_

## PHASE 2: 🚀 Showcase Creation (_`COUNT`_ Unique Concepts)

### 2.1 Theme Selection & Assignment
**Based on Phase 1 research and user requirements**, select _`COUNT`_ distinct design directions that:
- Address different aspects of the user's needs
- Explore diverse aesthetic territories
- Push different technical boundaries
- Avoid any overlap or redundancy

#### Design Direction
If the user provided a specific theme or direction in the arguments, the primarily create variants around that theme, ensuring each is unique in approach and execution. Otherwise, select from the following pool or discover new ones:

**Design Direction Pool** (select from these or discover new ones based on research):
- **Neo-Brutalist**: Raw concrete aesthetics, bold typography, harsh contrasts
- **Organic/Biomimetic**: Nature-inspired curves, growth patterns, living interfaces
- **Retro-Futurism**: 80s cyberpunk, CRT effects, neon aesthetics
- **Glassmorphism**: Translucent layers, backdrop filters, depth
- **Kinetic Typography**: Text-driven interfaces, animated type systems
- **Physics-Based**: Realistic behaviors, gravity, particle systems
- **Ambient/Adaptive**: Context-aware, breathing, responsive to environment
- **Maximalist**: Bold patterns, information density, visual celebration
- **Zen Minimalism**: Extreme reduction, perfect balance, single accents
- **Liquid/Fluid**: Water-like transitions, morphing shapes, flow states
- **Geometric Precision**: Mathematical beauty, sacred geometry, grid systems
- **Nostalgic/Vaporwave**: 90s web revival, gradient meshes, retro computing
- **Dark Mode First**: OLED optimization, high contrast, neon accents
- **Accessibility-First**: High contrast, clear navigation, assistive features
- **3D/Spatial**: Depth, perspective, spatial navigation
- **Generative/Procedural**: Algorithm-driven layouts, unique each visit
- **Emotional Design**: Mood-responsive, empathetic interfaces
- **Bauhaus Revival**: Form follows function, primary colors, geometric shapes

**Document the selected _`COUNT`_ themes** in _`<project_root>/docs/temp/ui-research/selected-themes.md`_ with rationale for each choice.

### 2.2 Showcase Development (Parallel Agents)
Launch showcase agents in parallel using multiple Task calls in a single message.

**Batching Rules:**
- **COUNT ≤ 5**: Launch all agents in parallel (one message with all Task calls)
- **COUNT > 5**: Launch in batches of 5, wait for batch to complete, then launch next batch

**For each showcase agent (`cc-workflows:ui-ux-designer`)**, provide:
1. **Their assigned design direction** from the selection phase
2. **The research findings** from Phase 1 (summarized)
3. **User requirements** from the arguments
4. **Mission**: Create a fully realized showcase in their assigned style

**Agent Instructions**:
- Each agent focuses exclusively on their assigned theme
- Interpret the theme through the lens of user requirements
- Push the boundaries of their specific design direction
- Ensure technical excellence and usability within their aesthetic

### 2.3 Hybrid Fusion Showcase
**After all _`COUNT`_ showcases complete**, launch a final agent:

**v`COUNT+1`: Hybrid Fusion**
- Review all _`COUNT`_ completed showcases
- Extract the most innovative elements from each
- Combine into ultimate synthesis concept
- Create the "best of all worlds" showcase

### 2.4 Showcase Requirements
Each showcase must include:

#### Structure
```
<project_root>/docs/temp/ui-concepts/vXX/
├── index.html          # Main showcase page
├── page2.html         # Secondary demonstration (if needed)
├── page3.html         # Tertiary demonstration (if needed)
├── styles.css         # Core styling
├── animations.css     # Animation definitions
├── interactions.js    # Interactive behaviors
└── README.md         # Concept explanation
```

#### Technical Implementation
**HTML Structure**:
- Semantic HTML5 with ARIA labels
- Progressive enhancement approach
- Component-based architecture

**CSS Excellence**:
```css
/* Modern CSS Features to Utilize */
- CSS Grid with subgrid
- Container queries
- :has() selector
- CSS nesting
- Cascade layers
- Custom properties with @property
- CSS math functions (clamp, min, max, calc)
- Scroll-driven animations
- View transitions API
```

**Animation & Motion**:
```css
/* Animation Techniques */
- Spring physics (cubic-bezier)
- Stagger animations
- Morphing transitions
- Parallax scrolling
- Intersection Observer triggers
- FLIP animations
- GPU-accelerated transforms
```

**Interaction Patterns**:
```javascript
/* JavaScript Enhancements */
- Gesture recognition
- Drag and drop with inertia
- Magnetic hover effects
- Sound feedback integration
- Keyboard navigation
- Touch-friendly interactions
- Haptic feedback triggers
```

### 2.5 Quality Criteria

**Visual Excellence**:
- Professional typography with font pairing
- Sophisticated color harmony
- Consistent spacing using modular scale
- Thoughtful use of negative space
- High-contrast accessibility modes

**State Design**:
- Idle, hover, focus, active, disabled, loading, error, success
- Smooth state transitions (300-400ms sweet spot)
- Clear affordances and feedback
- Progressive disclosure patterns

**Performance**:
- CSS containment for render optimization
- Will-change hints for animations
- RequestAnimationFrame for smooth JS
- Lazy loading for images/content
- Critical CSS inlining

**Responsive Behavior**:
- Mobile-first approach
- Fluid typography (clamp functions)
- Flexible grids with minmax()
- Touch target optimization (44px minimum)
- Orientation awareness

## PHASE 3: 🎯 Quality Assurance & Refinement

### 3.1 Design Review Protocol
After creating showcases (including Hybrid Fusion), conduct review:

**Launch `cc-workflows:ui-ux-designer`** to:
- Critique each showcase's design decisions
- Identify improvement opportunities
- Suggest refinements for visual hierarchy
- Evaluate emotional impact and user delight

**Launch `cc-workflows:qa-test-engineer`** to:
- Test responsive behavior across viewports
- Verify keyboard navigation
- Check accessibility compliance
- Validate performance metrics

### 3.2 Refinement Iteration
Based on review feedback:
- Enhance weak areas in each showcase
- Add missing micro-interactions
- Optimize animation performance
- Polish edge cases and transitions

### 3.3 Gallery Creation
Create gallery/showcase page _`<project_root>/docs/temp/ui-concepts/gallery.html`_ containing:
- Grid-based card layout linking to all showcases
- Brief design rationale for each concept
- Technical highlights for each variation
- Visual preview (iframe or screenshot) of each concept

### 3.4 Summary Report
Provide the user with:
- Location of all created files
- Brief description of each concept variation
- Recommendation for which concept(s) best match the brief
- How to view the concepts (e.g., `open docs/temp/ui-concepts/gallery.html`)



## EXECUTION NOTES

**Agent Management:**
- Use **foreground parallel agents (`run_in_background=false`)** - multiple Task calls in one message run concurrently
- Results return together when all agents in the batch complete
- For COUNT > 5: batch into groups of 5, wait for each batch before launching next
- Each phase completes fully before proceeding to the next

**Design Independence:**
- Each showcase agent works in isolation
- No design influence between showcases (they don't see each other's work)
- Each explores its assigned direction independently

**Quality Standards:**
- Each showcase should push boundaries while remaining usable
- Balance creativity with technical feasibility
- Ensure code is clean and maintainable
- Complete all _`COUNT`_ prototypes before finishing

**Creative Inspiration Sources**:
- Awwwards, CSS Design Awards, FWA
- Dribbble, Behance, Muzli
- CodePen, Codrops, CSS-Tricks
- Design systems: IBM Carbon, Atlassian, Shopify Polaris
- Gaming UIs: Cyberpunk 2077, Destiny 2, Overwatch
- Film UIs: Minority Report, Iron Man, Tron

**Remember**: This is about exploring design possibilities. Be bold, be creative, but also be responsive - keep the user informed of progress throughout.
