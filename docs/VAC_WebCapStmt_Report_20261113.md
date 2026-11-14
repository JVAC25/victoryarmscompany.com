# VAC website + Capability Statement rebuild — report (2026-11-13)

**Status:** built and committed on branch `redesign-2026-11` in a local clone. **Not pushed. Not deployed.** The live site is unchanged.

**Where it is:** WSL `~/projects/victoryarmscompany.com` (Windows path `\\wsl.localhost\Ubuntu-24.04\home\sentinel\projects\victoryarmscompany.com`).

**What to look at:** `index.html` (the site), `assets/VAC_CapabilityStatement_20261113.pdf` (one page), `docs/screenshots/site-375.png` and `site-1440.png`.

## Decisions waiting on the owner

| # | Decision | What was built (default) |
|---|---|---|
| 1 | Street address on the site and PDF | **Not shown.** City and state only. The SAM address is the home address; it matches SAM, so it can be shown by request. |
| 2 | Public phone number | **(910) 762-4050** (the owner's stated VAC line). The SAM contact phone could not be read, see section 3. |
| 3 | The full SAM NAICS and PSC lists on a public page | **Shown, codes only, labelled "SAM.gov".** See counsel flag 1 before publishing. |
| 4 | The one forward-looking "Company direction" line | **Shown** on both. One switch in `data/vac.json` (`show_direction`) turns it off. |
| 5 | Publishing | This session's GitHub login can read the JVAC25 repository but cannot write to it. Publishing needs a login with write access (section 6). |

## 1. Data pull

Source: VAC's SAM.gov entity record, read from the internal SAM mirror on the collector server. The cloud copy of the mirror has no entity rows, so the collector server's copy was used. Record fetched 2026-11-09 03:00 Eastern (08:00:33 UTC).

| Field | Value | Source | Fetched (UTC) |
|---|---|---|---|
| Legal name | Victory Arms Company LLC | SAM | 2026-11-09 08:00 |
| UEI | ZZQAKXV8EJ41 | SAM | 2026-11-09 08:00 |
| CAGE | 02S54 | SAM | 2026-11-09 08:00 |
| Registration status | Active | SAM | 2026-11-09 08:00 |
| Registration expiration | 2027-10-05 | SAM | 2026-11-09 08:00 |
| Primary NAICS | 611699 | SAM | 2026-11-09 08:00 |
| NAICS list | 21 SAM entries = 15 distinct codes: 325920, 332992, 332993, 332994, 333517, 336414, 336415, 423910, 423990, 459110, 541330, 541715, 561210, 611430, 611699 | SAM | 2026-11-09 08:00 |
| PSC list | 23 codes: 1305, 1310, 1315, 1320, 1337, 1338, 1340, 1376, 1390, 1395, 1398, 1410, 1420, 1550, 3408, 3693, AC12, AC13, U005, U006, U008, U009, U099 | SAM | 2026-11-09 08:00 |
| City, state | Jacksonville, NC | SAM | 2026-11-09 08:00 |
| Website on record | https://victoryarmscompany.com/ | SAM | 2026-11-09 08:00 |
| Contact business phone | not available from the mirror | see section 3 | n/a |

Full field-by-field trace: `docs/SOURCE_FACTS.md`.

**The SAM NAICS list is not the list in the phone-session handoff.** That handoff named 611519, 238990 and 332216; none of the three is in the current SAM record. SAM has 541715, 333517, 336414, 336415 and 325920 that the handoff did not name. The site uses SAM.

## 2. Claims removed, and why

From the **old site** (`index.html` on main):

| Removed | Why |
|---|---|
| "retired" wording for the principal (hero, overview, personnel card) | Rule: the only form is "Captain, U.S. Marine Corps (Veteran)" |
| Three hero statistics and the six "Why Victory Arms" lines built on the principal's military service | Owner direction 2026-11-13: no service history, counts or dollar values anywhere |
| "Key Personnel" card: award, billets, specialty code, deployments, clearance line, degree and certification line | Same direction. Replaced by the one-line Leadership block |
| "Past Performance" section (two blocks of service metrics) | It was service history presented as company past performance. Nothing may imply VAC holds federal awards or CPARS |
| Civilian carry-class instruction line and the civilian instructor certification tile with its number | No civilian-class content on the government site |
| "SDVOSB — SBA Certification Pending" | Out of date. Now "SBA-certified SDVOSB · VOSB" (active, renewal 15 Dec 2028) |
| "Boots to Business — SBA Graduate" tile | A course, not a certification a buyer can use |
| "Small Arms & Ordnance Procurement", "Ballistic Protection", the caliber list | Reads as selling firearms and regulated items. Replaced by resale and distribution wording (counsel flag 2) |
| NAICS shown as five codes with manufacturing descriptions | Replaced by the full SAM list, codes only |
| Contact email and both mail links pointing at the training domain | Domain separation. Contact is contracts@victoryarmscompany.com only |
| Old phone number (347 area code) | Replaced by the VAC line |
| Remote font loaded from Google | No external font loads. Fonts are now self-hosted |
| Download button pointing at a PDF that was never in the repository | Dead link. The new link is `assets/VAC_CapabilityStatement.pdf`, which exists |
| Gradient hero, off-palette colors, check-mark glyphs, old wordmark SVG (Arial) | Design locked to the VAC token set |

From the **old Capability Statement** (2026-03-30, state-bid version):

| Removed | Why |
|---|---|
| "(Ret.)" after the principal's rank, three places | Same rule as above |
| SAM line with the expired 2026 date | Replaced by SAM: Active, expires 5 Oct 2027 |
| "VA CVE Certified" | Wrong certifier. Now "SBA-certified SDVOSB · VOSB" |
| NAICS shown as two codes only | Primary 611699 plus the full SAM list |
| The tax ID | Never on a public page or PDF |
| The state contract number, state business licence number, state supplier-portal ID, "Prepared for" line | Bid-specific content for one state solicitation |
| "Approved Manufacturer Relationships" naming six ammunition makers | No vendor relationship is claimed without a signed agreement |
| "Past Performance" paragraph built on the principal's service; years-of-service and school-assignment sentences in the overview | Service history; implied past performance |
| "experienced with federal contracting requirements" | Unsupported. Replaced by the registrations (SAM, SBA, DIBBS) |
| "30-day ARO delivery commitment", "FOB Destination" | Solicitation-specific terms, not standing capabilities |
| Street address in the header and contact block | Owner decision 1 above |
| "SAAMI-compliant ... approved domestic manufacturers", "ITB-compliant", product-line claims | Tied to the removed vendor claims and to one bid |

## 3. Fields filled from the owner record because the mirror lacked them

| Field | Why the mirror lacked it | Value used |
|---|---|---|
| Business phone | The collector does not pull SAM's points-of-contact section | (910) 762-4050, from the owner's phone-line handoff of 2026-11-13 |
| SBA certification (SDVOSB, VOSB, renewal date) | SAM's SBA certification list is empty for this record; SAM shows only the self-representations | Owner record: SBA-certified SDVOSB and VOSB, renewal 2028-12-15 |
| DIBBS registration | Not a SAM field | Owner record: registered (2026-10-29) |
| Contracting email, principal line, sourcing stance, lines of business | Not SAM fields | Owner record, as written |

## 4. Copy choices for owner review

The approved sample canvas is the wording source. Changes made to it, each forced by a rule in the tasking:

| Canvas wording | Built wording | Reason |
|---|---|---|
| Headline "... & Weapons Training" | "... & Marksmanship Training" | Training is described only as firearms and marksmanship instruction |
| Card 1 "Ammunition & Small-Arms Supply"; codes "NAICS 423910 · FSC 1305 / 1005"; "weapon accessories (FSC 1005)" | "Ammunition Supply & Distribution"; "NAICS 423910 · PSC 1305"; "supplied by resale and distribution" | 1005 is not in the SAM PSC list, and "small-arms supply" reads as selling firearms (counsel flag 2) |
| Card 2 "Weapons & Marksmanship Training"; "delivered on-site or at partner ranges" | "Firearms & Marksmanship Training"; customers named as government, law-enforcement and unit; "at the customer's range or a contracted commercial range" | Training wording rule; no claim of partners |
| Card 3 headed "TACTICAL EQUIPMENT", no codes | "NAICS 423990 · DLA DIBBS"; title "Tactical Equipment & Federal Supply" | Each card is headed by codes from the SAM record |
| Subhead "Headquartered in Jacksonville ..." | "Located in Jacksonville ..." | Plain statement of place |
| Leadership: second sentence "Prices, signs and manages every quote ..." | Dropped | The tasking sets Leadership to one line. The same fact is in the Principal-Direct differentiator |
| Placeholders for SAM expiration, secondary NAICS, PSC, phone | Filled from section 1 and section 3 | |

Other choices:

- **Street address:** not shown (decision 1).
- **Company Overview** (PDF only): one paragraph written from the owner record's three lines of business. The canvas had none.
- **Sourcing stance:** shown as a row in Company Data on both.
- **NAICS and PSC:** codes only, without SAM's descriptions, labelled "SAM.gov" so they read as registration data.
- **Header:** the site header carries UEI and CAGE beside the lockup. Section links appear at 1024 px and wider.
- **Logo:** used as-is (1024 px file shown at 40 px). It is 1.5 MB, which slows the first load on a phone. Not altered, per the rule.
- **Phone:** shown as text, not a tap-to-call link, because the tasking allows only internal links and the contracting mail link.

## 5. Counsel flags (free: APEX Accelerator / NC SBTDC)

1. **SAM lists codes VAC has no current licence or capability for.** The NAICS list includes ammunition, small-arms, explosives, guided-missile and machine-tool manufacturing; the PSC list includes large-calibre ammunition, bulk explosives, rockets, guided missiles and unmanned aircraft. The record says these are registered by design. The site shows them as codes only under "SAM.gov" and claims no manufacturing, FFL/FEL or ITAR registration anywhere. Question for a free counselor before publishing: does listing these registered codes on a public capability page create a representation problem for a company with no FFL/FEL or DDTC registration? No determination is made here.
2. **Scope wording.** Ammunition and equipment are described as "resale and distribution" throughout. NAICS 332992 and 332994 appear only in the code list, never in a capability sentence. This is the existing open question on scope language against no FFL/FEL.
3. **Citations in the Set-Aside line** (FAR subpart 19.14; 38 U.S.C. 8127) are carried from the approved canvas and the tasking. They were not re-read against the current FAR text in this session.

## 6. QA results

`python3 scripts/qa.py` — all checks pass:

- Forbidden-term scan: zero hits in shipped text files (the tasking's list, plus the trade name, the internal system names, analytics tags, the tax-ID pattern and the SAM key prefix).
- CSS: only the ten locked color tokens; no gradients, no imports, no remote URLs.
- Both pages: balanced tags, no JavaScript (one JSON-LD data block), every link is internal and resolves or is the contracting mail link, every stylesheet, font, image and icon is local.
- Every NAICS and PSC code on both pages is in `data/vac.json`; UEI, CAGE, primary NAICS, email, phone and legal name all render from it.
- PDF: exactly 1 page, US Letter; the dated file and the stable alias are byte-identical; the download link resolves.
- Screenshots at 375 px and 1440 px are in `docs/screenshots/`.

Not done as written, and why:

- **Local preview with `python3 -m http.server`:** the session's permission system refused to start a server. Pages were rendered straight from the files with headless Edge instead, which is the same method the tasking gives for the PDF. "No console errors" is supported by the pages having no scripts and no missing local files; it was not observed in a browser console.
- **Design-parity screenshots** are on disk in `docs/screenshots/qm-parity/` but are **left out of git on purpose** (`.gitignore`). This repository is public, and those images show the internal tool's artboards. Copies are in Downloads.
- **Forbidden-term scan of the PDF text and of binary files** was not run (no PDF text tool on the machine). The PDF is printed from the HTML that passed.
- **GitHub Pages:** `_config.yml` keeps `docs/`, `scripts/`, `README.md` and `CLAUDE.md` off the public site. This assumes Pages builds from the branch in its default mode. If Pages is set to another mode, those files would be served.
- **Old content stays in the public git history** of the repository (the previous `index.html`). This rebuild removes it from the site, not from history.

## 7. The one command to publish, once approved

Run in WSL Ubuntu, signed in to GitHub as an account with write access to JVAC25 (this session's login has read access only):

```
cd ~/projects/victoryarmscompany.com && git checkout main && git merge --no-ff redesign-2026-11 -m "Publish redesign-2026-11" && git push origin main
```

GitHub Pages publishes main automatically. DNS is not touched.
