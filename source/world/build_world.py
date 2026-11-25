#!/usr/bin/env python3
"""Builds the Founder's Office portfolio into world/dist/ from world/site_content.py.
One content source feeds the 3D journey (templates) and the no-3D fallback (stacked list).
Usage: python3 world/build_world.py"""
import html, json, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_content import LINKS, HERO, CHAPTERS, CASES  # noqa: E402

E = html.escape
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "world" / "dist"
NAME = "Sri Krishna Taak"
TITLE = "Sri Krishna Taak | Founder's Office internship, March to May 2027"
DESC = ("Sri Krishna Taak builds the first version, brings people together and moves the work forward: "
        "ResumeFit, CaseUnion 4.0, field work from Cairo to Rajasthan. A train journey through the work.")
N = len(CHAPTERS)

LOGOFILES = {"niti": "niti.png", "harvard": "harvard.svg", "mu": "mu.png", "akshaya": "akshaya.png", "telangana": "telangana.svg", "aiesec": "aiesec.jpg", "icon": "icon.jpg", "jagriti": "jagriti.webp", "iift": "iift.png", "rotaract": "rotaract.png", "iima": "iima.png", "nitw": "nitw.png", "iitgn": "iitgn.png", "svnit": "svnit.png", "tie": "tie.png", "sristi": "sristi.png", "iis": "iis.png"}
LOGONAMES = {"niti": "NITI Aayog", "harvard": "Harvard (HPAIR conference)", "mu": "Masters' Union", "akshaya": "The Akshaya Patra Foundation",
             "telangana": "Government of Telangana", "aiesec": "AIESEC", "icon": "Icon Creations", "ted": "TEDx", "jagriti": "Jagriti Yatra", "iift": "IIFT Delhi", "rotaract": "Rotaract", "iima": "IIM Ahmedabad", "nitw": "NIT Warangal", "iitgn": "IIT Gandhinagar", "svnit": "SVNIT Surat", "tie": "TiE Ahmedabad", "sristi": "SRISTI", "iis": "Indian Institute of Sustainability"}
LABELS = (("Result", "r"), ("Action", "a"), ("Context", "c"))


def logo_tile(k):
    if k == "ted":
        return '<span class="lg tx" role="img" aria-label="TEDx">TED<i>x</i></span>'
    return f'<span class="lg"><img src="assets/logos/{E(LOGOFILES[k])}" alt="{E(LOGONAMES[k])}" height="30"></span>'


def link(label, href, new=True):
    if not href:
        return ""
    if href.startswith("http"):
        return f'<li><a class="chip" href="{E(href)}" target="_blank" rel="noopener noreferrer">{E(label)}<span class="sr"> (opens in a new tab)</span></a></li>'
    return f'<li><a class="chip" href="{E(href)}">{E(label)}</a></li>'


def figure(f, cls=""):
    return (f'<figure class="{cls}"><img src="{E(f["src"])}" alt="{E(f["alt"])}" loading="lazy" decoding="async">'
            f'<figcaption>{E(f["cap"])}</figcaption></figure>')


def rac(it):
    return '<dl class="rac">' + "".join(f'<div><dt>{lab}</dt><dd>{E(it[k])}</dd></div>' for lab, k in LABELS) + "</dl>"


def item_body(it, fallback=False):
    out = [rac(it)]
    if it.get("thumb"):
        t = it["thumb"]
        out.append(f'<figure class="thumb"><img src="{E(t["src"])}" alt="{E(t["alt"])}" width="132" height="92" decoding="async"{"" if not fallback else " loading=lazy"}><figcaption>{E(t["cap"])}</figcaption></figure>')
    tail = ""
    if it.get("quote"):
        q = it["quote"]
        tail += (f'<figure class="quote"><blockquote>&ldquo;{E(q["text"])}&rdquo;</blockquote>'
                 f'<figcaption><b>{E(q["name"])}</b> {E(q["role"])} <a href="{E(q["url"])}" target="_blank" rel="noopener">LinkedIn recommendation<span class="sr"> (opens in a new tab)</span></a></figcaption></figure>')
    if it.get("proof"):
        tail += '<ul class="proof">' + "".join(link(l, h) for l, h in it["proof"]) + "</ul>"
    if it.get("src"):
        tail += f'<p class="src">{E(it["src"])}</p>'
    if it.get("more") and not fallback:
        tail += f'<p class="cact"><button type="button" class="btn big" data-case="{E(it["more"])}">More detail</button></p>'
    out.append(f'<div class="cmeta">{tail}</div>')
    return "".join(out)


