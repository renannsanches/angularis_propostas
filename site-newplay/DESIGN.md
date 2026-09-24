# NewPlay proposal layout

Refinement of the existing Angularis identity: dark neutral surfaces, pink accent and supplied brand marks. Visitors compare recurring plans and a separate implementation project, inspect terms and discuss contracting.

## Direction

Editorial split, Geist variable, prominent prices, aligned offer cards, native disclosures. DESIGN_VARIANCE 6, MOTION_INTENSITY 5, VISUAL_DENSITY 4. Static HTML remains directly viewable offline.

Reading path: introduction, recurring plans, implementation, strategic context, process, terms and full scope, next steps. No fabricated submission or acceptance workflow.

## System

- Container 1224px; responsive gutters 48/32/24/20px.
- Spacing 8/16/24/32/48px within groups; 64–120px between sections.
- Self-hosted Geist variable. Body 16px; display tracking no tighter than -0.04em.
- Background #111013, surface #1a181d, foreground #f5f1f6, muted #bcb4c1, accent #f47fad.
- Offer surfaces 14px corners, buttons 8px, recommendation badge 5px.
- Tabler outline icons, 1.5 stroke weight, locally vendored.
- 44px interaction targets, visible keyboard focus, skip navigation, semantic disclosures.

## Motion

GSAP entrance establishes hierarchy from an already visible state. Reading groups reveal once on scroll with 18px rise, 650ms ease-out and at most 210ms sibling staggering, as explicitly requested. Content is visible before enhancement; reduced motion disables the reveals. Desktop ScrollTrigger scales/fades the supplied hero mark and pins the implementation summary only when viewport height and content travel permit. No scroll hijacking or section-wide reveal masks.

## Content

Original proposals preserved in the parent directory; current publishable content lives in content/. Growth: 30–40 original pieces monthly. Scale: 50–60. Implementation payment: 50% at start and 50% upon completion after approval. The duplicate scope block preceding responsibilities was removed at the user's request. template.html contains the page; build.py embeds the original full scopes. dist is the complete portable site.

## Glass finish

User-requested Apple-inspired web glass approximation on plan and implementation cards: translucent dark surfaces, restrained brand-colored light, soft backdrop blur and fine reflective edges. High-contrast text, opaque fallbacks for reduced transparency and subtle pointer reflection only on fine pointers. This is a CSS approximation, not an official Apple web component.
