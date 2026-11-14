#!/usr/bin/env python3
"""Build index.html, capability-statement.html, sitemap.xml and robots.txt from data/vac.json.

Python 3.11+ standard library only. Usage:  python3 scripts/build.py
The site and the one-page statement render from the same data file, so they cannot disagree.
"""
from __future__ import annotations

import json
import sys
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def e(value: object) -> str:
    return escape(str(value), quote=True)


def fmt_date(iso: str) -> str:
    d = date.fromisoformat(iso)
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def compact(iso: str) -> str:
    return iso.replace("-", "")


def badge(text: str, cert: bool = False) -> str:
    cls = "badge cert" if cert else "badge"
    return f'<span class="{cls}">{e(text)}</span>'


def cards(items: list[dict]) -> str:
    out = []
    for c in items:
        lis = "".join(f"<li>{e(b)}</li>" for b in c["bullets"])
        out.append(
            '<article class="card">'
            f'<span class="label codes">{e(c["codes"])}</span>'
            f'<h3>{e(c["title"])}</h3><ul>{lis}</ul></article>'
        )
    return "\n".join(out)


def diffs(items: list[dict]) -> str:
    return "\n".join(
        f'<div class="diff"><h3>{e(d["title"])}</h3><p>{e(d["text"])}</p></div>' for d in items
    )


def row(label: str, value_html: str) -> str:
    return f'<div class="data-row"><dt class="label">{e(label)}</dt><dd>{value_html}</dd></div>'


def head(v: dict, *, title: str, description: str, canonical: str, css: list[str], html_class: str = "") -> str:
    ent = v["entity"]
    site = v["site"]
    logo = site["url"] + "assets/vac-logo.png"
    ld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": ent["legal_name"],
        "legalName": ent["legal_name"],
        "url": site["url"],
        "logo": logo,
        "email": ent["email"],
        "telephone": ent["phone_e164"],
        "naics": ent["primary_naics"],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": ent["city"],
            "addressRegion": ent["state"],
            "addressCountry": ent["country"],
        },
        "identifier": [
            {"@type": "PropertyValue", "propertyID": "UEI", "name": "SAM.gov Unique Entity ID", "value": ent["uei"]},
            {"@type": "PropertyValue", "propertyID": "CAGE", "name": "CAGE Code", "value": ent["cage"]},
        ],
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "Contracting",
            "email": ent["email"],
            "telephone": ent["phone_e164"],
        },
    }
    links = "\n".join(f'<link rel="stylesheet" href="{e(c)}">' for c in css)
    cls = f' class="{html_class}"' if html_class else ""
    return f"""<!doctype html>
<html lang="en"{cls}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(canonical)}">
<meta name="theme-color" content="#0F0E0C">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(ent["legal_name"])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(canonical)}">
<meta property="og:image" content="{e(logo)}">
<meta name="twitter:card" content="summary">
<link rel="icon" type="image/png" href="assets/vac-logo.png">
<link rel="preload" href="assets/fonts/bebas-neue-400.woff2" as="font" type="font/woff2" crossorigin>
{links}
<script type="application/ld+json">{json.dumps(ld, separators=(",", ":"))}</script>
</head>
"""


def lockup(ent: dict, href: str) -> str:
    return (
        f'<a class="lockup" href="{e(href)}">'
        f'<img src="assets/vac-logo.png" alt="{e(ent["legal_name"])} logo" width="40" height="40">'
        f'<span><span class="lockup-name">{e(ent["wordmark"]).upper()}</span>'
        f'<span class="lockup-tag">{e(ent["tagline"])}</span></span></a>'
    )


def naics_badges(ent: dict) -> str:
    out = []
    for code in ent["naics"]:
        if code == ent["primary_naics"]:
            out.append(badge(f"{code} Primary", cert=True))
        else:
            out.append(badge(code))
    return f'<div class="code-list">{"".join(out)}</div>'


