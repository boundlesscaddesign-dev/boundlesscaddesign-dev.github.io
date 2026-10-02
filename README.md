# BoundlessCAD

[![Site check](https://github.com/boundlesscaddesign-dev/boundlesscaddesign-dev.github.io/actions/workflows/site-check.yml/badge.svg)](https://github.com/boundlesscaddesign-dev/boundlesscaddesign-dev.github.io/actions/workflows/site-check.yml)
[![Live site](https://img.shields.io/badge/site-live-7FD1C7)](https://boundlesscaddesign-dev.github.io)

Remote **exocad** design studio for dental labs, milling centres and digital clinics.
Crowns, bridges, implant crowns and custom abutments, full-arch implant prostheses, night guards and surgical guides — production-ready STL files plus the exocad project in 24–48 h. **The first case is designed free.**

**Website:** https://boundlesscaddesign-dev.github.io · **Email:** boundlesscad.design@gmail.com · **Instagram:** [@boundless.cad](https://instagram.com/boundless.cad)

## What is in this repository

This repository is the public website (GitHub Pages, no build step).

| Path | What it is |
|---|---|
| `index.html`, `es/` | Home page in English and Spanish |
| `send/` | How to send a case: files, digital prescription, FDI tooth chart |
| `plans/` | Monthly Design Seat plans |
| `review/` | Free design-review offer |
| `refer/`, `partner/`, `guide/` | Referral program, white-label partner page, outsourcing guide |
| `cases/` | Interactive 3D case library (three.js viewer, anonymised exocad exports) |
| `brand/` | Logos, social covers, Instagram highlight covers, email signature |
| `tools/` | Internal generators (QC report, brand kit, video pages) |
| `llms.txt`, `robots.txt`, `sitemap.xml` | Search and AI-crawler discovery |
| `.github/` | Issue forms, automated site checks, Dependabot |

## Working on the site

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

- **Add a 3D case:** see [`cases/README.md`](cases/README.md). Always check the file for patient or clinic names before publishing.
- **Add a page:** create `<name>/index.html`, link it from the nav, add it to `sitemap.xml` (the *Site check* workflow fails if a listed page does not exist).
- Pages marked `noindex` (for example `/for/` and `/v/`) are private landing pages and are intentionally not in the sitemap.

## Privacy

Case files published here are anonymised: no patient names, dates of birth, clinic or doctor names. Customer files are never stored in this repository.

## Contributing and security

Found a typo or a broken link? Open an issue using the templates, or email us. Security reports: see [`SECURITY.md`](SECURITY.md).

© BoundlessCAD. All rights reserved — see [`LICENSE`](LICENSE).
