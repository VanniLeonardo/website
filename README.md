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
| `npm run motifs`  | Regenerate the research motifs (see `scripts/motifs/`) |

Requires Node ≥ 22.12 (Astro 6).

## Site structure

Nav is deliberately small: Research · Experience · CV · Contact, plus
`/thesis/`, linked from Research, the homepage, and news. `/notes/` builds but
stays out of the nav until a note exists: an empty section is never
advertised. `/projects/` and `/teaching/` are static redirects (see
`astro.config.mjs`); projects merged into `/research/`, teaching and
leadership onto `/experience/`.

## Owner-supplied assets (never commit placeholders)

Still missing:

- `public/thesis/vanni-2026-bsc-thesis.pdf` — thesis PDF, acknowledgements
  removed. The "Download thesis (PDF)" button on `/thesis/` renders only once
  this file exists (build-time `fs.existsSync` check in
  `src/pages/thesis.astro`); until then the page shows an "email me" line.
Google Scholar and ORCID links in `src/content/pages/contact.md` are live and
verified, and both appear in the homepage JSON-LD `sameAs`.

Research rows carry a generated motif from `src/components/Motif.astro`, built
from real 3D geometry by `scripts/motifs/` (never a fake screenshot). The
prosthetic-arm entry also carries a real demo frame from the project's own
public media.

## Editing content

### Homepage copy

- `src/content/pages/hero.md` — name, mono status line (two variants, see
  below), the display `statement`, the `seeking` line (delete once a position
  is secured), and the links with their `weight` for the call-to-action
  hierarchy.
- `src/content/pages/bio.md` — the About paragraph.
- `src/content/pages/background.md` — the education entries, used by the
  homepage and the CV page.
- `src/content/pages/experience.md` — roles and the teaching block, used by
  `/experience/`, the homepage, and the CV page.

Wording that depends on the TUM start date is resolved at build time by
`src/lib/dates.ts`: a rebuild on or after 2026-10-01 switches "Incoming M.Sc."
to the present tense, in the hero and in the JSON-LD. There is no comment to
remember to action.

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

## Deployment (GitHub Pages)

`.github/workflows/deploy.yml` builds with `withastro/action` and deploys via
`actions/deploy-pages` on every push to `main`.

`astro.config.mjs` sets `site: 'https://leonardovanni.com'`, the apex domain,
which drives canonical URLs, `og:url` and the sitemap. `www` 301-redirects to
the apex, so the apex is the one canonical host.

`public/CNAME` must hold the apex domain too: GitHub Pages reads it on every
deploy and it decides the redirect direction. If it is set to `www`, the
redirect reverses and every canonical URL on the site points at a host that
redirects away.

## Notes for maintainers

- Design tokens live in `src/styles/global.css` (`--bg`, `--surface`,
  `--border`, `--rule`, `--text`, `--muted`, `--accent`,
  `--status-public`). All text-on-background pairs were checked at ≥ 4.5:1
  (WCAG AA); re-check if you change them.
- No animations, no analytics, no client frameworks, no contact forms, by
  design. Hover feedback is a colour change only.
- The research motifs are static SVG generated ahead of time, so they cost
  nothing at runtime: no WebGL and no client JavaScript. Regenerating them
  needs Python (`scripts/motifs/requirements.txt`); building the site does
  not.
- `vite` is pinned as a devDependency so `@tailwindcss/vite` resolves the same
  Vite major as Astro (removing it re-introduces a rolldown-vite binding
  mismatch at build time).
- `npm run og` regenerates the social card (`public/og-default.png`); it uses
  the dev-only static font packages (`@fontsource/space-grotesk`,
  `@fontsource/inter`) because resvg renders variable fonts incorrectly. Run
  it after changing the palette or the hero wording.