def build_index(v: dict) -> str:
    ent, site, cp, pr = v["entity"], v["site"], v["copy"], v["principal"]
    pdf = "assets/VAC_CapabilityStatement.pdf"
    place = f'{ent["city"]}, {ent["state_name"]}'
    badges = "".join(badge(b["text"], b["cert"]) for b in cp["badges"])
    psc = '<div class="code-list">' + "".join(badge(p) for p in ent["psc"]) + "</div>"
    direction = f'<p class="direction">{e(cp["direction"])}</p>' if cp.get("show_direction") else ""
    rows = "\n".join(
        [
            row("Legal name", e(ent["legal_name"])),
            row("UEI · CAGE", f'{e(ent["uei"])} · {e(ent["cage"])}'),
            row("SAM.gov", f'{e(ent["sam_status"])} · registration expires {e(fmt_date(ent["sam_expiration"]))}'),
            row("Certifications", f'{e(ent["certifications"])} (active, renewal {e(fmt_date(ent["cert_renewal"]))})'),
            row("DLA DIBBS", f'{e(ent["dibbs"])} under CAGE {e(ent["cage"])}'),
            row("NAICS (SAM.gov)", naics_badges(ent)),
            row("PSC (SAM.gov)", psc),
            row("Sourcing", e(ent["sourcing"])),
            row("Location", f'{e(place)} ({e(ent["region_note"])})'),
        ]
    )
    return (
        head(v, title=site["title"], description=site["description"], canonical=site["url"], css=["assets/site.css"])
        + f"""<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
<div class="wrap">
{lockup(ent, "#top")}
<div class="header-right">
<div class="ids"><span>UEI <b>{e(ent["uei"])}</b></span><span>CAGE <b>{e(ent["cage"])}</b></span></div>
<nav class="nav" aria-label="Primary">
<a href="#capabilities">Capabilities</a>
<a href="#data">Company Data</a>
<a href="#contact">Contact</a>
</nav>
</div>
</div>
</header>

<main id="main">
<section class="hero" id="top">
<div class="wrap">
<div class="badges">{badges}</div>
<h1>{e(cp["headline"])}</h1>
<p class="sub">{e(cp["subhead"])}</p>
<div class="btn-row">
<a class="btn primary" href="{pdf}">{e(cp["cta_primary"])}</a>
<a class="btn" href="mailto:{e(ent["email"])}">{e(cp["cta_secondary"])}</a>
</div>
</div>
</section>

<section class="tiles" aria-label="Identifiers">
<div class="wrap">
<div class="tile-grid">
<div class="tile wide"><span class="value">{e(ent["uei"])}</span><span class="label">UEI</span></div>
<div class="tile"><span class="value">{e(ent["cage"])}</span><span class="label">CAGE Code</span></div>
<div class="tile"><span class="value">{e(ent["primary_naics"])}</span><span class="label">Primary NAICS</span></div>
<div class="tile wide"><span class="value red">{e(ent["cert_short"])}</span><span class="label">SBA Certified · Renewal {e(fmt_date(ent["cert_renewal"]))}</span></div>
</div>
</div>
</section>

<section class="section" id="capabilities">
<div class="wrap">
<h2>Core Competencies</h2>
<div class="card-grid">
{cards(cp["competencies"])}
</div>
</div>
</section>

<section class="section alt" id="differentiators">
<div class="wrap">
<h2>Differentiators</h2>
<div class="diff-grid">
{diffs(cp["differentiators"])}
</div>
{direction}
</div>
</section>

<section class="section" id="data">
<div class="wrap">
<h2>Company Data</h2>
<dl class="data">
{rows}
</dl>
</div>
</section>

<section class="section alt" id="leadership">
<div class="wrap">
<h2>Leadership</h2>
<div class="leader">
<span class="name">{e(pr["name"])}, {e(pr["title"])}</span>
<span class="label service">{e(pr["service"])}</span>
<span class="role">{e(pr["role"])}</span>
</div>
</div>
</section>

<section class="section contact" id="contact">
<div class="wrap">
<div class="contact-lines">
<h2>Contracting Contact</h2>
<a class="contact-email" href="mailto:{e(ent["email"])}">{e(ent["email"])}</a>
<span class="contact-meta">{e(ent["phone"])} · {e(place)}</span>
</div>
<a class="btn primary" href="{pdf}">Download Capability Statement</a>
</div>
</section>
</main>

<footer class="site-footer">
<div class="wrap">
<span>© {e(site["copyright_year"])} {e(ent["legal_name"])}</span>
<span>{e(ent["certifications"])} · UEI {e(ent["uei"])} · CAGE {e(ent["cage"])}</span>
</div>
</footer>
</body>
</html>
"""
    )


