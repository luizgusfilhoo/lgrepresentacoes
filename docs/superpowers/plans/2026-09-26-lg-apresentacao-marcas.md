# LG Representações Presentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a concise, professional single-page LG site with nine correctly presented brands, a controllable logo scroller, Instagram contact, and a Caruaru map.

**Architecture:** Keep the published root as the single source of truth in plain HTML, CSS and JavaScript; synchronize its deployable files to `dist/` for the existing Sites preview. Separate the brand interaction and map behavior into focused scripts. Present each of the three visual models to LG after its verification and wait for feedback before the next model.

**Tech Stack:** Static HTML/CSS/JavaScript, GitHub Pages `/lgrepresentacoes/`, locally served Leaflet for the map, existing Python `unittest` suite.

**Spec:** `docs/superpowers/specs/2026-09-26-lg-apresentacao-marcas-design.md`

**Runtime:** On this Mac, use the bundled Python at `/Users/luizfilho/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` and Node at `/Users/luizfilho/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node`; system `python3` and `git` may invoke unavailable Xcode tools. Commands below use `python3`/`node` as shorthand for these two absolute binaries and the bundled fallback `git`.

## Global Constraints

- Keep one page and the existing nine-brand order: Atlas, Dryko, Amatools, Mundial Prime, Lamesa, Odem, Saga Metais, Botafogo, J. Lobato.
- Preserve each brand's original logo colors and full silhouette; preserve the correct official site and supplied catalog links.
- Keep all internal URLs relative so they work under `/lgrepresentacoes/`.
- Support keyboard navigation, visible focus, `prefers-reduced-motion`, and a usable narrow mobile layout.
- Show only the Caruaru, PE region; no invented office address or customer geolocation.
- Keep `dist/` synchronized without discarding existing unrelated or user-owned files.
- Show the completed header/hero model, brand model, then compact About/contact/map model to LG, incorporating feedback before advancing.

## Review Focus

- At 320–390 px width, headings, logos, map, and controls remain readable without page-wide horizontal scroll (Tasks 1–3 browser checks).
- With reduced motion, the brand ribbon and reveals stop moving while all links remain accessible (Task 2 browser check).
- If map tiles or JavaScript fail, “Caruaru, Pernambuco” and an external map link remain usable (Task 3 test).
- Missing or mismatched logo/catalog/image paths fail a local-file and brand-mapping check before publication (Task 2 test).
- After deployment in a subdirectory, styles, scripts, images, PDFs, and `sobre/` navigation resolve correctly (Task 4 test and live check).

---

### Task 1: Compact header, hero and indicators — visual model 1

**Files:** Modify `index.html`, `style.css`, `main.js`; create `tests/test_home_presentation.py`.

**Interfaces:** Produces anchor IDs `top`, `marcas`, `sobre`, `contato` and the root HTML structure consumed by Tasks 2–4. Uses the current LG logo, team image, and approved numbers.

- [ ] Write failing `unittest` assertions that the navigation has the four destinations, the hero has one `h1`, the two actions lead to brands/contact, all four approved indicators exist, and Instagram links to `https://www.instagram.com/lg.represen/` with an accessible name.
- [ ] Run `python3 -m unittest tests/test_home_presentation.py -v`; verify those assertions fail against the current root page.
- [ ] Rework header, hero, indicators, typography and spacing in the three files. Use Manrope for reading and headings, preserve LG colors, add a recognizable Instagram SVG/icon link, and trim duplicated introductory text without deleting supplied facts.
- [ ] Run the targeted test; verify pass. Inspect at desktop and 390/320 px in the local preview for clipped text and horizontal overflow.
- [ ] Commit only the task's files. Show a desktop and mobile preview of this complete model to LG and apply requested adjustments before Task 2.

### Task 2: Brand ribbon and nine complete presentations — visual model 2

**Files:** Modify `index.html`, `style.css`; create `marcas.js`, `docs/brand-assets.md`; extend `tests/test_representadas.py`.

**Interfaces:** Consumes `#marcas` and existing `#marca-*` IDs. Produces a single nine-brand data mapping and accessible previous/next/select controls, consumed by no other feature. The ribbon links to each corresponding brand panel.