def card_html(ch):
    a, b = ch["stamp"]
    items = ch["items"]
    head = (f'<header class="chead"><p class="kicker mono">{ch["n"]:02d} · {E(ch["label"])} · {E(ch["year"])}</p>'
            f'<span class="stamp" aria-hidden="true"><b>{E(a)}</b><i>{E(b)}</i></span></header>'
            f'<h2 class="ctitle" tabindex="-1">{E(ch["title"])}</h2>')
    if ch.get("contact"):
        it = items[0]
        links = (f'<li><a class="chip big" href="mailto:{E(LINKS["email"])}">Email me</a></li>' + link("LinkedIn", LINKS["linkedin"]) +
                 link("GitHub", LINKS["github"]) + link("Product Hunt", LINKS["ph_profile"]))
        return head + f'<div class="item open"><p class="lede">{E(it["r"])}</p><p>{E(it["a"])}</p><p>{E(it["c"])}</p></div><ul class="proof">{links}</ul>'
    if len(items) == 1:
        it = items[0]
        logos = "".join(logo_tile(k) for k in it.get("logos", []))
        top = f'<p class="iwhen mono">{E(it["when"])}</p>' + (f'<div class="logos">{logos}</div>' if logos else "")
        return head + f'<div class="item open">{top}{item_body(it)}</div>'
    parts = []
    for i, it in enumerate(items):
        logos = "".join(logo_tile(k) for k in it.get("logos", []))
        op = i == 0
        parts.append(
            f'<div class="item{" open" if op else ""}"><button type="button" class="ih" aria-expanded="{"true" if op else "false"}">'
            f'<span class="in">{logos}{E(it["name"])}</span><span class="iw mono">{E(it["when"])}</span></button>'
            f'<div class="ib">{item_body(it)}</div></div>')
    return head + '<div class="items">' + "".join(parts) + "</div>"


def case_html(cid, prefix):
    c = CASES[cid]
    meta = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in c["meta"])
    out = [f'<article class="case" id="{prefix}{cid}"><header><p class="mono">Detail</p><h2 class="cs-title" tabindex="-1">{E(c["title"])}</h2><dl class="meta">{meta}</dl></header>',
           f'<p class="lead">{E(c["lead"])}</p>']
    for b in c["blocks"]:
        if "h" in b:
            out.append(f'<h3>{E(b["h"])}</h3>')
        if "timeline" in b:
            out.append('<ol class="timeline">' + "".join(f'<li><b>{E(d)}</b><span>{E(t)}</span></li>' for d, t in b["timeline"]) + "</ol>")
        for t in b.get("p", []):
            out.append(f"<p>{E(t)}</p>")
        if "ul" in b:
            out.append('<ul class="rule">' + "".join(f"<li>{E(x)}</li>" for x in b["ul"]) + "</ul>")
            if b.get("note"):
                out.append(f'<p class="note">{E(b["note"])}</p>')
        if "fig" in b:
            out.append(figure(b["fig"]))
    out.append('<ul class="proof">' + "".join(link(l, h) for l, h in c["proof"]) + "</ul></article>")
    return "".join(out)


def hero_html():
    ents = "".join(f'<li><button type="button" class="chipcard" data-go="{e["go"]}"><em>{E(e["n"])}</em><b>{E(e["k"])}</b><span>{E(e["v"])}</span></button></li>' for e in HERO["entries"])
    return f"""<div class="h-in">
      <p class="mono h-k">{E(HERO['kicker'])}</p>
      <h1 class="h-h1">{E(HERO['h1'])}</h1>
      <p class="h-sub">{E(HERO['sub'])}</p>
      <ul class="chips" aria-label="Start with one kind of work">{ents}</ul>
      <p class="h-act"><button class="btn big" type="button" data-go="{HERO['start']['go']}" id="bExplore">{E(HERO['start']['label'])}</button><a class="btn big h-mail" href="mailto:{E(LINKS['email'])}">Email me</a></p>
    </div>
    <figure class="h-photo"><img src="{E(HERO['photo']['src'])}" alt="{E(HERO['photo']['alt'])}" width="480" height="320"><figcaption class="mono">{E(HERO['photo']['cap'])}</figcaption></figure>"""


