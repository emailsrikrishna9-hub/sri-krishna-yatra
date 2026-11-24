#!/usr/bin/env python3
"""Builds the Yatra Express portfolio into world/dist/ from world/site_content.py.
One content source feeds both the 3D journey (templates) and the text route (articles).
Usage: python3 world/build_world.py"""
import html, json, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_content import LINKS, HERO, CHAPTERS, CASES, RESUMES  # noqa: E402

E = html.escape
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "world" / "dist"
NAME = "Sri Krishna Taak"
TITLE = "Sri Krishna Taak | Builder and programme lead, Summer 2027"
DESC = ("Portfolio of Sri Krishna Taak: ResumeFit (a live AI resume tool), Careers Club (40 events in 5 months), "
        "NITI Aayog policy research and more, told as a train journey with a text version. Open to Summer 2027 internships.")
N = len(CHAPTERS)

LOGOFILES = {"niti": "niti.png", "harvard": "harvard.svg", "mu": "mu.png", "iift": "iift.png", "akshaya": "akshaya.png", "jagriti": "jagriti.webp"}
LOGONAMES = {"niti": "NITI Aayog", "harvard": "Harvard", "mu": "Masters' Union", "iift": "IIFT Delhi", "akshaya": "The Akshaya Patra Foundation", "jagriti": "Jagriti Yatra", "ted": "TEDx"}

COBWEB_TPL = """<svg viewBox="0 0 620 300" role="img" aria-labelledby="@cwT @cwD" class="diagram">
<title id="@cwT">The cobweb price cycle</title><desc id="@cwD">A loop: a high price makes farmers plant more, a glut makes the price fall, farmers cut back, supply tightens and the price rises again. Reactive trade curbs feed into the loop.</desc>
<defs><marker id="@ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<g font-family="Inter Tight,Arial,sans-serif" font-size="15" font-weight="700" fill="currentColor" stroke="currentColor">
<g fill="none" stroke-width="2.4" marker-end="url(#@ar)"><path d="M214 56H400"/><path d="M500 84V150"/><path d="M400 214H214"/><path d="M110 150V84"/></g>
<g fill="var(--dg-fill,#fff)" stroke-width="2.4"><rect x="20" y="28" width="190" height="56" rx="14"/><rect x="404" y="28" width="196" height="56" rx="14"/><rect x="404" y="150" width="196" height="64" rx="14"/><rect x="20" y="150" width="190" height="64" rx="14"/></g>
<g stroke="none"><text x="115" y="62" text-anchor="middle">Price is high</text><text x="502" y="62" text-anchor="middle">Farmers plant more</text><text x="502" y="178" text-anchor="middle">Glut, price falls</text><text x="502" y="198" text-anchor="middle" font-weight="500" font-size="13">(imports can add to it)</text><text x="115" y="178" text-anchor="middle">Farmers cut back,</text><text x="115" y="198" text-anchor="middle">supply tightens</text></g>
<g fill="var(--dg-accent,#ffc83d)" stroke-width="2.4"><rect x="210" y="238" width="200" height="46" rx="23"/></g>
<g stroke="none"><text x="310" y="266" text-anchor="middle">Reactive trade curbs</text></g>
<g fill="none" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#@ar)"><path d="M250 238C190 226 150 222 130 218"/><path d="M370 238C430 226 470 222 490 218"/></g>
</g></svg>"""


def cobweb(prefix):
    return COBWEB_TPL.replace("@", prefix)


def esc_para(t):
    return f"<p>{E(t)}</p>"


def link(label, href, ext=None):
    if not href:
        return f'<li><span class="chip off">{E(label)}</span></li>'
    ext = href.startswith("http") if ext is None else ext
    attrs = ' target="_blank" rel="noopener noreferrer"' if ext else ""
    dl = " download" if href.endswith(".pdf") else ""
    return f'<li><a class="chip" href="{E(href)}"{attrs}{dl}>{E(label)}<span class="sr"> (opens in a new tab)</span></a></li>' if ext else f'<li><a class="chip" href="{E(href)}"{dl}>{E(label)}</a></li>'


def figure(f, lazy=True, cls=""):
    ld = ' loading="lazy" decoding="async"' if lazy else ""
    return (f'<figure class="{cls}"><img src="{E(f["src"])}" alt="{E(f["alt"])}"{ld}>'
            f'<figcaption>{E(f["cap"])}</figcaption></figure>')


