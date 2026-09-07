# leonardovanni.com

Personal academic website of Leonardo Vanni — static, no client-side
JavaScript (the mobile nav is a CSS-only disclosure).

Design: warm-paper editorial — ink text, rust accent, hairline rules, mono
kickers. Built with [Astro](https://astro.build) + TypeScript (strict),
Tailwind CSS v4, MDX notes, and build-time math via remark-math +
rehype-KaTeX. Fonts (Space Grotesk, Inter, JetBrains Mono) are self-hosted,
latin subset only — no CDN or third-party requests anywhere.

## Commands

| Command           | Action                                            |
| ----------------- | ------------------------------------------------- |
| `npm install`     | Install dependencies                              |
| `npm run dev`     | Dev server at `localhost:4321`                    |
| `npm run build`   | Production build to `./dist/`                     |
| `npm run preview` | Preview the production build                      |
| `npm run check`   | Type-check (`astro check`)                        |
| `npm run og`      | Regenerate `public/og-default.png` from the fonts |

Requires Node ≥ 22.12 (Astro 6).

## Site structure

Nav is deliberately small: Research · CV · Notes · Contact (+ `/thesis/`,
linked from Research, the homepage, and news). `/projects/` and `/teaching/`
are static redirects (see `astro.config.mjs`) — projects merged into
`/research/`, teaching & leadership onto `/cv/`.

## Owner-supplied assets (never commit placeholders)

Still missing:

- `public/thesis/vanni-2026-bsc-thesis.pdf` — thesis PDF, acknowledgements
  removed. The "Download thesis (PDF)" button on `/thesis/` renders only once
  this file exists (build-time `fs.existsSync` check in
  `src/pages/thesis.astro`); until then the page shows an "email me" line.
- Google Scholar / ORCID links — placeholders in
  `src/content/pages/contact.md`, add after first indexed publication.
- Real project media (thumbnails/videos) — until then, each research row uses
  a hand-drawn SVG motif from `src/components/Motif.astro` (one per project;
  abstract diagrams, never fake screenshots).

## Editing content

### Homepage copy

- `src/content/pages/hero.md` — name, mono status line, the display
  `statement`, the `seeking` line (delete once a position is secured), links,
  and the "Currently:" body paragraph.
- `src/content/pages/taste.md` — the three "What I care about" items.
- `src/content/pages/bio.md` — the About paragraph (has dated TODO comments:
  graduation wording, TUM announcement).

### Add a project

Create `src/content/projects/<slug>.md` with frontmatter matching the schema
in `src/content.config.ts`. Key fields: `title`, `shortTitle` (kicker label),
`hook` (one sharp sentence — the homepage headline for the row), `oneLiner`
(1–2 sentence contribution, shown on homepage rows), `abstract`, `role`,
`collaborators?`, `status: ongoing | completed | public`, `period`, `links?`,
`comingSoon?`, `featured`, `order`, `draft?`.

The markdown **body** is the researcher-facing detail (problem / idea / why
it matters) rendered on `/research/`; when a project has no body, the
`abstract` is shown there instead. Homepage shows the three `featured: true`
entries.

- `draft: true` → never built.
- A row shows its links row **or** the muted `comingSoon` line, never both.
- Any link whose URL contains `[PLACEHOLDER` is kept in the file but skipped
  at render time.
- New projects get the fallback `pointcloud` motif; add a dedicated one in
  `src/components/Motif.astro` and map it in
  `src/components/ResearchRow.astro`.

### Add a news item

Create `src/content/news/<yyyy-mm-slug>.md`:

```yaml
---
date: 2026-07-01
text: "One sentence. May contain one inline [markdown link](/path/)."
---
```

The homepage shows the latest 4, newest first. **Future-dated items are
hidden** until a build on/after their date (filter in
`src/pages/index.astro`) — the graduation item is future-dated on purpose;
after graduating, verify its text and push any commit to rebuild.

### Add a note

Create `src/content/notes/<slug>.mdx` with `title`, `date`, `description`,
optional `draft`. Math (`$...$`, `$$...$$`) and code highlighting work out of
the box. With zero notes, `/notes/` shows only the intro sentence (the build
warning "No files found matching \*\*/\*.mdx" is harmless and disappears with
the first note). When the first note goes live, revisit the intro sentence in
`src/content/pages/notes-index.md` ("Nothing here yet.").

## Graduation checklist (July 21, 2026)

1. `src/content/news/2026-06-graduation.md` — verify date/text/grade; it
   renders automatically on the first build after the date.
2. `src/content/pages/bio.md` — follow the AFTER GRADUATION comment
   ("completing" → "graduated ... 110 cum laude").

## TUM announcement checklist (do NOT edit before it is public)

TUM must not appear as Leonardo's own destination until publicly announced.
On announcement day, search the codebase for `AFTER TUM` and follow each
comment:

1. `src/content/pages/bio.md` — insert the TUM clause after the Polytechnique
   clause as the comment specifies.
2. `src/content/pages/cv-page.md` — add the TUM entry where the comment marks
   it (also update the CV PDF itself).
3. Off-site (handoff `extras/`, not in this repo): GitHub profile README and
   LinkedIn headline/About.

## Deployment (GitHub Pages)

`.github/workflows/deploy.yml` builds with `withastro/action` and deploys via
`actions/deploy-pages` on every push to `main`.

`astro.config.mjs` sets `site: 'https://www.leonardovanni.com'` (canonical
URLs, sitemap); `public/robots.txt` points at `/sitemap-index.xml`.

## Notes for maintainers

- Design tokens live in `src/styles/global.css` (`--bg`, `--surface`,
  `--border`, `--rule`, `--text`, `--muted`, `--accent`,
  `--status-public`). All text-on-background pairs were checked at ≥ 4.5:1
  (WCAG AA); re-check if you change them.
- No animations, no analytics, no client frameworks, no contact forms — by
  design. Hover feedback is a color change only.
- `vite` is pinned as a devDependency so `@tailwindcss/vite` resolves the same
  Vite major as Astro (removing it re-introduces a rolldown-vite binding
  mismatch at build time).
- `npm run og` regenerates the social card (`public/og-default.png`); it uses
  the dev-only static font packages (`@fontsource/space-grotesk`,
  `@fontsource/inter`) because resvg renders variable fonts incorrectly. Run
  it after changing the palette or the hero wording.
