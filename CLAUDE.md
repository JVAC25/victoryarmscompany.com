# CLAUDE.md — victoryarmscompany.com

Government-facing site for Victory Arms Company LLC (VAC only). Audience: contracting officers, primes, small-business liaison officers.

## Rules that bind every change

- `data/vac.json` is the single source of truth. Never type a fact into `index.html` or `capability-statement.html`; they are generated.
- Every value in `data/vac.json` must trace to `docs/SOURCE_FACTS.md` (SAM.gov record) or the owner record.
- Principal line is exactly: Jelani A. Staine, Principal · Captain, U.S. Marine Corps (Veteran). No service history of any kind.
- Contact is contracts@victoryarmscompany.com only. No link, form or email to any other domain.
- No civilian-class content. Training is firearms and marksmanship instruction for government, law-enforcement and unit customers.
- No claim of manufacturing capability, licences, awards, contract vehicles, partners or vendor relationships.
- No tax ID, credentials, account numbers or confirmation numbers in the repository.
- No remote fonts, no third-party scripts, no analytics. Fonts are self-hosted in `assets/fonts/`.
- Colors: only the ten tokens at the top of `assets/site.css`. No gradients. Design is locked; do not reinterpret it.
- The logo `assets/vac-logo.png` is used as-is. Do not generate or alter a logo.
- Work on a branch. Do not push to main or deploy without the owner's approval.

## Commands

- Build: `python3 scripts/build.py`
- QA gate: `python3 scripts/qa.py`
- PDF: headless Microsoft Edge, see README.md

## Milestones

- **2026-11-13:** Rebuilt on branch `redesign-2026-11`. Single source of truth `data/vac.json`; build script `scripts/build.py` (Python standard library only) renders the site and the one-page Capability Statement from it; PDF pipeline via headless Edge with dated file + stable alias; QA gate `scripts/qa.py`; pre-commit secret check in `scripts/hooks/`. Not deployed.