def fallback_html():
    parts = []
    for ch in CHAPTERS[1:]:
        art = [f'<article id="p-{ch["id"]}"><h2><span class="mono">{ch["n"]:02d} · {E(ch["label"])} · {E(ch["year"])}</span><br>{E(ch["title"])}</h2>']
        for it in ch["items"]:
            logos = "".join(logo_tile(k) for k in it.get("logos", []))
            art.append(f'<section class="pitem"><h3>{E(it["name"])} <span class="mono">{E(it["when"])}</span></h3>' + (f'<div class="logos">{logos}</div>' if logos else "") + item_body(it, True).replace('<p class="cact">', '<p class="cact" hidden>') + "</section>")
            if it.get("more"):
                art.append(f'<details class="pcase" open><summary>Detail: {E(CASES[it["more"]]["title"])}</summary>{case_html(it["more"], "plain-case-")}</details>')
        if ch.get("contact"):
            art.append('<ul class="proof">' + f'<li><a class="chip big" href="mailto:{E(LINKS["email"])}">{E(LINKS["email"])}</a></li>' + link("LinkedIn", LINKS["linkedin"]) + link("GitHub", LINKS["github"]) + link("Product Hunt", LINKS["ph_profile"]) + "</ul>")
        art.append("</article>")
        parts.append("".join(art))
    return "".join(parts)


def main():
    chapters = [dict(id=c["id"], n=c["n"], label=c["label"], title=c.get("title", NAME), year=c["year"], board=c["board"], sub=c["sub"],
                     country=c["country"], mon=c["mon"], logos=c["logos"], biome=c["biome"]) for c in CHAPTERS]
    data = dict(chapters=chapters, logos=LOGOFILES, logoNames=LOGONAMES)
    templates = [f'<template id="t-{c["id"]}">{card_html(c)}</template>' for c in CHAPTERS[1:]]
    templates += [f'<template id="c-{cid}">{case_html(cid, "case-")}</template>' for cid in CASES]
    index_items = "".join(f'<li><button type="button" data-go="{c["n"]}"><b>{c["n"]:02d}</b><span>{E(c["label"])}<small>{E(c["year"])}</small></span></button></li>' for c in CHAPTERS)
    ld = json.dumps({"@context": "https://schema.org", "@type": "Person", "name": NAME, "url": LINKS["site"],
                     "sameAs": [LINKS["linkedin"], LINKS["github"], LINKS["ph_profile"]],
                     "alumniOf": {"@type": "Organization", "name": "Masters' Union"}}, ensure_ascii=False)
    page = f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(TITLE)}</title>
