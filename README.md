# victoryarmscompany.com

Government-facing site and one-page Capability Statement for Victory Arms Company LLC.
Static HTML on GitHub Pages. No frameworks, no npm, no third-party scripts, no remote fonts.

## How it works

| Piece | File |
|---|---|
| Single source of truth | `data/vac.json` |
| Build script (Python 3.11+, standard library only) | `scripts/build.py` |
| Generated pages (do not edit by hand) | `index.html`, `capability-statement.html`, `sitemap.xml`, `robots.txt` |
| Styles | `assets/site.css`, `assets/capstmt.css` |
| Self-hosted fonts + license | `assets/fonts/` |
| Capability Statement PDF | `assets/VAC_CapabilityStatement_<YYYYMMDD>.pdf` and the stable alias `assets/VAC_CapabilityStatement.pdf` |
| QA gate | `scripts/qa.py` |
| Where each fact came from | `docs/SOURCE_FACTS.md` |

## Change a fact

1. Edit `data/vac.json` (and record the source in `docs/SOURCE_FACTS.md`).
2. `python3 scripts/build.py`
3. Re-render the PDF from `capability-statement.html` with headless Microsoft Edge:
   `msedge --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=<out.pdf> <file URL of capability-statement.html>`
   Save it as the dated file and copy it over the alias.
4. `python3 scripts/qa.py` (every line must read PASS)

## One-time setup per clone

`git config core.hooksPath scripts/hooks` turns on the pre-commit check that blocks tax-ID-shaped numbers and SAM.gov API keys.
