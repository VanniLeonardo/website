# leonardovanni.com

Personal academic website of Leonardo Vanni — static, dark-only, no client-side
JavaScript (the mobile nav is a CSS-only disclosure).

Built with [Astro](https://astro.build) + TypeScript (strict), Tailwind CSS v4,
MDX notes, and build-time math via remark-math + rehype-KaTeX. Fonts
(Space Grotesk, Inter, JetBrains Mono) are self-hosted, latin subset only —
no CDN or third-party requests anywhere.

## Commands

| Command           | Action                                            |
| ----------------- | ------------------------------------------------- |
| `npm install`     | Install dependencies                              |
| `npm run dev`     | Dev server at `localhost:4321`                    |
| `npm run build`   | Production build to `./dist/`                     |
| `npm run preview` | Preview the production build                      |
| `npm run check`   | Type-check (`astro check`)                        |
| `npm run og`      | Regenerate `public/og-default.png` from the fonts |

## Owner-supplied assets (never commit placeholders)

Still missing — drop these files at exactly these paths. Links/buttons are
already wired and the site builds fine while they are missing (the download
links 404 until the files exist, which is expected):

- `public/cv/leonardo-vanni-cv.pdf` — CV, **no phone number**
- `public/thesis/vanni-2026-bsc-thesis.pdf` — thesis PDF, acknowledgements removed
- two thesis figures in `src/assets/thesis/` (export per the FIGURES comment
  in `src/content/pages/thesis-page.md`), then uncomment the `<Image>` slots
  in `src/pages/thesis.astro` and match the filenames

Already in place: `src/assets/photo.jpg` (rendered by
`src/components/PhotoPlaceholder.astro` via `astro:assets`, center-cropped to
a 480×480 square).

## Editing content

### Add a project

Create `src/content/projects/<slug>.md` with frontmatter matching the schema
in `src/content.config.ts` (title, oneLiner, abstract, tags, role,
collaborators?, status: `ongoing | completed | public`, period, links?,
comingSoon?, featured, order, draft?). Cards render on `/projects/` sorted by
`order`; the three `featured: true` entries appear on the homepage.

- `draft: true` → never built.
- A card shows its links row **or** the muted `comingSoon` line, never both.
- Any link whose URL contains `[PLACEHOLDER` is kept in the file but skipped
  at render time (currently: the Prosthetic-Arm ResearchGate link — replace it
  with the real URL when ready).

### Add a news item

Create `src/content/news/<yyyy-mm-slug>.md`:

```yaml
---
date: 2026-07-01
text: "One sentence. May contain one inline [markdown link](/path/)."
---
```

The homepage shows the latest 4, newest first. The four existing items carry
`# TODO` comments — set the exact dates before launch.

### Add a note

Create `src/content/notes/<slug>.mdx` with `title`, `date`, `description`,
optional `draft`. Math (`$...$`, `$$...$$`) and code highlighting work out of
the box. With zero notes, `/notes/` shows only the intro sentence (the build
warning "No files found matching \*\*/\*.mdx" is harmless and disappears with
the first note). When the first note goes live, revisit the intro sentence in
`src/content/pages/notes-index.md` ("Nothing here yet.").

## TUM announcement checklist (do NOT edit before it is public)

TUM must not appear as Leonardo's own destination until publicly announced;
as the affiliation of TopoEgo collaborators it is fine. On announcement day,
search the codebase for `AFTER TUM ANNOUNCEMENT` and follow each comment:

1. `src/content/pages/bio.md` — insert the TUM clause after the Polytechnique
   clause as the comment specifies.
2. `src/content/pages/cv-page.md` — add the TUM entry under Education where
   the comment marks it (also update the CV PDF itself).
3. Off-site (handoff `extras/`, not in this repo): GitHub profile README and
   LinkedIn headline/About.

## TopoEgo release-day checklist

When the paper/code/benchmark go public (see the binding comment in
`src/content/projects/topoego.md`):

1. Replace the `comingSoon` field with a `links` array (paper, code, benchmark).
2. Consider `status: public` and promote to a dedicated `/projects/topoego/`
   page (v2 — individual project pages intentionally do not exist in v1).
3. Add TopoEgo to LinkedIn Featured (handoff `extras/`).
4. Confirm Federico Tombari's preferred affiliation wording ("TUM" vs
   "TUM & Google") — see the comment in `topoego.md`.

## Deployment (GitHub Pages)

`.github/workflows/deploy.yml` builds with `withastro/action` and deploys via
`actions/deploy-pages` on every push to `main`. One-time repo setup:

1. Push to GitHub; in **Settings → Pages** set Source to **GitHub Actions**.
2. Set the custom domain to `www.leonardovanni.com` (DNS: CNAME record for
   `www` → `<user>.github.io`, plus apex redirect at the registrar if wanted).
3. `public/CNAME` is copied into every build, so the custom domain survives
   deploys.

`astro.config.mjs` sets `site: 'https://www.leonardovanni.com'` (canonical
URLs, sitemap); `public/robots.txt` points at `/sitemap-index.xml`.

## Notes for maintainers

- Design tokens live in `src/styles/global.css` (`--bg`, `--surface`,
  `--border`, `--text`, `--muted`, `--accent`, `--status-public`).
- No animations, no analytics, no client frameworks, no contact forms — by
  design. Hover feedback is a border/text color change only.
- `vite` is pinned as a devDependency so `@tailwindcss/vite` resolves the same
  Vite major as Astro (removing it re-introduces a rolldown-vite binding
  mismatch at build time).
- `npm run og` regenerates the social card (`public/og-default.png`); it uses
  the dev-only static font packages (`@fontsource/space-grotesk`,
  `@fontsource/inter`) because resvg renders variable fonts incorrectly.
