---
description: Creates simple HTML wireframes for all pages/screens from feature requirements (simple, no sub-agents)
argument-hint: [Feature requirements - inline, file path, or PRD reference] [Optional - design system or concept design directory]
---

# Create Wireframes (Simple)

Transform feature requirements into simple HTML wireframes that capture key layout and interaction patterns for all pages/screens.

**Platform-Agnostic**: HTML/CSS is used as the universal design language for ALL projects (web, mobile, desktop). Wireframes serve as the canonical design reference that will be adapted to platform-specific implementations later.


## Variables

REQUIREMENTS: $1 (feature requirements - inline description, file path, or PRD reference)
DESIGN_DIR: $2 (optional - design system directory or concept design inputs)
OUTPUT_DIR: ${3:-docs/wireframes}


## Instructions

- **Fully** read and understand the **Workflow Rules, Guardrails and Guidelines** section as defined in AGENTS.md, etc. before starting work, including but not limited to:
  - **Foundational Rules and Guardrails**
  - **Foundational Development Guidelines and Standards** (e.g. Development, Architecture, UI/UX Guidelines etc.)
- No sub-agents - direct sequential wireframe creation
- **Wireframes only** - No design system creation (use `create-design-system` command for that)
- **Simple, grayscale layouts** - Focus on structure, not visual polish
- **100% page coverage** - Every page/screen in requirements MUST have a wireframe
- **NEVER STOP until complete** - this is a continuous workflow from analysis through creation to validation
- **Auto-integrate feedback** - validation findings are immediately fixed, not waiting for approval
- **Self-correcting** - if issues are found during review, fix them and continue; only stop if fundamentally blocked


## Workflow

### Phase 1: Requirements Analysis

#### Validate Inputs
- Verify _`REQUIREMENTS`_ is provided - if not, **STOP** and ask user
- If _`DESIGN_DIR`_ provided, verify it exists and note available design assets

#### Create Page Inventory
**CRITICAL**: Extract comprehensive list of ALL pages/screens from _`REQUIREMENTS`_:
- Main pages (home, dashboard, settings, etc.)
- Sub-pages and detail views
- Modal/overlay states (if complex enough to warrant separate wireframe)
- Error/empty/loading states (if distinct layouts needed)

Document in _`OUTPUT_DIR/page-inventory.md`_:
```markdown
# Page Inventory

## Pages to Wireframe
1. [page-name] - [brief description]
2. [page-name] - [brief description]
...

## Total: [N] wireframes required
```

#### Identify Key Patterns
From requirements, note:
- **Navigation structure** (header, sidebar, tabs, etc.)
- **Key content blocks** and their hierarchy
- **Primary user actions** and CTA placement
- **Responsive requirements** (mobile/tablet/desktop)

**Gate**: Complete page inventory created, patterns identified


### Phase 2: Wireframe Creation

#### Wireframe Approach
Create basic, grayscale HTML layouts showing:
- **Major sections** and their placement
- **Key containers** (panels, cards, etc.)
- **Content blocks** with realistic proportions
- **Primary navigation** structure
- **Important CTAs** and hierarchy
- **Basic responsive behavior**

**Keep it simple**:
- Use boxes and placeholders
- Grayscale only - no colors
- Focus on layout, not details
- Show information hierarchy

#### Base Template
Use this template for all wireframes:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Page Name] - Wireframe</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: system-ui, sans-serif;
            line-height: 1.5;
            color: #333;
            background: #f5f5f5;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .box {
            background: white;
            border: 2px solid #ddd;
            padding: 20px;
            margin-bottom: 20px;
        }
        .placeholder {
            background: #e0e0e0;
            border: 2px dashed #999;
            padding: 40px;
            text-align: center;
            color: #666;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background: #666;
            color: white;
            text-decoration: none;
        }
        .btn-outline {
            background: white;
            color: #666;
            border: 2px solid #666;
        }
        .grid {
            display: grid;
            gap: 20px;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        }
        .flex { display: flex; gap: 20px; align-items: center; }
        @media (max-width: 768px) {
            .flex { flex-direction: column; }
        }
    </style>
</head>
<body>
    <!-- Page content here -->