- [ ] Add failing tests for the nine ordered brand IDs; each panel's original-color logo, official URL, local PDF, product-line description, and asset-file existence; ribbon pause control and brand selection labels.
- [ ] Run `python3 -m unittest tests/test_representadas.py -v`; verify the new assertions fail.
- [ ] Research each product image against its official brand site or supplied catalog; record asset source and selection in `docs/brand-assets.md`. Use a catalog image when an official web image is unsuitable; optimize local images without cropping logos.
- [ ] Implement a single continuous logo ribbon with duplicated decorative group, edge fade, pause/focus behavior and reduced-motion styling. Implement readable brand panels in `marcas.js` with direct selection and previous/next controls; load that script from `index.html`.
- [ ] Run the targeted tests; verify pass. Inspect all nine panels and the ribbon at desktop and 390/320 px; verify keyboard controls, pause, full logo colors, reduced motion and no overflow.
- [ ] Commit only this task's files and selected assets. Show this complete model to LG and apply requested adjustments before Task 3.

### Task 3: Compact institutional content, contact and Caruaru map — visual model 3

**Files:** Modify `index.html`, `style.css`; create `caruaru-map.js`, `assets/vendor/leaflet/` files, `docs/react-component-notes.md`, `tests/test_location_and_contact.py`.

**Interfaces:** Consumes `#sobre`, `#contato`, current team contacts/hours and Instagram URL. `caruaru-map.js` initializes only the `#caruaru-map` element when near the viewport; no other script depends on Leaflet. Initial map center is approximately `[-8.29, -35.97]`, matching IBGE's Caruaru reference, and represents the city rather than an office address.

- [ ] Add failing tests that the institutional content contains founder, Pernambuco, purpose, mission, vision, five values and future goals without duplicate story sections; that contacts/hours remain complete; and that the map has a textual Caruaru fallback and external map link.
- [ ] Run `python3 -m unittest tests/test_location_and_contact.py -v`; verify the new assertions fail.
- [ ] Consolidate the repeated About blocks and compact the contact layout while preserving every approved person, number, address and daily hour. Place the Caruaru map beside/below the hours according to available width.
- [ ] Add locally hosted Leaflet, initialize it only near the map, with Caruaru marker, zoom/pan, attribution and disabled scroll-wheel zoom. Keep the fallback visible if tiles or script fail. In `docs/react-component-notes.md`, explain why this static project has no `/components/ui` and give the shadcn CLI, Tailwind and TypeScript setup path for a future React migration; document that the supplied React components were adapted as behavior here.
- [ ] Run the targeted tests; verify pass. Inspect map and fallback at desktop and 390/320 px, with keyboard and slow/offline network conditions.
- [ ] Commit only this task's files. Show this complete model to LG and apply requested adjustments before Task 4.

### Task 4: Synchronize, verify and publish

**Files:** Modify `index.html`, `robots.txt`, `sobre/index.html`; create `scripts/sync-dist.mjs`, `tests/test_publish_files.py`; update `dist/` deployable mirror.

**Interfaces:** `node scripts/sync-dist.mjs` copies the root deployable HTML/CSS/JS/assets/robots files into `dist/` without deleting unrelated files. GitHub Pages serves root `main`; Sites preview serves `dist/`.

- [ ] Add failing tests that root has no `noindex,nofollow`, `robots.txt` allows indexing, the canonical URL is `https://luizgusfilhoo.github.io/lgrepresentacoes/`, all local references resolve, `sobre/` returns to the root About anchor, and root/dist deployable files match after synchronization.
- [ ] Run `python3 -m unittest tests/test_publish_files.py -v`; verify failure.
- [ ] Implement metadata, canonical URL, robots rule and relative redirect. Write `scripts/sync-dist.mjs`, run it, and confirm it preserved unrelated `dist/` entries.
- [ ] Run all `python3 -m unittest discover -s tests -v` and `node --check main.js`, `node --check marcas.js`, `node --check caruaru-map.js`; verify pass. Inspect the local preview once more, including every catalog and Instagram link.
- [ ] Commit only the release files; push `main` after LG approves model 3. Confirm GitHub Pages finishes building and returns HTTP 200 for the page, key assets, and a PDF; show the live URL.
