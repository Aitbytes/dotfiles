---
name: html-slides
description: Produce polished scroll-based HTML slide presentations from research using Tailwind CSS. Fixed sidebar index, full-height slides, PDF-like scrolling.
---

## What I do

Create visually stunning HTML slide presentations that scroll like a PDF. Each slide is full viewport height with a fixed sidebar index on the left for navigation.

## When to use me

When you want a presentation that:

- Scrolls like a PDF opened in a browser
- Has a fixed index sidebar for quick navigation
- Looks polished and professional for sharing/pitching

## Requirements

- Tailwind CDN (automatic via cdn.tailwindcss.com)
- Inter font from Google Fonts
- No build step needed — pure HTML/CSS

## Template

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Presentation Title</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
      rel="stylesheet"
    />
    <style>
      body {
        font-family: "Inter", system-ui, sans-serif;
      }
      html {
        scroll-behavior: smooth;
      }
      .slide {
        min-height: 100vh;
      }
    </style>
  </head>
  <body class="bg-slate-900 text-white">
    <!-- Index Sidebar -->
    <nav
      class="fixed left-0 top-0 h-full w-56 bg-slate-950/90 border-r border-slate-800 p-4 z-50 backdrop-blur"
    >
      <div
        class="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-4"
      >
        Contents
      </div>
      <ul class="space-y-1">
        <li>
          <a
            href="#slide-1"
            class="block px-3 py-2 rounded-lg text-sm text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >1. Title</a
          >
        </li>
        <li>
          <a
            href="#slide-2"
            class="block px-3 py-2 rounded-lg text-sm text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >2. Context</a
          >
        </li>
        <li>
          <a
            href="#slide-3"
            class="block px-3 py-2 rounded-lg text-sm text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >3. Findings</a
          >
        </li>
        <li>
          <a
            href="#slide-4"
            class="block px-3 py-2 rounded-lg text-sm text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >4. Impact</a
          >
        </li>
        <li>
          <a
            href="#slide-5"
            class="block px-3 py-2 rounded-lg text-sm text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >5. Takeaway</a
          >
        </li>
      </ul>
    </nav>

    <!-- Main Content -->
    <main class="ml-56">
      <!-- Slide 1: Title -->
      <section
        id="slide-1"
        class="slide flex flex-col items-center justify-center text-center px-8 py-32"
      >
        <div class="max-w-3xl">
          <div
            class="inline-block px-4 py-1.5 bg-blue-500/20 text-blue-400 rounded-full text-sm font-medium mb-6"
          >
            TAGLINE
          </div>
          <h1
            class="text-6xl font-extrabold mb-4 bg-gradient-to-r from-white via-blue-200 to-blue-400 bg-clip-text text-transparent"
          >
            Title
          </h1>
          <p class="text-2xl text-slate-400">Subtitle</p>
        </div>
      </section>

      <!-- Slide 2: Content -->
      <section id="slide-2" class="slide px-8 py-32 border-t border-slate-800">
        <div class="max-w-4xl mx-auto">
          <h2 class="text-4xl font-bold mb-8">Section Title</h2>
          <!-- Content here -->
        </div>
      </section>

      <!-- Slide 3: Stats Cards -->
      <section id="slide-3" class="slide px-8 py-32 border-t border-slate-800">
        <div class="max-w-4xl mx-auto">
          <h2 class="text-4xl font-bold mb-8">Key Findings</h2>
          <div class="grid grid-cols-3 gap-6">
            <div
              class="bg-slate-800/50 border border-slate-700 rounded-2xl p-6"
            >
              <div class="text-4xl font-bold text-blue-400">Stat</div>
              <div class="text-slate-400">Label</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Slide 4: Takeaway -->
      <section id="slide-4" class="slide px-8 py-32 border-t border-slate-800">
        <div class="max-w-3xl mx-auto text-center">
          <h2 class="text-5xl font-bold mb-6">Key Takeaway</h2>
          <p class="text-xl text-slate-400 mb-8">Supporting text</p>
          <div class="grid grid-cols-3 gap-4">
            <div class="bg-slate-800/50 rounded-xl p-4">
              <div class="text-3xl font-bold text-blue-400">50%</div>
              <div class="text-sm text-slate-400">Metric 1</div>
            </div>
            <div class="bg-slate-800/50 rounded-xl p-4">
              <div class="text-3xl font-bold text-green-400">10x</div>
              <div class="text-sm text-slate-400">Metric 2</div>
            </div>
            <div class="bg-slate-800/50 rounded-xl p-4">
              <div class="text-3xl font-bold text-purple-400">100%</div>
              <div class="text-sm text-slate-400">Metric 3</div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </body>
</html>
```

## Design Patterns

- **Dark theme**: `bg-slate-900`, white text
- **Accent colors**: blue (`text-blue-400`), green, purple for highlights
- **Stats**: Large numbers with color, small labels
- **Cards**: Rounded corners (`rounded-2xl`), subtle borders
- **Gradients**: For emphasis on titles
- **Fixed sidebar**: `w-56`, stays visible
- **Each slide**: `min-height: 100vh`, full-page

## Writing Slides

1. Create a new `.html` file in `output/`
2. Use the template above as a base
3. Fill in 4-5 slides of research content
4. Update sidebar links to match your sections

## Output

Write `output/<topic>-slides.html` as a tool result so the user can open it directly in a browser.
