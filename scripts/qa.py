#!/usr/bin/env python3
"""QA gate for the VAC government site. Python 3.11+ standard library only.

Usage:  python3 scripts/qa.py      (exit 0 = all checks pass)

This file and docs/ are excluded from the forbidden-term scan because they must name the terms.
assets/fonts/OFL.txt is excluded because it is verbatim license text.
"""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT_EXT = {".html", ".css", ".json", ".xml", ".txt", ".md", ".py", ".yml", ""}
SKIP_DIRS = {".git", "docs"}
SKIP_FILES = {"scripts/qa.py", "scripts/hooks/pre-commit", "assets/fonts/OFL.txt"}

FORBIDDEN = [
    r"Ret\.", r"retired", r"former Marine", r"ex-Marine", r"CVE", r"Delaware", r"GSS26043",
    r"victoryweaponstraining", r"Victory Weapons Training", r"USCCA", r"concealed",
    r"fonts\.googleapis", r"fonts\.gstatic", r"cdn", r"gtag", r"SOI", r"Company H", r"commander",
    r"MOS", r"Wirgman", r"rounds", r"Marines trained", r"\b\d{2}-\d{7}\b",
    r"quartermaster", r"pathfinder", r"sigint", r"googletagmanager", r"fbq\(", r"SAM-[0-9a-f]{8}-",
]
TOKENS = {"#0F0E0C", "#1A1814", "#25221C", "#38342C", "#EFE5C6", "#B3A98F", "#CFAE55", "#B3121C", "#4F8A5B", "#7A776F"}
VOID = {"meta", "link", "img", "br", "hr", "input"}

fails: list[str] = []


def check(ok: bool, msg: str) -> None:
    print(("PASS  " if ok else "FAIL  ") + msg)
    if not ok:
        fails.append(msg)


def shipped_text_files() -> list[Path]:
    out = []
    for p in sorted(ROOT.rglob("*")):
        rel = p.relative_to(ROOT).as_posix()
        if not p.is_file() or any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        if rel in SKIP_FILES or p.suffix.lower() not in TEXT_EXT or p.name == "CNAME":
            continue
        out.append(p)
    return out


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.errors: list[str] = []
        self.links: list[str] = []
        self.srcs: list[str] = []
        self.ids: set[str] = set()
        self.text: list[str] = []
        self.scripts = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if tag == "link" and "href" in a and a.get("rel") != "canonical":
            self.srcs.append(a["href"])
        if tag in ("img", "script") and "src" in a:
            self.srcs.append(a["src"])
        if tag == "script" and a.get("type") != "application/ld+json":
            self.scripts += 1
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"unbalanced </{tag}> (open: {self.stack[-3:]})")
        else:
            self.stack.pop()

    def handle_data(self, data):
        self.text.append(data)


def main() -> int:
    v = json.loads((ROOT / "data" / "vac.json").read_text(encoding="utf-8"))
    ent = v["entity"]

    # 1. forbidden terms
    hits = []
    for p in shipped_text_files():
        body = p.read_text(encoding="utf-8", errors="replace")
        for pat in FORBIDDEN:
            for m in re.finditer(pat, body, flags=re.IGNORECASE):
                line = body.count("\n", 0, m.start()) + 1
                hits.append(f"{p.relative_to(ROOT).as_posix()}:{line}: /{pat}/ -> {m.group(0)!r}")
    for h in hits:
        print("      " + h)
    check(not hits, f"forbidden-term scan: {len(hits)} hits across {len(shipped_text_files())} shipped text files")

    # 2. CSS colors
    bad = []
    for css in sorted((ROOT / "assets").glob("*.css")):
        for m in re.finditer(r"#[0-9A-Fa-f]{3,8}\b", css.read_text(encoding="utf-8")):
            if m.group(0).upper() not in TOKENS:
                bad.append(f"{css.name}: {m.group(0)}")
        body = css.read_text(encoding="utf-8")
        for pat in (r"rgba?\(", r"hsla?\(", r"gradient\(", r"@import", r"https?://"):
            if re.search(pat, body):
                bad.append(f"{css.name}: /{pat}/")
    check(not bad, "CSS uses only the ten locked tokens; no gradients, imports or remote URLs " + ("" if not bad else str(bad)))

    # 3. HTML structure, links, assets
    for name in ("index.html", "capability-statement.html"):
        pg = Page()
        pg.feed((ROOT / name).read_text(encoding="utf-8"))
        check(not pg.errors and not pg.stack, f"{name}: tags balanced {pg.errors[:3]}")
        check(pg.scripts == 0, f"{name}: no JavaScript (JSON-LD only)")
        bad_links = []
        for href in pg.links:
            if href == f"mailto:{ent['email']}":
                continue
            if href.startswith("#"):
                if href[1:] not in pg.ids:
                    bad_links.append(href + " (no such id)")
                continue
            if re.match(r"^[a-z]+:", href) or href.startswith("//"):
                bad_links.append(href)
                continue
            if not (ROOT / href).is_file():
                bad_links.append(href + " (missing file)")
        check(not bad_links, f"{name}: every link is internal and resolves, or mailto:{ent['email']} {bad_links}")
        missing = [s for s in pg.srcs if re.match(r"^[a-z]+:", s) or not (ROOT / s).is_file()]
        check(not missing, f"{name}: every stylesheet, image and icon is local and present {missing}")
        text = " ".join(pg.text)
        for key in ("uei", "cage", "primary_naics", "email", "phone", "legal_name"):
            check(str(ent[key]) in text, f"{name}: shows {key} from vac.json")
        # the only 6-digit codes allowed on a page are the primary NAICS and the card codes in vac.json
        allowed = {ent["primary_naics"]} | set(re.findall(r"\b\d{6}\b", json.dumps(v["copy"])))
        six = set(re.findall(r"\b\d{6}\b", text))
        check(six <= allowed, f"{name}: no NAICS code beyond the primary and the card codes {sorted(six - allowed)}")
        for pat in (r"expir", r"renewal", r"DIBBS[- ]registered", r"registered in DLA", r"FAR 19", r"U\.S\.C\."):
            check(not re.search(pat, text, re.I), f"{name}: no /{pat}/ on the page")

    # 4. fonts and license
    fonts = sorted(p.name for p in (ROOT / "assets" / "fonts").glob("*.woff2"))
    check(len(fonts) == 4 and (ROOT / "assets" / "fonts" / "OFL.txt").is_file(), f"self-hosted fonts + OFL license present {fonts}")

    # 5. PDF
    stamp = v["site"]["statement_date"].replace("-", "")
    dated = ROOT / "assets" / f"VAC_CapabilityStatement_{stamp}.pdf"
    alias = ROOT / "assets" / "VAC_CapabilityStatement.pdf"
    check(dated.is_file() and alias.is_file(), f"PDF present: {dated.name} + stable alias")
    if dated.is_file() and alias.is_file():
        data = dated.read_bytes()
        pages = len(re.findall(rb"/Type\s*/Page\b", data))
        check(pages == 1, f"PDF is exactly 1 page (found {pages})")
        check(data == alias.read_bytes(), "alias PDF is byte-identical to the dated PDF")
        check(b"/MediaBox [0 0 612 792]" in data or b"/MediaBox[0 0 612 792]" in data, "PDF page is US Letter (612 x 792 pt)")

    # 6. SEO files
    for f in ("sitemap.xml", "robots.txt", "CNAME"):
        check((ROOT / f).is_file(), f"{f} present")

    print()
    print("RESULT: " + ("ALL PASS" if not fails else f"{len(fails)} FAILED"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
