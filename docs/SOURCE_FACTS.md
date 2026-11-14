# SOURCE FACTS — where every value in `data/vac.json` comes from

Two sources only:

- **SAM** = VAC's own SAM.gov entity record (Entity Management API v3, lookup by UEI, sections entityRegistration + coreData + assertions), read from VAC's internal SAM mirror. Record fetched **2026-11-09 08:00:33 UTC** (03:00 Eastern). Read for this build on 2026-11-13. Everything in this column is public on SAM.gov.
- **OWNER** = the owner record stated in the build tasking of 2026-11-13, plus the owner's phone-line handoff of 2026-11-13.

No API key, tax ID, account number or confirmation number is recorded here or anywhere in this repository.

## Entity facts

| `vac.json` field | Value | Source | SAM field | Fetched (UTC) |
|---|---|---|---|---|
| `entity.legal_name` | Victory Arms Company LLC | SAM | entityRegistration.legalBusinessName (SAM stores it in capitals) | 2026-11-09 08:00 |
| `entity.uei` | ZZQAKXV8EJ41 | SAM | entityRegistration.ueiSAM | 2026-11-09 08:00 |
| `entity.cage` | 02S54 | SAM | entityRegistration.cageCode | 2026-11-09 08:00 |
| `entity.sam_status` | Active | SAM | entityRegistration.registrationStatus | 2026-11-09 08:00 |
| `entity.sam_expiration` | 2027-10-05 | SAM | entityRegistration.registrationExpirationDate | 2026-11-09 08:00 |
| `entity.primary_naics` | 611699 | SAM | assertions.goodsAndServices.primaryNaics | 2026-11-09 08:00 |
| `entity.naics` | 15 codes (below) | SAM | assertions.goodsAndServices.naicsList | 2026-11-09 08:00 |
| `entity.psc` | 23 codes (below) | SAM | assertions.goodsAndServices.pscList | 2026-11-09 08:00 |
| `entity.city`, `entity.state` | Jacksonville, NC | SAM | coreData.physicalAddress | 2026-11-09 08:00 |
| `site.url` | https://victoryarmscompany.com/ | SAM | coreData.entityInformation.entityURL | 2026-11-09 08:00 |
| `entity.certifications`, `entity.cert_renewal` | SBA-certified SDVOSB · VOSB, renewal 2028-12-15 | OWNER | SAM's sbaBusinessTypeList is empty for this record; SAM carries only the self-representations "Veteran-Owned Business" and "Service-Disabled Veteran-Owned Business" | n/a |
| `entity.dibbs` | Registered | OWNER | not a SAM field (owner record: registered 2026-10-29) | n/a |
| `entity.email` | contracts@victoryarmscompany.com | OWNER | n/a | n/a |
| `entity.phone` | (910) 762-4050 | OWNER | the SAM points-of-contact section is not in the mirror, so the SAM POC phone could not be read; this is the owner's stated public VAC line | n/a |
| `entity.region_note` | Camp Lejeune region | OWNER | n/a | n/a |
| `entity.sourcing` | domestic and allied sourcing only | OWNER | n/a | n/a |
| `principal.*` | Jelani A. Staine, Principal · Captain, U.S. Marine Corps (Veteran) · Owner and authorized signatory | OWNER | n/a | n/a |

Other SAM values read and deliberately not published: registration activation date 2026-10-06, initial registration date 2024-08-16, purpose of registration "All Awards", exclusion flag "N", the street address (owner decision pending), the trade name (kept off this site by the domain-separation rule).

## NAICS list as registered in SAM

SAM lists 21 entries, which are 15 distinct codes (541330 and 541715 each appear four times with different size-standard exceptions). Primary: **611699**.

`325920 332992 332993 332994 333517 336414 336415 423910 423990 459110 541330 541715 561210 611430 611699`

## PSC list as registered in SAM

`1305 1310 1315 1320 1337 1338 1340 1376 1390 1395 1398 1410 1420 1550 3408 3693 AC12 AC13 U005 U006 U008 U009 U099`

## Copy

The wording in `copy.*` (headline, competency cards, differentiators, direction line) comes from the owner-approved sample canvas of 2026-11-13, edited only where a binding rule required it. The edits are listed in `docs/VAC_WebCapStmt_Report_20261113.md`, section 4. The legal citations in the Set-Aside differentiator (FAR subpart 19.14; 38 U.S.C. 8127) are from the owner-approved canvas and the build tasking.