def build_statement(v: dict) -> str:
    ent, site, cp, pr = v["entity"], v["site"], v["copy"], v["principal"]
    place = f'{ent["city"]}, {ent["state_name"]}'
    stamp = fmt_date(site["statement_date"])
    pdf = "assets/VAC_CapabilityStatement.pdf"
    naics = " ".join(
        f"<b>{e(c)} (primary)</b>" if c == ent["primary_naics"] else e(c) for c in ent["naics"]
    )
    psc = " ".join(e(p) for p in ent["psc"])
    direction = f'<p class="direction">{e(cp["direction"])}</p>' if cp.get("show_direction") else ""
    rows = "\n".join(
        [
            row("SAM.gov", f'{e(ent["sam_status"])} · registration expires {e(fmt_date(ent["sam_expiration"]))} · DLA DIBBS {e(ent["dibbs"]).lower()}'),
            row("Certifications", f'{e(ent["certifications"])} (active, renewal {e(fmt_date(ent["cert_renewal"]))})'),
            row("NAICS (SAM.gov)", f'<span class="codes-inline">{naics}</span>'),
            row("PSC (SAM.gov)", f'<span class="codes-inline">{psc}</span>'),
            row("Sourcing", e(ent["sourcing"])),
        ]
    )
    title = f'Capability Statement | {ent["legal_name"]}'
    return (
        head(
            v,
            title=title,
            description=site["description"],
            canonical=site["url"] + "capability-statement.html",
            css=["assets/site.css", "assets/capstmt.css"],
            html_class="cs",
        )
        + f"""<body>
<div class="screen-bar">
<a class="btn" href="index.html">Back to site</a>
<a class="btn primary" href="{pdf}">Download PDF</a>
</div>
<main class="sheet">
<header class="band">
<div class="band-top">
{lockup(ent, "index.html")}
<div class="doc-title"><div class="t">CAPABILITY STATEMENT</div><div class="label d">{e(stamp)}</div></div>
</div>
<div class="band-tiles">
<div class="tile"><span class="value">{e(ent["uei"])}</span><span class="label">UEI</span></div>
<div class="tile"><span class="value">{e(ent["cage"])}</span><span class="label">CAGE Code</span></div>
<div class="tile"><span class="value">{e(ent["primary_naics"])}</span><span class="label">Primary NAICS</span></div>
<div class="tile"><span class="value cream">{e(ent["cert_short"])}</span><span class="label">SBA Certified</span></div>
<div class="tile"><span class="value cream">{e(ent["sam_status"])}</span><span class="label">SAM.gov · to {e(fmt_date(ent["sam_expiration"]))}</span></div>
</div>
</header>

<div class="body">
<section>
<h2>Company Overview</h2>
<p class="overview">{e(cp["overview"])}</p>
</section>

<section>
<h2>Core Competencies</h2>
<div class="card-grid">
{cards(cp["competencies"])}
</div>
</section>

<section>
<h2>Differentiators</h2>
<div class="diff-grid">
{diffs(cp["differentiators"])}
</div>
{direction}
</section>

<section>
<h2>Company Data</h2>
<dl class="data">
{rows}
</dl>
</section>

<div class="bottom">
<section>
<h2>Leadership</h2>
<div class="leader">
<span class="name">{e(pr["name"])}, {e(pr["title"])}</span>
<span class="label service">{e(pr["service"])}</span>
<span class="role">{e(pr["role"])}</span>
</div>
</section>
<section>
<h2>Contracting Contact</h2>
<div class="contact-lines">
<a class="contact-email" href="mailto:{e(ent["email"])}">{e(ent["email"])}</a>
<span class="contact-meta">{e(ent["phone"])} · {e(place)} · victoryarmscompany.com</span>
</div>
</section>
</div>

<div class="foot">
<span>{e(ent["legal_name"])} · {e(ent["certifications"])}</span>
<span>UEI {e(ent["uei"])} · CAGE {e(ent["cage"])} · {e(stamp)}</span>
</div>
</div>
</main>
</body>
</html>
"""
    )


def main() -> int:
    v = json.loads((ROOT / "data" / "vac.json").read_text(encoding="utf-8"))
    ent, site = v["entity"], v["site"]
    if ent["primary_naics"] not in ent["naics"]:
        print("error: primary NAICS is not in the NAICS list", file=sys.stderr)
        return 1
    out = {
        "index.html": build_index(v),
        "capability-statement.html": build_statement(v),
        "robots.txt": f"User-agent: *\nAllow: /\n\nSitemap: {site['url']}sitemap.xml\n",
        "sitemap.xml": (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"  <url><loc>{site['url']}</loc><lastmod>{site['statement_date']}</lastmod></url>\n"
            f"  <url><loc>{site['url']}capability-statement.html</loc><lastmod>{site['statement_date']}</lastmod></url>\n"
            f"  <url><loc>{site['url']}assets/VAC_CapabilityStatement.pdf</loc><lastmod>{site['statement_date']}</lastmod></url>\n"
            "</urlset>\n"
        ),
    }
    for name, text in out.items():
        (ROOT / name).write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {name} ({len(text)} bytes)")
    print(f"dated PDF name: assets/VAC_CapabilityStatement_{compact(site['statement_date'])}.pdf")
    return 0


if __name__ == "__main__":
    sys.exit(main())
