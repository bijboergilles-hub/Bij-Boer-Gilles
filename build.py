#!/usr/bin/env python3
"""Bouwt de site: src/pages/*.html + src/layout.html + src/data.json -> docs/.

Elke pagina begint met kopregels (sleutel: waarde) tot een regel '---'.
{{sleutel}} wordt vervangen door de waarde uit data.json of de kopregels.
Prijzen en gegevens staan dus maar op één plek: src/data.json.
"""
import json, re, pathlib, datetime

ROOT = pathlib.Path(__file__).parent
SRC, OUT = ROOT / "src", ROOT / "docs"
data = json.loads((SRC / "data.json").read_text(encoding="utf-8"))
layout = (SRC / "layout.html").read_text(encoding="utf-8")
NAV = ["kampen", "feestjes", "bezoek", "scholen", "groepen", "workshops", "over"]


def fill(text, values):
    def rep(m):
        k = m.group(1)
        if k not in values:
            raise KeyError(f"onbekende sleutel {{{{{k}}}}}")
        return values[k]
    return re.sub(r"\{\{(\w+)\}\}", rep, text)


urls = []
for page in sorted((SRC / "pages").glob("*.html")):
    raw = page.read_text(encoding="utf-8")
    head, body = raw.split("\n---\n", 1)
    meta = dict(l.split(": ", 1) for l in head.strip().splitlines())
    values = dict(data)
    path = "" if page.stem == "index" else page.name
    values.update(
        page_title=meta["title"],
        page_description=meta["description"],
        page_image=meta.get("image", "hero-groep-kippen"),
        page_path=path,
        page_head=meta.get("head", ""),
    )
    for n in NAV:
        values[f"cur_{n}"] = ' aria-current="page"' if meta.get("nav") == n else ""
    values["content"] = fill(body, values)
    (OUT / page.name).write_text(fill(layout, values), encoding="utf-8")
    if meta.get("sitemap", "ja") == "ja":
        urls.append(f"{data['site_url']}/{path}")

today = datetime.date.today().isoformat()
(OUT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls)
    + "</urlset>\n", encoding="utf-8")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {data['site_url']}/sitemap.xml\n")
print(f"{len(urls)} pagina's gebouwd")