def case_html(cid, prefix):
    c = CASES[cid]
    meta = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in c["meta"])
    out = [f'<article class="case" id="{prefix}{cid}"><header><p class="mono">Case study</p><h2 class="cs-title" tabindex="-1">{E(c["title"])}</h2><dl class="meta">{meta}</dl></header>',
           f'<p class="lead">{E(c["lead"])}</p>']
    for b in c["blocks"]:
        if "h" in b:
            out.append(f'<h3>{E(b["h"])}</h3>')
        if "timeline" in b:
            out.append('<ol class="timeline">' + "".join(f'<li><b>{E(d)}</b><span>{E(t)}</span></li>' for d, t in b["timeline"]) + "</ol>")
        for t in b.get("p", []):
            out.append(esc_para(t))
        if "ul" in b:
            out.append("<ul class=\"rule\">" + "".join(f"<li>{E(x)}</li>" for x in b["ul"]) + "</ul>")
            if b.get("note"):
                out.append(f'<p class="note">{E(b["note"])}</p>')
        if "fig" in b:
            out.append(figure(b["fig"]))
        if "nums" in b:
            out.append('<ul class="nums">' + "".join(f'<li><b>{E(n)}</b><span>{E(l)}</span></li>' for n, l in b["nums"]) + "</ul>")
            out.append(f'<p class="note">{E(b["cap"])}</p>')
        if "svg" in b:
            out.append(f'<figure class="svgfig">{cobweb(prefix)}<figcaption>{E(b["cap"])}</figcaption></figure>')
    out.append('<ul class="proof">' + "".join(link(l, h) for l, h in c["proof"]) + "</ul></article>")
    return "".join(out)


def card_html(ch):
    i = ch["n"]
    stamp = ""
    if ch.get("stamp"):
        a, b = ch["stamp"]
        stamp = f'<span class="stamp" aria-hidden="true"><b>{E(a)}</b><i>{E(b)}</i></span>'
    kicker = f'{i:02d} · {E(ch["label"])} · {E(ch["year"])}'
    body = "".join(esc_para(t) for t in ch["rac"])
    media = ""
    if ch.get("thumb"):
        t = ch["thumb"]
        media += (f'<figure class="thumb"><img src="{E(t["src"])}" alt="{E(t["alt"])}" width="120" height="90" decoding="async">'
                  f'<figcaption>{E(t["cap"])}</figcaption></figure>')
    proof = "".join(link(l, h) for l, h in ch.get("proof", []))
    if ch.get("contact"):
        proof = (link("Email me", "mailto:" + LINKS["email"], False) + link("LinkedIn", LINKS["linkedin"]) + link("GitHub", LINKS["github"]) +
                 link("Product Hunt", LINKS["ph_profile"]) + "".join(link(l, h) for l, h in RESUMES))
    act = ""
    if ch.get("featured"):
        act = f'<p class="cact"><button type="button" class="btn big" data-case="{E(ch["id"])}">Read the case study</button></p>'
    return (f'<header class="chead"><p class="kicker mono">{kicker}</p>{stamp}</header>'
            f'<h2 class="ctitle" tabindex="-1">{E(ch["title"])}</h2><div class="cbody">{body}</div>'
            f'<div class="cmedia">{media}<ul class="proof">{proof}</ul></div>{act}')


def hero_html():
    chips = "".join(f'<li><button type="button" class="chipcard" data-go="{c["go"]}"><b>{E(c["k"])}</b><span>{E(c["v"])}</span></button></li>' for c in HERO["chips"])
    return f"""<div class="h-in">
      <p class="mono h-k">{E(HERO['kicker'])}</p>
      <h1 class="h-h1">{E(HERO['h1'])}</h1>
      <p class="h-sub">{E(HERO['sub'])}</p>
      <ul class="chips" aria-label="Three pieces of work">{chips}</ul>
      <p class="h-act"><button class="btn big" type="button" data-go="1" id="bExplore">Explore work</button>
        <a class="btn" href="resume.pdf" download>Resume</a>
        <a class="btn" href="{E(LINKS['linkedin'])}" target="_blank" rel="noopener noreferrer">LinkedIn<span class="sr"> (opens in a new tab)</span></a>
        <a class="btn" href="{E(LINKS['github'])}" target="_blank" rel="noopener noreferrer">GitHub<span class="sr"> (opens in a new tab)</span></a>
        <button class="btn" type="button" data-go="{N - 1}">Contact</button></p>
    </div>
    <figure class="h-photo"><img src="{E(HERO['photo']['src'])}" alt="{E(HERO['photo']['alt'])}" width="480" height="320"><figcaption class="mono">{E(HERO['photo']['cap'])}</figcaption></figure>"""