<meta name="description" content="{E(DESC)}">
<link rel="canonical" href="{E(LINKS['site'])}">
<meta name="theme-color" content="#0b1d3a">
<meta property="og:type" content="website"><meta property="og:site_name" content="{E(NAME)}">
<meta property="og:title" content="{E(TITLE)}"><meta property="og:description" content="{E(DESC)}">
<meta property="og:url" content="{E(LINKS['site'])}"><meta property="og:image" content="{E(LINKS['site'])}assets/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Sri Krishna Taak: I build the first version, bring people together, and move the work forward, with a train on a rail line">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(TITLE)}"><meta name="twitter:description" content="{E(DESC)}"><meta name="twitter:image" content="{E(LINKS['site'])}assets/og.png">
<link rel="preload" href="assets/fonts/inter-tight-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/css/world.css">
<script type="application/ld+json">{ld}</script>
<script>document.documentElement.className='js'</script>
</head>
<body>
<canvas id="gl" aria-hidden="true"></canvas>
<div class="vig" aria-hidden="true"></div>
<div class="cut" id="cut" aria-hidden="true"></div>
<div class="hud intro" id="hud" hidden>
  <header class="bar">
    <a class="logo" href="#start" data-go="0" aria-label="{E(NAME)}, back to the start">SKT<span>.</span></a>
    <nav class="btns" aria-label="Site controls">
      <button type="button" id="bIndex" aria-expanded="false" aria-controls="index">Stations</button>
      <button type="button" id="bSound" aria-pressed="false"><span class="m-hide">Train&nbsp;</span><span id="sndTxt">sound: off</span></button>
      <a class="solid" id="bResume" href="resume.pdf" target="_blank" rel="noopener">View r&eacute;sum&eacute;<span class="sr"> (PDF, opens in a new tab)</span></a>
    </nav>
  </header>
  <nav class="index" id="index" aria-label="Stations" hidden><ol>{index_items}</ol></nav>
  <section class="hero" id="hero" aria-label="Introduction">{hero_html()}</section>
  <section class="card" id="card" aria-label="Station"></section>
  <nav class="pager" id="pager" aria-label="Journey"><button type="button" id="bPrev" aria-label="Previous station">&#8592;<span> Previous</span></button><p class="pcount mono" id="pcount" aria-hidden="true"></p><button type="button" id="bNext" aria-label="Next station"><span>Next </span>&#8594;</button></nav>
  <div class="hintline mono" id="hintline" aria-hidden="true">Scroll, swipe or press &#8594; to ride one stop</div>
  <div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-label="More detail" hidden><div class="sheet-in"><button type="button" class="sheet-x btn" id="sheetX">Close</button><div id="sheetBody"></div></div></div>
</div>
<p class="sr" id="live" role="status" aria-live="polite"></p>
<main id="plain" class="plain" tabindex="-1">
  <header><h1>{E(NAME)}</h1>
  <p class="lead">{E(HERO['h1'])}</p><p>{E(HERO['sub'])}</p>
  <p><a class="btn big" href="mailto:{E(LINKS['email'])}">Email me</a> <a class="btn" href="resume.pdf" target="_blank" rel="noopener">View r&eacute;sum&eacute;</a></p></header>
  {fallback_html()}
  <footer><p>An independent portfolio by {E(NAME)}. Figures come from my r&eacute;sum&eacute; unless a source is linked or named beside the claim.</p></footer>
</main>
{"".join(templates)}
<script>window.YATRA={json.dumps(data, ensure_ascii=False)};</script>
<script src="assets/vendor/three.min.js"></script>
<script src="assets/js/world.js"></script>
</body></html>"""
    if OUT.exists():
        shutil.rmtree(OUT)
    for d in ("assets/css", "assets/js", "assets/vendor", "assets/img", "assets/logos"):
        (OUT / d).mkdir(parents=True)
    shutil.copytree(ROOT / "assets/fonts", OUT / "assets/fonts", ignore=shutil.ignore_patterns("Geist*"))
    imgs = {HERO["photo"]["src"]}
    works = set()
    for c in CHAPTERS:
        for it in c.get("items", []):
            if it.get("thumb"):
                (imgs if it["thumb"]["src"].startswith("assets/img/") else works).add(it["thumb"]["src"])
    for cs in CASES.values():
        for b in cs["blocks"]:
            if "fig" in b:
                works.add(b["fig"]["src"])
    for src in imgs | works:
        (OUT / src).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / src, OUT / src)
    for f in LOGOFILES.values():
        shutil.copy(ROOT / "assets/logos" / f, OUT / "assets/logos" / f)
    shutil.copy(ROOT / "assets/vendor/three.min.js", OUT / "assets/vendor/three.min.js")
    shutil.copy(ROOT / "world/src/world.css", OUT / "assets/css/world.css")
    shutil.copy(ROOT / "world/src/world.js", OUT / "assets/js/world.js")
    for extra in ("favicon.svg", "og.png"):
        if (ROOT / "world/src" / extra).exists():
            shutil.copy(ROOT / "world/src" / extra, OUT / "assets" / extra)
    (OUT / "index.html").write_text(page, encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    shutil.copy(ROOT / "content/resumes/Sri_Krishna_Main_Resume.pdf", OUT / "resume.pdf")
    print("built ->", OUT)


if __name__ == "__main__":
    main()
