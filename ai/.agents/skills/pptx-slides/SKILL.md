---
name: pptx-slides
description: Produce a professional PowerPoint (.pptx) slide deck from research findings using python-pptx. Includes a ready-to-run template script and widescreen 16:9 layout.
---

## What I do

Convert structured research findings into a polished PowerPoint slide deck with a professional 16:9 widescreen layout. Uses python-pptx for programmatic slide generation with consistent styling, bullet formatting, and section dividers.

## When to use me

When the user wants a `.pptx` file they can edit in PowerPoint, LibreOffice Impress, or Google Slides. Ideal for corporate presentations, stakeholder briefings, or deliverables that require a familiar office format.

## Requirements

- `uv run --with python-pptx` (python-pptx is not in nixpkgs, so use uv)
- Python 3.12+

## How to generate

### Step 1: Write a generator script

Create and run a Python script like this:

```bash
uv run --with python-pptx python3 - << 'EOF'
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

def add_title_slide(prs, title, subtitle_text):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = title
    sub_ph = slide.placeholders[1]
    sub_ph.text = subtitle_text
    return slide

def add_section_slide(prs, section_title):
    slide = prs.slides.add_slide(prs.slide_layouts[2])
    slide.shapes.title.text = section_title
    return slide

def add_bullet_slide(prs, title, bullets):
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title
    tf = slide.placeholders[1].text_frame
    for bullet in bullets:
        p = tf.add_paragraph()
        p.text = bullet
        p.level = 0
    return slide

# === BUILD SLIDES ===

add_title_slide(prs, "Research Title", "Subtitle / Date")

add_section_slide(prs, "Executive Summary")

add_bullet_slide(prs, "Key Findings", [
    "Finding 1 — [Source] — High confidence",
    "Finding 2 — [Source] — Medium confidence",
])

add_bullet_slide(prs, "Why It Matters", [
    "Implication 1",
    "Implication 2",
])

add_section_slide(prs, "Detailed Findings")

add_bullet_slide(prs, "Finding 1", [
    "Evidence: [citation]",
    "Confidence: High",
    "Key insight: ...",
])

add_bullet_slide(prs, "Finding 2", [
    "Evidence: [citation]",
    "Confidence: Medium",
    "Key insight: ...",
])

add_section_slide(prs, "Conclusions")

add_bullet_slide(prs, "Takeaways", [
    "Actionable recommendation 1",
    "Actionable recommendation 2",
])

add_bullet_slide(prs, "Open Questions", [
    "What remains unknown",
    "What needs further investigation",
])

add_bullet_slide(prs, "Thank You", [
    "Questions?",
    "Contact: ...",
])

prs.save("output/slides.pptx")
print("Saved: output/slides.pptx")
EOF
```

### Step 2: Create output directory and run

```bash
mkdir -p output && uv run --with python-pptx python3 - << 'SCRIPT'
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ... (paste the slide generation code from Step 1)
SCRIPT
```

## Slide type reference

| Slide type      | Use case                   | python-pptx approach |
| --------------- | -------------------------- | -------------------- |
| Title slide     | Deck title, subtitle, date | `slide_layouts[0]`   |
| Section divider | New section header         | `slide_layouts[2]`   |
| Bullet slide    | Content with bullets       | `slide_layouts[1]`   |
| Two-column      | Comparison or list + image | manual shapes        |

## Styling notes

- **Fonts**: Use Calibri or Arial (system defaults) — no need to embed fonts
- **Colors**: Blue title slides (`RGBColor(0, 51, 102)`), white content slides
- **Font sizes**: Title 44pt, bullets 24pt, sub-bullets 20pt
- **Section slides**: Use a dark background color for visual separation
- **Images**: Add via `slide.shapes.add_picture()` positioned with `Inches()`

## Output envelope

The skill produces `output/slides.pptx`. The agent should write this path as a tool result so the user can open it directly in their preferred presentation software.

## Limitations

- python-pptx does not support speaker notes via CLI; add notes programmatically if needed
- Complex layouts (merged cells, animated charts) are not supported — keep slides simple
- For templates with logos or master slides, provide the template `.pptx` as a base file and modify it instead of building from scratch