def plain_html():
    parts = []
    for ch in CHAPTERS[1:]:
        art = [f'<article id="p-{ch["id"]}"><h2><span class="mono">{ch["n"]:02d} · {E(ch["label"])} · {E(ch["year"])}</span><br>{E(ch["title"])}</h2>']
        art += [esc_para(t) for t in ch["rac"]]
        if ch.get("thumb"):
            art.append(figure(ch["thumb"]))
        if ch["id"] in CASES:
            art.append(f'<details class="pcase" open><summary>Case study: {E(CASES[ch["id"]]["title"])}</summary>{case_html(ch["id"], "plain-case-")}</details>')
        pr = "".join(link(l, h) for l, h in ch.get("proof", []))
        if ch.get("contact"):
            pr = (link("Email: " + LINKS["email"], "mailto:" + LINKS["email"], False) + link("LinkedIn", LINKS["linkedin"]) + link("GitHub", LINKS["github"]) +
                  link("Product Hunt profile", LINKS["ph_profile"]) + "".join(link(l, h) for l, h in RESUMES))
        if pr:
            art.append(f'<ul class="proof">{pr}</ul>')
        art.append("</article>")
        parts.append("".join(art))
    return "".join(parts)


def main():
    chapters = []
    for ch in CHAPTERS:
        chapters.append(dict(id=ch["id"], n=ch["n"], label=ch["label"], title=ch.get("title", NAME), year=ch["year"], board=ch["board"], sub=ch["sub"],
                             country=ch["country"], mon=ch["mon"], logos=ch["logos"], featured=bool(ch.get("featured"))))
    data = dict(chapters=chapters, logos=LOGOFILES, logoNames=LOGONAMES)
    templates = [f'<template id="t-{ch["id"]}">{card_html(ch)}</template>' for ch in CHAPTERS[1:]]
    templates += [f'<template id="c-{cid}">{case_html(cid, "case-")}</template>' for cid in CASES]
    index_items = "".join(f'<li><button type="button" data-go="{ch["n"]}"><b>{ch["n"]:02d}</b><span>{E(ch["label"])}<small>{E(ch["year"])}</small></span></button></li>' for ch in CHAPTERS)
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
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Sri Krishna Taak: builder and programme lead, with a train on a rail line">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(TITLE)}"><meta name="twitter:description" content="{E(DESC)}"><meta name="twitter:image" content="{E(LINKS['site'])}assets/og.png">
<link rel="preload" href="assets/fonts/inter-tight-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/css/world.css">
<script type="application/ld+json">{ld}</script>
<script>document.documentElement.className='js'</script>
</head>
<body>
<a class="skip" href="#plain" id="skipText">Skip the animation: go to the text version</a>
<canvas id="gl" aria-hidden="true"></canvas>
<div class="vig" aria-hidden="true"></div>
<div class="cut" id="cut" aria-hidden="true"></div>
<div class="hud intro" id="hud" hidden>
  <header class="bar">
    <a class="logo" href="#start" data-go="0" aria-label="{E(NAME)}, back to the start">SKT<span>.</span></a>
    <nav class="btns" aria-label="Site controls">
      <button type="button" id="bIndex" aria-expanded="false" aria-controls="index">Stations</button>
      <button type="button" id="bSound" aria-pressed="false"><span class="m-hide">Train&nbsp;</span><span id="sndTxt">sound: off</span></button>
      <button type="button" id="bPlain">Text<span class="m-hide">&nbsp;version</span></button>
      <a class="solid" href="resume.pdf" download>Resume</a>
    </nav>
  </header>
  <nav class="index" id="index" aria-label="Stations" hidden><ol>{index_items}</ol></nav>
  <section class="hero" id="hero" aria-label="Introduction">{hero_html()}</section>
  <section class="card" id="card" aria-label="Station"></section>
  <nav class="pager" id="pager" aria-label="Journey"><button type="button" id="bPrev" aria-label="Previous station">&#8592;<span> Previous</span></button><p class="pcount mono" id="pcount" aria-hidden="true"></p><button type="button" id="bNext" aria-label="Next station"><span>Next </span>&#8594;</button></nav>
  <div class="hintline mono" id="hintline" aria-hidden="true">Scroll, swipe or press &#8594; to ride one stop</div>
  <div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-label="Case study" hidden><div class="sheet-in"><button type="button" class="sheet-x btn" id="sheetX">Close case study</button><div id="sheetBody"></div></div></div>