</body>
</html>
```

#### Common Patterns

**Navigation:**
```html
<nav class="box">
    <div class="flex" style="justify-content: space-between;">
        <div class="placeholder" style="width: 120px; height: 40px;">LOGO</div>
        <div class="flex">
            <a href="#" class="btn btn-outline">Menu 1</a>
            <a href="#" class="btn btn-outline">Menu 2</a>
            <a href="#" class="btn">Sign Up</a>
        </div>
    </div>
</nav>
```

**Hero Section:**
```html
<section class="box">
    <div class="grid" style="grid-template-columns: 1fr 1fr;">
        <div>
            <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">Headline</h1>
            <p style="margin-bottom: 2rem; color: #666;">Description text</p>
            <a href="#" class="btn">Get Started</a>
        </div>
        <div class="placeholder" style="height: 300px;">IMAGE</div>
    </div>
</section>
```

**Content Grid:**
```html
<div class="grid">
    <div class="box">
        <div class="placeholder" style="height: 150px; margin-bottom: 10px;">IMG</div>
        <h3>Item Title</h3>
        <p>Brief description</p>
    </div>
    <!-- Repeat -->
</div>
```

#### Sequential Wireframe Creation
Create each wireframe from the page inventory:
1. Reference the page inventory list
2. Create each wireframe file sequentially
3. Use consistent navigation across all pages
4. **Naming convention**: `[page-name].html` (e.g., `home.html`, `dashboard.html`, `user-profile.html`)

#### Completeness Verification
After all wireframes created:
- Cross-check against Phase 1 inventory
- Verify EVERY page has corresponding wireframe
- No page skipped because "similar" to another

**Gate**: All pages from inventory have wireframes


### Phase 3: Validation & Auto-Refinement

#### Self-Review
Review all wireframes for:
- Responsive behavior across viewports
- Navigation consistency
- Layout proportions
- Information hierarchy
- Content organization
- User flow representation

#### Automatically Integrate Findings (DO NOT STOP - continue immediately)
- **Critical/High issues** (broken layouts, missing sections, navigation inconsistencies): Fix immediately in affected wireframe files
- **Medium/Low issues** (proportion tweaks, minor hierarchy adjustments): Fix inline during this phase
- If review identifies missing pages or states not in original inventory → create them now

**NO GATE - Continue immediately to Phase 4 after fixing all issues found**


### Phase 4: Documentation

#### Update Page Inventory
Mark all wireframes as complete in _`OUTPUT_DIR/page-inventory.md`_.

#### Create Index Page
Create _`OUTPUT_DIR/index.html`_ as navigation hub:
- Grid/list of all wireframes with thumbnails
- Brief description of each page
- Links to individual wireframe files

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wireframe Index</title>
    <style>
        body { font-family: system-ui; padding: 40px; background: #f5f5f5; }
        .grid { display: grid; gap: 20px; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }
        .card {
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
        }
        .card iframe { width: 100%; height: 200px; border: none; pointer-events: none; }
        .card-body { padding: 16px; }
        .card h3 { margin: 0 0 8px; }
        .card p { color: #666; margin: 0 0 12px; }
        .card a { color: #333; }
    </style>
</head>
<body>
    <h1>Wireframes</h1>
    <p style="color: #666; margin-bottom: 24px;">Total: [N] pages</p>
    <div class="grid">
        <!-- Card per wireframe -->
        <div class="card">
            <iframe src="[page].html"></iframe>
            <div class="card-body">
                <h3>[Page Name]</h3>
                <p>[Brief description]</p>
                <a href="[page].html">View wireframe &rarr;</a>
            </div>
        </div>
    </div>
</body>
</html>
```

**Gate**: Documentation complete


## Output

```
OUTPUT_DIR/
├── index.html              # Navigation hub for all wireframes
├── page-inventory.md       # Checklist of all pages
├── home.html              # Individual wireframes...
├── dashboard.html
├── [page-name].html
└── ...
```


## Quality Checklist

- [ ] **100% coverage**: Every page from requirements has a wireframe
- [ ] **No missing pages**: Cross-checked against inventory
- [ ] Layout hierarchy is clear
- [ ] Navigation is consistent across pages
- [ ] Responsive behavior works
- [ ] All wireframes use grayscale (no colors)
- [ ] Index page links to all wireframes
- [ ] Page inventory matches actual files


**Remember**: Wireframes focus on structure, not polish. Keep them simple, grayscale, and focused on layout patterns. Every page in the requirements must have a corresponding wireframe.
