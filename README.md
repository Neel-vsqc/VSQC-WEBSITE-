# VSQC Website

Static website for **VSQC — Vaishno Sai Quality Consultants Pvt. Ltd.**: management systems, ESG, digital transformation, information security and safety consulting.

Plain HTML, CSS and JavaScript. No framework, no build step needed to host it.

## Pages

| Page | File |
| --- | --- |
| Home: hero + scroll-driven 7-service video showcase | `index.html` |
| Service pages (7) | `service-iso.html`, `service-esg.html`, `service-vendor.html`, `service-training.html`, `service-digital.html`, `service-infosec.html`, `service-safety.html` |
| Portal, Achievements, Policies, Team, Contact | `portal.html`, `achievements.html`, `policies.html`, `team.html`, `contact.html` |
| Not found | `404.html` |

## Run locally

Serve the folder (the videos need a real server for seeking):

```bash
npx serve -l 5173 .
```

Then open http://localhost:5173. `serve.json` makes `/policies` and `/policies.html` both work.

## Editing content

All copy lives in `_build/content.py`; layout templates are in `_build/build.py`. After editing, regenerate the HTML:

```bash
python _build/build.py
```

Do not upload `_build/` to the web host. It is only for editing.

## Before launch

In `_build/content.py` → `SITE`:

- `email`: the real contact address (currently a placeholder, `info@vsqc.in`)
- `form_endpoint`: a form service (e.g. Formspree). Until set, forms open the visitor's email app. Anonymous whistleblower reports need it.
- `portal_customer_url` / `portal_employee_url`: portal sign-in addresses

Official partner/client logos: put `logos/<slug>.svg` (or `.png`) next to `index.html` and rebuild. Slugs: `tuv-rheinland`, `bsi`, `lrqa`, `tata-realty`, `gemsons-precision`.

## How the showcase video works

`clip-1.mp4` is the hero loop. Odd clips 3–15 are the seven service loops; even clips 2–14 are the transitions between them. Every clip's last frame matches the next clip's first frame. Scrolling forward one step plays the transition, then cuts to the loop; scrolling back or jumping crossfades. Timings are in the `CONFIG` block at the top of `main.js`.