</div>
<p class="sr" id="live" role="status" aria-live="polite"></p>
<main id="plain" class="plain" tabindex="-1">
  <header><p class="mono">Text version of the portfolio</p><h1>{E(NAME)}</h1>
  <p class="lead">{E(HERO['h1'])}</p><p>{E(HERO['sub'])}</p>
  <ul class="chips">{"".join(f'<li><a class="chipcard" href="#p-{CHAPTERS[c["go"]]["id"]}"><b>{E(c["k"])}</b><span>{E(c["v"])}</span></a></li>' for c in HERO["chips"])}</ul>
  <p><a class="btn big" href="mailto:{E(LINKS['email'])}">Email me</a> <a class="btn" href="resume.pdf" download>Resume</a> <a class="btn" href="{E(LINKS['linkedin'])}" target="_blank" rel="noopener noreferrer">LinkedIn<span class="sr"> (opens in a new tab)</span></a> <a class="btn" href="{E(LINKS['github'])}" target="_blank" rel="noopener noreferrer">GitHub<span class="sr"> (opens in a new tab)</span></a> <button class="btn" type="button" id="bRide">Ride the train</button></p></header>
  {plain_html()}
  <footer><p>An independent portfolio by {E(NAME)}. Figures come from my resume unless a source is linked beside the claim.</p></footer>
</main>
{"".join(templates)}
<script>window.YATRA={json.dumps(data, ensure_ascii=False)};</script>
<script src="assets/vendor/three.min.js"></script>
<script src="assets/js/world.js"></script>
</body></html>"""

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets/css").mkdir(parents=True)
    (OUT / "assets/js").mkdir(parents=True)
    (OUT / "assets/vendor").mkdir()
    (OUT / "assets/img").mkdir()
    (OUT / "assets/logos").mkdir()
    shutil.copytree(ROOT / "assets/fonts", OUT / "assets/fonts", ignore=shutil.ignore_patterns("Geist*"))
    used_img = set()
    for ch in CHAPTERS:
        if ch.get("thumb") and ch["thumb"]["src"].startswith("assets/img/"):
            used_img.add(ch["thumb"]["src"])
    used_img.add(HERO["photo"]["src"])
    for src in used_img:
        shutil.copy(ROOT / src, OUT / src)
    shutil.copytree(ROOT / "assets/work", OUT / "assets/work")
    for f in LOGOFILES.values():
        shutil.copy(ROOT / "assets/logos" / f, OUT / "assets/logos" / f)
    shutil.copy(ROOT / "assets/vendor/three.min.js", OUT / "assets/vendor/three.min.js")
    shutil.copy(ROOT / "world/src/world.css", OUT / "assets/css/world.css")
    shutil.copy(ROOT / "world/src/world.js", OUT / "assets/js/world.js")
    for extra in ("favicon.svg", "og.png"):
        p = ROOT / "world/src" / extra
        if p.exists():
            shutil.copy(p, OUT / "assets" / extra)
    (OUT / "index.html").write_text(page, encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    res = ROOT / "content/resumes"
    shutil.copy(res / "Sri_Krishna_Main_Resume.pdf", OUT / "resume.pdf")
    shutil.copy(res / "Sri_Krishna_Founders_Office_Resume.pdf", OUT / "resume-founders-office.pdf")
    shutil.copy(res / "Sri_Krishna_Consulting_Resume.pdf", OUT / "resume-consulting.pdf")
    print("built ->", OUT)


if __name__ == "__main__":
    main()
