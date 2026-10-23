---
name: frontend-style
description: Visual direction and frontend rules for this user's web projects - bold, non-generic design with hard bans (cards, badges, background orbs, emoji, lucide-style icon sets, overused fonts) and a concept-first process. Load for any UI design, frontend implementation or design review.
---

# Frontend style

The goal is interfaces that look **designed for this subject by a person with a point of view**, never like the median AI-generated site. Language models drift toward the statistically safest choices: Inter, a centered hero, a three-card feature grid, a purple gradient. Every rule below pushes away from that center.

This builds on Anthropic's `frontend-design` guidance. Where the two differ, **this file wins.**

## Hard bans (the user's brief)

- **Card-based layouts.** No grids of rounded, shadowed boxes as the main way to organize content: feature cards, testimonial cards, pricing cards, card-in-card. Structure content with typography, rules, columns, whitespace, numbering, tables, bands, overlap and scale.
- **Badges and pills** as decoration: "New", "Popular", "Beta" chips, status pills used for flavor, rounded tag clouds. A real filter control may look like a control.
- **Background orbs and blobs**: blurred colored circles, glowing spheres, lava-lamp shapes behind the content.
- **Emoji** anywhere in the UI or the copy. This includes pictographic symbols used as icons (✨ ✓ ★ →) in place of real typography or SVG.
- **Lucide**, and stock outline icon sets that look the same: heroicons, tabler, feather, react-icons. By default, use **no icons**. Typography, numbering and labels carry the meaning. If an icon really earns its place, draw a small custom SVG set in the project's own visual language.
- **Overused fonts**: Inter, Roboto, Open Sans, Lato, Arial, Montserrat, Poppins, Geist, Space Grotesk, and system-ui as the primary face. A system stack is fine as the *fallback* after a real typeface.

`scripts/anti_slop.py` (run by `make check`) enforces what static analysis can catch. Errors must be fixed. Warnings go to the design critic. A line marked `anti-slop: allow <reason>` needs a real reason, which the reviewer checks.

## Gradients: allowed, following Claude's guidance

Gradients and atmospheric backgrounds are allowed when they create **depth and atmosphere that fit the chosen direction**: layered radial washes, a light source, paper or film grain, gradient meshes tied to the palette, geometric patterns. They must never be:
- the purple/indigo/violet → pink or blue SaaS gradient (the checker blocks it);
- gradient-filled headline text as the hero trick;
- the only idea on the page, or a substitute for a layout concept;
- an orb in disguise (see the bans above).

## Be bold

- **Commit to one extreme direction** and push it: brutalist, Swiss/International, editorial magazine, constructivist poster, retro print, industrial, cartographic, luxury-minimal, toy-like, and so on. See [references/directions.md](references/directions.md) for seeds, not templates. Mixing two halves of two styles produces mush.
- **Typography is the main visual element.** Use extreme contrast: weights 100–200 against 800–900, size jumps of 3× or more, display type set big enough to be a layout element. Use one distinctive family used decisively, or two that are clearly different, such as a display face with a mono or a serif with a grotesque.
- **Color**: one dominant color with sharp accents. Avoid evenly spread, timid palettes. Draw on the subject's world (signage, packaging, instruments, print, IDE themes), not on "tech blue".
- **Layout**: asymmetry, a visible grid that is sometimes broken on purpose, overlap, very large numerals, full-bleed bands, sticky or rotated elements. Avoid the default stack of a centered hero, three columns, logos, testimonials and a CTA.
- **Motion**: one orchestrated moment, such as a staggered page-load reveal or a scroll-linked change, rather than a sprinkle of hover effects. Motion that responds to the user (opening, confirming) is fine. Respect `prefers-reduced-motion`.

The full catalog of AI-look tells to avoid is in [references/anti-patterns.md](references/anti-patterns.md).

## Process (designer and frontend-dev)

1. **Subject first.** What world does this product live in? Who uses it, where, and in what mood? What does that world look like? Its vernacular materials, printed matter, signage and instruments are the raw material.
2. **Direction.** Name it in 2–4 words and state the one bold idea in a sentence.
3. **Token plan before any code**: 4–6 named colors with hex values and roles; type roles (display, text, mono, small) with family, weights and a scale; spacing scale; radius (often 0); one motion principle; layout rules with ASCII wireframes of the key screens.
4. **Self-review the plan** against the brief and this file. For every choice, ask: "Is this the first thing any model would pick?" If yes, change it.
5. **Build.** Use CSS custom properties for every token. Load fonts properly: `font-display: swap`, preload the display face, subset when you can.
6. **Critique.** Screenshot at 375, 768 and 1440 px and compare against the plan. **Remove one element** before you call it done.

## Fonts

- Choose per project and **justify** the choice in `docs/design.md`: why this face fits this subject.
- Avoid repeating yourself across projects. Read the registry at `${CLAUDE_PLUGIN_DATA}/font-registry.md`, which may not exist yet. Do not reuse a pairing already listed there. When the user approves a design, append a line: `YYYY-MM-DD · <project> · <display> + <text>`.
- Good sources: less common Google Fonts families, Velvetyne, Collletttivo, Open Foundry, and other OFL foundries. Fontshare is fine, but its most popular faces are already a cliché. **Check the license** (OFL or another web-embeddable license) and self-host.

## Copy

Write from the user's side, in plain, active, sentence-case language. Use specific nouns, not "Unlock the power of…". Error messages say what happened and how to fix it. Empty states invite the next action. No exclamation marks unless the brand truly speaks that way.

## Quality floor (non-negotiable)

- Responsive from 360 px up; nothing scrolls sideways.
- WCAG 2.2 AA contrast; visible `:focus-visible` states; full keyboard operation; semantic HTML landmarks; labels on every input.
- `prefers-reduced-motion` respected; no layout shift from web fonts.
- Images have dimensions and alt text; above-the-fold media is not lazy-loaded.
- Lighthouse performance ≥ 90 on mobile for content pages.
