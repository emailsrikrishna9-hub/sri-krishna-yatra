#!/usr/bin/env python3
"""Builds the Founder's Office portfolio into world/dist/ from world/site_content.py.
One content source feeds the 3D journey (templates) and the no-3D fallback (stacked list).
Usage: python3 world/build_world.py"""
import html, json, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_content import LINKS, HERO, CHAPTERS, CASES, ALLWORK  # noqa: E402

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
LABELS = (("The win", "r"), ("My move", "a"), ("Backdrop", "c"))


LOGOURLS = {"icon": "https://icon-creations.com/", "telangana": "https://www.telangana.gov.in/", "aiesec": "https://www.aiesec.in/",
            "ted": "https://www.ted.com/tedx", "iis": "https://www.gujaratuniversity.ac.in/", "sristi": "https://www.sristi.org/",
            "akshaya": "https://www.akshayapatra.org/", "niti": "https://www.niti.gov.in/", "iima": "https://www.iima.ac.in/",
            "harvard": "https://www.hpair.org/", "mu": "https://mastersunion.org/", "jagriti": "https://www.jagritiyatra.com/",
            "iift": "https://www.iift.ac.in/", "rotaract": "https://www.rotary.org/en/get-involved/rotaract-clubs",
            "nitw": "https://www.nitw.ac.in/", "iitgn": "https://iitgn.ac.in/", "svnit": "https://www.svnit.ac.in/",
            "tie": "https://ahmedabad.tie.org/"}


def logo_tile(k):
    """A logo that opens the organisation's website. Never place it inside a button."""
    name = LOGONAMES[k]
    inner = 'TED<i>x</i>' if k == "ted" else f'<img src="assets/logos/{E(LOGOFILES[k])}" alt="" height="30">'
    cls = "lg tx" if k == "ted" else "lg"
    return (f'<a class="{cls}" href="{E(LOGOURLS[k])}" target="_blank" rel="noopener noreferrer" '
            f'title="{E(name)} website" aria-label="{E(name)} website (opens in a new tab)">{inner}</a>')


def board_html():
    """Every piece of work with its organisation and one line on what was done; each tile jumps to its stop."""
    groups = []
    for title, rows in ALLWORK["groups"]:
        tiles = []
        for logo, name, did, when, go in rows:
            mark = logo_tile(logo) if logo else f'<span class="lg tx" aria-hidden="true">{E(name[0])}</span>'
            tiles.append(f'<li class="wl">{mark}<button type="button" class="wt" data-go="{go}"><span><b>{E(name)}</b>'
                         f'<span class="wd">{E(did)}</span><small class="mono">{E(when)}</small></span></button></li>')
        groups.append(f'<section class="wg"><h3 class="mono">{E(title)}</h3><ul>{"".join(tiles)}</ul></section>')
    also = "".join(logo_tile(k) for k in ALLWORK["also"])
    return (f'<p class="wnote">{E(ALLWORK["note"])}</p><div class="board">{"".join(groups)}</div>'
            f'<div class="walso"><span class="mono">Also along the way</span>{also}</div>')


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
        qlink = (f' <a href="{E(q["url"])}" target="_blank" rel="noopener">LinkedIn recommendation<span class="sr"> (opens in a new tab)</span></a>' if q.get("url") else "")
        tail += (f'<figure class="quote"><blockquote>&ldquo;{E(q["text"])}&rdquo;</blockquote>'
                 f'<figcaption><b>{E(q["name"])}</b> {E(q["role"])}{qlink}</figcaption></figure>')
    if it.get("proof"):
        tail += '<ul class="proof">' + "".join(link(l, h) for l, h in it["proof"]) + "</ul>"
    if it.get("src"):
        tail += f'<p class="src">{E(it["src"])}</p>'
    if it.get("letter") and not fallback:
        tail += f'<p class="cact"><button type="button" class="btn big" data-case="letter-{E(it["letter"]["id"])}">{E(it["letter"]["btn"])}</button></p>'
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
        return (head + f'<div class="item open"><p class="lede">{E(it["r"])} {E(it["a"])}</p></div><ul class="proof">{links}</ul>'
                f'<h3 class="wtitle">{E(ALLWORK["title"])}</h3>' + board_html())
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
            f'<div class="item{" open" if op else ""}{" haslg" if logos else ""}">' + (f'<span class="hlg">{logos}</span>' if logos else "") + f'<button type="button" class="ih" aria-expanded="{"true" if op else "false"}">'
            f'<span class="in">{E(it["name"])}</span><span class="iw mono">{E(it["when"])}</span></button>'
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


def letters():
    return [it["letter"] for c in CHAPTERS for it in c.get("items", []) if it.get("letter")]


def letter_html(l):
    return (f'<article class="case letter"><header><p class="mono">Proof</p><h2 class="cs-title" tabindex="-1">{E(l["title"])}</h2></header>'
            f'<p>{E(l["cap"])}</p><figure><img src="assets/proof/{E(l["id"])}.jpg" alt="{E(l["title"])}"></figure></article>')


def hero_html():
    pics = "".join(f'<li><button type="button" class="hpic" data-go="{p["go"]}"><img src="{E(p["src"])}" alt="{E(p["alt"])}" style="object-position:{E(p["pos"])}"><span>{E(p["cap"])}</span></button></li>' for p in HERO["photos"])
    nums = "".join(f'<li><button type="button" class="hnum" data-go="{e["go"]}"><b>{E(e["n"])}</b> {E(e["k"])}</button></li>' for e in HERO["entries"])
    return f"""<div class="h-in">
      <p class="mono h-k">{E(HERO['kicker'])}</p>
      <h1 class="h-h1">{E(HERO['h1'])}</h1>
      <p class="h-sub">{E(HERO['sub'])}</p>
      <ul class="h-pics" aria-label="Moments from the work">{pics}</ul>
      <ul class="h-nums" aria-label="Highlights">{nums}</ul>
      <p class="h-act"><button class="btn big" type="button" data-go="{HERO['start']['go']}" id="bExplore">{E(HERO['start']['label'])}</button><button class="btn big h-mail" type="button" data-go="{HERO['all']['go']}">{E(HERO['all']['label'])}</button><a class="btn big h-mail" href="mailto:{E(LINKS['email'])}">Email me</a></p>
    </div>"""


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
            art.append(f'<p>{E(ALLWORK["note"])}.</p>')
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
    templates += [f'<template id="c-letter-{l["id"]}">{letter_html(l)}</template>' for l in letters()]
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
  <div class="hintline mono" id="hintline" aria-hidden="true">Scroll, swipe or press &#8594; to see each experience</div>
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
    imgs = {p["src"] for p in HERO["photos"] if p["src"].startswith("assets/img/")}
    works = set()
    for c in CHAPTERS:
        for it in c.get("items", []):
            if it.get("thumb"):
                (imgs if it["thumb"]["src"].startswith("assets/img/") else works).add(it["thumb"]["src"])
    for cs in CASES.values():
        for b in cs["blocks"]:
            if "fig" in b:
                works.add(b["fig"]["src"])
    works |= {p["src"] for p in HERO["photos"] if not p["src"].startswith("assets/img/")}
    works |= {f"assets/proof/{l['id']}.jpg" for l in letters()}
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
