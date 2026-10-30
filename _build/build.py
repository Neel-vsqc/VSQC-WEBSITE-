"""
Builds the VSQC static site into the folder above this one.

    python _build/build.py

Edit copy in content.py, layout in the template functions below.
Output is plain HTML — no build step is needed to host it.
"""
import json
from html import escape as e
from pathlib import Path

from content import (ACHIEVEMENTS, CONTACT, HOME, LOGOS, POLICIES, PORTAL,
                     SERVICES, SITE, STANDARDS, TEAM)

OUT = Path(__file__).resolve().parent.parent
N = len(SERVICES)
ARROW = '<svg class="arrow" viewBox="0 0 28 10" aria-hidden="true"><path d="M0 5h26M22 1l4 4-4 4"/></svg>'


def svc_url(s):
    return f"service-{s['slug']}.html"


# ------------------------------------------------------------------
# Shared layout
# ------------------------------------------------------------------
#            href                   label           key
NAV = [
    ("index.html", "Home", "home"),
    ("index.html#services", "Services", "services"),
    ("portal.html", "Portal", "portal"),
    ("achievements.html", "Achievements", "achievements"),
    ("policies.html", "Policies", "policies"),
    ("team.html", "Team", "team"),
    ("contact.html", "Contact", "contact"),
]
PAGES = ["portal", "achievements", "policies", "team", "contact"] + [f"service-{s['slug']}" for s in SERVICES]


def head(title, desc, preload=""):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="theme-color" content="#030C18">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300;400;500;600&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
  {preload}
  <link rel="stylesheet" href="styles.css">
</head>"""


def header(active, home=False):
    """Centred glass pill (logo · Contact · Menu). All links live in the menu panel."""
    i = 0
    main_links = []
    for href, label, key in NAV:
        extra = ""
        if home and key == "services":
            href, extra = "#services", ' data-scroll-step="0"'
        elif home and key == "home":
            href, extra = "#top", ' data-scroll-step="-1"'
        cur = ' aria-current="page"' if key == active else ""
        main_links.append(f'<li class="menu__item" style="--i:{i}"><a class="menu__link" href="{href}" data-nav="{key}"{cur}{extra}>{label}</a></li>')
        i += 1
    svc_links = []
    for s in SERVICES:
        cur = ' aria-current="page"' if active == f"service-{s['slug']}" else ""
        svc_links.append(f'<li class="menu__item" style="--i:{i}"><a class="menu__link" href="{svc_url(s)}"{cur}>{e(s["short"])}</a></li>')
        i += 1
    return f"""
<body class="{'is-home' if home else 'is-page'}">
  <a class="skip" href="#content">Skip to content</a>
  <header class="nav" id="nav">
    <div class="nav__shell">
      <div class="nav__bar glass" data-glass>
        <a class="nav__logo" href="index.html" aria-label="VSQC home">VSQC</a>
        <a class="nav__cta" href="contact.html">Contact</a>
        <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="menu" aria-label="Open menu">
          <span class="nav__burger" aria-hidden="true"><i></i><i></i><i></i></span>
        </button>
      </div>
      <nav class="menu glass" id="menu" aria-label="Site">
        <p class="menu__label">Explore</p>
        <ul class="menu__list">{''.join(main_links)}</ul>
        <hr class="menu__rule">
        <p class="menu__label">Services</p>
        <ul class="menu__list menu__list--small">{''.join(svc_links)}</ul>
        <div class="menu__foot"><span>{' · '.join(SITE['offices'])}</span><a href="mailto:{e(SITE['email'])}">{e(SITE['email'])}</a></div>
      </nav>
    </div>
  </header>
  <div class="nav__scrim" aria-hidden="true"></div>
"""


def logos_block(title="Trusted by industry leaders and <em>certification bodies</em>",
                note="Clients we have certified and the certification bodies we partner with."):
    def tile(name, slug, tag, style):
        f = next((p for p in (OUT / "logos").glob(f"{slug}.*")), None) if (OUT / "logos").exists() else None
        if f:
            inner = f'<img src="logos/{f.name}" alt="{e(name)}" loading="lazy">'
        else:
            inner = (f'<span class="wm"><span class="wm__name wm__name--{style}">{e(name)}</span>'
                     f'<span class="wm__tag">{e(tag)}</span></span>')
        return f'<li class="logo glass" title="{e(name)}">{inner}</li>'

    # repeat the short list so one copy is always wider than the screen → seamless loop
    row = "".join(tile(*l) for l in LOGOS) * 3
    chips = "".join(f'<li class="chip"><b>{e(c)}</b><span>{e(n)}</span></li>' for c, n, _ in STANDARDS)
    return f"""
  <section class="logos" aria-label="Clients, partners and standards">
    <div class="logos__head">
      <div>
        <p class="eyebrow rv"><span class="hairline"></span>Clients &amp; partners</p>
        <h2 class="logos__title rv">{title}</h2>
      </div>
      <p class="logos__note rv">{e(note)}</p>
    </div>
    <div class="marquee" style="--speed: 38s">
      <div class="marquee__track">
        <ul class="marquee__list">{row}</ul>
        <ul class="marquee__list" aria-hidden="true">{row}</ul>
      </div>
    </div>
    <div class="marquee marquee--reverse" style="--speed: 120s">
      <div class="marquee__track">
        <ul class="marquee__list">{chips}</ul>
        <ul class="marquee__list" aria-hidden="true">{chips}</ul>
      </div>
    </div>
  </section>"""


def footer(scripts=""):
    svc_links = "\n".join(f'<li><a href="{svc_url(s)}">{e(s["short"])}</a></li>' for s in SERVICES)
    cfg = json.dumps({k: SITE[k] for k in ("email", "form_endpoint", "portal_customer_url", "portal_employee_url")})
    return f"""
  <footer class="footer">
    <div class="footer__top">
      <p class="footer__line rv">The one stop shop for your <em>management services</em> needs.</p>
      <a class="btn btn--solid rv" href="contact.html">Contact us</a>
    </div>
    <div class="footer__cols">
      <div>
        <p class="footer__h">Services</p>
        <ul>{svc_links}</ul>
      </div>
      <div>
        <p class="footer__h">Company</p>
        <ul>
          <li><a href="portal.html">Portal</a></li>
          <li><a href="achievements.html">Achievements</a></li>
          <li><a href="policies.html">Policies</a></li>
          <li><a href="team.html">Team &amp; Partners</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <p class="footer__h">Offices</p>
        <ul>{''.join(f'<li>{e(o)}</li>' for o in SITE['offices'])}</ul>
      </div>
      <div>
        <p class="footer__h">Reach us</p>
        <ul>
          <li><a href="mailto:{e(SITE['email'])}">{e(SITE['email'])}</a></li>
          <li><a href="contact.html?form=rfq">Request a quote</a></li>
          <li><a href="contact.html?form=grievance">Grievance</a></li>
          <li><a href="contact.html?form=whistleblower">Whistleblower</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__base">
      <span>&copy; <span data-year>2026</span> {e(SITE['legal'])}</span>
      <a class="footer__logo" href="index.html" aria-label="VSQC home">VSQC</a>
    </div>
  </footer>

  <script>window.VSQC_CONFIG = {cfg};</script>
  <script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js" defer></script>
  <script src="site.js" defer></script>
  {scripts}
</body>
</html>
"""


def page_hero(eyebrow, title, lead, clip, actions="", title_html=None):
    return f"""
  <section class="phero" id="content">
    <div class="phero__media" aria-hidden="true">
      <div class="phero__camera" data-parallax>
        <video class="phero__video" src="clip-{clip}.mp4" poster="poster-{clip}.jpg" muted playsinline autoplay loop preload="auto" data-autopause></video>
      </div>
      <div class="stage__shade"></div>
    </div>
    <div class="phero__inner">
      <p class="eyebrow hero-in"><span class="hairline"></span>{eyebrow}</p>
      <h1 class="phero__title hero-in">{title_html or e(title)}</h1>
      <p class="phero__lead hero-in">{e(lead)}</p>
      {f'<div class="phero__actions hero-in">{actions}</div>' if actions else ''}
    </div>
    <a class="enter-hint enter-hint--page" href="#main" aria-label="Scroll down">
      <span class="enter-hint__mouse" aria-hidden="true"><span></span></span>
    </a>
  </section>
  <div id="main"></div>"""


def sec_head(eyebrow, title, note="", id_=""):
    return f"""
    <header class="sec__head"{f' id="{id_}"' if id_ else ''}>
      <p class="eyebrow rv"><span class="hairline"></span>{e(eyebrow)}</p>
      <h2 class="sec__title rv">{title}</h2>
      {f'<p class="sec__note rv">{e(note)}</p>' if note else ''}
    </header>"""


def numbered(items):
    rows = "\n".join(
        f"""<li class="item rv">
          <span class="item__num">{i:02d}</span>
          <h3 class="item__title">{e(t)}</h3>
          <p class="item__desc">{e(d)}</p>
        </li>""" for i, (t, d) in enumerate(items, 1))
    return f'<ol class="items">{rows}</ol>'


def cta(title_html, href, label="Request a quote"):
    return f"""
  <section class="cta">
    <h2 class="cta__title rv">{title_html}</h2>
    <div class="cta__actions rv">
      <a class="btn btn--solid" href="{href}">{label}</a>
      <a class="btn btn--ghost" href="contact.html">Talk to us</a>
    </div>
  </section>"""


def write(name, html):
    (OUT / name).write_text(html, encoding="utf-8")
    print("wrote", name)


# ------------------------------------------------------------------
# HOME
# ------------------------------------------------------------------
def build_home():
    articles = []
    for i, s in enumerate(SERVICES):
        articles.append(f"""
            <article class="svc" data-short="{e(s['short'])}">
              <p class="svc__count reveal"><span class="svc__num">{i+1:02d}</span> / {N:02d}</p>
              <h2 class="svc__title">{e(s['title'])}</h2>
              <p class="svc__desc reveal">{e(s['line'])}</p>
              <p class="svc__tags reveal">{e(s['tags'])}</p>
              <a class="btn btn--line reveal" href="{svc_url(s)}">Explore {ARROW}</a>
            </article>""")

    index_rows = "\n".join(
        f"""<li class="idx__row rv">
          <a href="{href}">
            <span class="idx__num">{i:02d}</span>
            <span class="idx__title">{e(t)}</span>
            <span class="idx__desc">{e(d)}</span>
            {ARROW}
          </a>
        </li>""" for i, (href, t, d) in enumerate(HOME["index"], 1))

    html = head(
        "VSQC — Management Systems, ESG & Digital Transformation Consulting",
        "VSQC is a one stop shop for management services: ISO certifications, ESG frameworks, digital tools, information security and safety systems.",
        '<link rel="preload" as="image" href="0-hero.png">',
    ) + header("home", home=True) + f"""
  <main id="content">
    <!-- SHOWCASE = HERO + SERVICES. .stage is sticky for the whole section. -->
    <section class="showcase" id="top" style="--steps: {N}">
      <div class="stage" id="stage">
        <div class="stage__media" aria-hidden="true">
          <div class="stage__camera" id="camera">
            <img class="stage__poster" src="0-hero.png" alt="">
            <video class="stage__video" muted playsinline preload="auto" poster="0-hero.png"></video>
            <video class="stage__video" muted playsinline preload="auto"></video>
            <video class="stage__video" muted playsinline preload="auto"></video>
            <video class="stage__video" muted playsinline preload="auto"></video>
          </div>
          <div class="stage__shade"></div>
        </div>

        <div class="services" id="services-ui" aria-label="Our services">
          <p class="services__eyebrow"><span class="hairline"></span>Our services</p>
          <ol class="rail" id="rail"></ol>
          <div class="svc-stack" id="svc-stack">{''.join(articles)}
          </div>
        </div>
      </div>

      <div class="hero" id="hero">
        <div class="hero__inner">
          <p class="hero__eyebrow"><span class="hairline"></span>Management consulting · India · Sri Lanka · UAE</p>
          <h1 class="hero__title">The <em>one stop shop</em> for your management services needs</h1>
          <p class="hero__sub">Top-line and bottom-line excellence through ISO certifications, ESG frameworks, digital tools, information security and safety systems.</p>
          <div class="hero__actions">
            <a class="btn btn--solid" href="#services" data-scroll-step="0">Explore our services</a>
            <a class="btn btn--ghost" href="contact.html">Contact us</a>
          </div>
        </div>
        <a class="enter-hint" href="#services" data-scroll-step="0">
          <span class="enter-hint__label">Scroll to enter</span>
          <span class="enter-hint__mouse" aria-hidden="true"><span></span></span>
        </a>
      </div>
    </section>

    <!-- WELCOME -->
    <section class="statement">
      <p class="eyebrow rv"><span class="hairline"></span>About VSQC</p>
      <p class="statement__text rv">{e(HOME['welcome'])}</p>
    </section>
    {logos_block()}

    <!-- ALL SERVICES (quiet text index) -->
    <section class="sec sec--tight">
      {sec_head('All services', 'Seven practices, <em>one partner</em>', HOME['services_intro'])}
      <ol class="idx">
        {''.join(f'''<li class="idx__row rv"><a href="{svc_url(s)}"><span class="idx__num">{i:02d}</span><span class="idx__title">{e(s['title'])}</span><span class="idx__desc">{e(s['line'])}</span>{ARROW}</a></li>''' for i, s in enumerate(SERVICES, 1))}
      </ol>
    </section>

    <!-- EXPLORE VSQC -->
    <section class="sec sec--tight">
      {sec_head('Explore VSQC', 'Everything in <em>one place</em>')}
      <ol class="idx">{index_rows}</ol>
    </section>
  </main>
""" + footer('<script src="main.js" defer></script>')
    write("index.html", html)


# ------------------------------------------------------------------
# SERVICE PAGES
# ------------------------------------------------------------------
def standards_block():
    rows = "\n".join(
        f"""<li class="std" data-search="{e((c + ' ' + n + ' ' + d).lower())}">
          <button class="std__btn" type="button" aria-expanded="false" aria-controls="std-{i}">
            <span class="std__code">{e(c)}</span>
            <span class="std__name">{e(n)}</span>
            <span class="std__plus" aria-hidden="true"></span>
          </button>
          <div class="std__panel" id="std-{i}" hidden><p>{e(d)}</p></div>
        </li>""" for i, (c, n, d) in enumerate(STANDARDS))
    return f"""
  <section class="sec" id="standards">
    {sec_head('The standards', f'{len(STANDARDS)} standards, <em>one team</em>', 'ISO and other management system standards we implement, audit and support.')}
    <div class="stds" data-standards>
      <div class="stds__bar rv">
        <label class="field field--search">
          <span class="field__label">Find a standard</span>
          <input type="search" placeholder="e.g. 27001, food, automotive" autocomplete="off" data-standards-search>
        </label>
        <p class="stds__count" data-standards-count aria-live="polite">{len(STANDARDS)} standards</p>
      </div>
      <ul class="stds__list">{rows}</ul>
      <p class="stds__empty" data-standards-empty hidden>No standard matches that search. <a href="contact.html?form=rfq&amp;service=iso">Ask us about it</a>.</p>
    </div>
  </section>"""


def build_services():
    for i, s in enumerate(SERVICES):
        nxt = SERVICES[(i + 1) % N]
        actions = (f'<a class="btn btn--solid" href="contact.html?form=rfq&amp;service={s["slug"]}">Request a quote</a>'
                   f'<a class="btn btn--ghost" href="#what-we-do">What we do</a>')
        html = head(f"{s['title']} — VSQC", s["intro"],
                    f'<link rel="preload" as="image" href="poster-{s["loop"]}.jpg">') + header(f"service-{s['slug']}") + f"""
  <main>
    {page_hero(f'Service {i+1:02d} / {N:02d}', s['title'], s['intro'], s['loop'], actions)}

    <section class="sec">
      {sec_head('What we do', f'{len(s["items"])} ways we <em>help</em>', s['line'], 'what-we-do')}
      {numbered(s['items'])}
    </section>
    {standards_block() if s.get('standards') else ''}
    {cta(f'Discuss your <em>{e(s["short"])}</em> requirement with VSQC', f'contact.html?form=rfq&amp;service={s["slug"]}')}

    <a class="next rv" href="{svc_url(nxt)}">
      <span class="eyebrow"><span class="hairline"></span>Next service</span>
      <span class="next__title">{e(nxt['title'])}</span>
      {ARROW}
    </a>
  </main>
""" + footer()
        write(svc_url(s), html)


# ------------------------------------------------------------------
# PORTAL
# ------------------------------------------------------------------
def build_portal():
    html = head("VSQC Portal — Customers & Employees", PORTAL["intro"],
                '<link rel="preload" as="image" href="poster-11.jpg">') + header("portal") + f"""
  <main>
    {page_hero('Customers &amp; employees', 'Login to your VSQC Portal', PORTAL['intro'], 11)}

    <section class="sec">
      {sec_head('Sign in', 'Choose your <em>gateway</em>')}
      <ol class="idx idx--portal">
        <li class="idx__row rv">
          <a href="#" data-portal="customer">
            <span class="idx__num">01</span>
            <span class="idx__title">Customers</span>
            <span class="idx__desc">Track project progress, audit reports and compliance metrics for your organization.</span>
            {ARROW}
          </a>
        </li>
        <li class="idx__row rv">
          <a href="#" data-portal="employee">
            <span class="idx__num">02</span>
            <span class="idx__title">Employees</span>
            <span class="idx__desc">Your workspace for engagements, audits, documents and schedules.</span>
            {ARROW}
          </a>
        </li>
      </ol>
      <p class="sec__note portal-note rv" data-portal-note hidden>Portal access is set up by VSQC for each client and team member. If you don't have an account yet, <a href="contact.html?form=feedback&amp;topic=Portal%20access">request access here</a>.</p>
    </section>
    {cta('Need access to the <em>portal</em>?', 'contact.html?topic=Portal%20access', 'Request access')}
  </main>
""" + footer()
    write("portal.html", html)


# ------------------------------------------------------------------
# ACHIEVEMENTS
# ------------------------------------------------------------------
def build_achievements():
    a = ACHIEVEMENTS
    html = head("Our Achievements — VSQC", a["intro"],
                '<link rel="preload" as="image" href="poster-3.jpg">') + header("achievements") + f"""
  <main>
    {page_hero('Our achievements', 'A record built on certifications', a['intro'], 3)}

    <section class="sec">
      {sec_head('Track record', 'Achievements, <em>clients</em> and credentials')}
      {numbered(a['rows'])}
    </section>

    <section class="sec sec--split">
      <div>
        {sec_head('Clients who speak for us', 'Trusted by <em>industry leaders</em>')}
      </div>
      <ul class="names rv">{''.join(f'<li>{e(c)}</li>' for c in a['clients'])}</ul>
    </section>

    <section class="sec sec--split">
      <div>
        {sec_head('Consulting partner', 'Working with top-tier <em>certification bodies</em>')}
      </div>
      <ul class="names rv">{''.join(f'<li>{e(c)}</li>' for c in a['partners'])}</ul>
    </section>

    <section class="sec sec--split">
      <div>
        {sec_head('Our own certifications', 'We hold ourselves to <em>the same standard</em>')}
      </div>
      <ul class="certs rv">{''.join(f'<li><span class="certs__code">{e(c)}</span><span>{e(n)}</span></li>' for c, n in a['own_certs'])}</ul>
    </section>
    {logos_block('Clients, partners and the <em>standards</em> we work with', 'Multi-site, multi-standard certifications delivered with leading certification bodies.')}
    {cta('Start your <em>certification</em> journey', 'contact.html?form=rfq')}
  </main>
""" + footer()
    write("achievements.html", html)


# ------------------------------------------------------------------
# POLICIES
# ------------------------------------------------------------------
def build_policies():
    p = POLICIES

    def rows(items, kind):
        return "\n".join(
            f"""<li class="idx__row rv">
              <a href="contact.html?form=feedback&amp;topic={e(t.replace(' ', '%20'))}%20%E2%80%94%20copy%20request">
                <span class="idx__num">{i:02d}</span>
                <span class="idx__title">{e(t)}{' process' if kind == 'process' else ''}</span>
                <span class="idx__desc">{e(d)}</span>
                <span class="idx__cta">Request a copy {ARROW}</span>
              </a>
            </li>""" for i, (t, d) in enumerate(items, 1))

    html = head("Our Policies — VSQC", p["intro"],
                '<link rel="preload" as="image" href="poster-15.jpg">') + header("policies") + f"""
  <main>
    {page_hero('Our policies', 'Integrity, written down', p['intro'], 15)}

    <section class="sec sec--tight">
      {sec_head('Policies', 'ESG, whistleblower &amp; <em>quality</em>', p['policies_note'])}
      <ol class="idx">{rows(p['policies'], 'policy')}</ol>
    </section>

    <section class="sec sec--tight">
      {sec_head('Processes', 'How we <em>deliver</em>', p['processes_note'])}
      <ol class="idx">{rows(p['processes'], 'process')}</ol>
    </section>
    {cta('Raise a concern <em>confidentially</em>', 'contact.html?form=whistleblower', 'Grievance &amp; whistleblower')}
  </main>
""" + footer()
    write("policies.html", html)


# ------------------------------------------------------------------
# TEAM
# ------------------------------------------------------------------
def build_team():
    t = TEAM
    people = ""
    if t["people"]:
        cards = "".join(
            f"""<li class="person rv">{f'<img src="{e(ph)}" alt="" loading="lazy">' if ph else ''}<p class="person__name">{e(n)}</p><p class="person__role">{e(r)}</p></li>"""
            for n, r, ph in t["people"])
        people = f"""<section class="sec">{sec_head('Our people', 'The <em>team</em>')}<ul class="people">{cards}</ul></section>"""
    html = head("Our Team & Partners — VSQC", t["intro"],
                '<link rel="preload" as="image" href="poster-7.jpg">') + header("team") + f"""
  <main>
    {page_hero('Our team &amp; partners', 'People behind every certification', t['intro'], 7)}
    {people}
    <section class="sec sec--split">
      <div>{sec_head('Strategic partners', 'Consulting partner to leading <em>certification bodies</em>')}</div>
      <ul class="names rv">{''.join(f'<li>{e(c)}</li>' for c in ACHIEVEMENTS['partners'])}</ul>
    </section>
    <section class="sec sec--split">
      <div>{sec_head('Where we work', 'Offices across <em>three countries</em>')}</div>
      <ul class="names rv">{''.join(f'<li>{e(o)}</li>' for o in SITE['offices'])}</ul>
    </section>
    <section class="sec sec--split">
      <div>{sec_head('Disciplines', 'One team, <em>seven practices</em>')}</div>
      <ul class="names names--small rv">{''.join(f'<li><a href="{svc_url(s)}">{e(s["short"])}</a></li>' for s in SERVICES)}</ul>
    </section>
    {logos_block()}
    {cta('Work with the <em>VSQC</em> team', 'contact.html')}
  </main>
""" + footer()
    write("team.html", html)


# ------------------------------------------------------------------
# CONTACT
# ------------------------------------------------------------------
def build_contact():
    opts = "".join(f'<option value="{s["slug"]}">{e(s["title"])}</option>' for s in SERVICES)
    hp = '<label class="hp" aria-hidden="true">Leave empty <input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label>'

    def field(name, label, type_="text", req=True, auto="", full=False, extra=""):
        r = " required" if req else ""
        a = f' autocomplete="{auto}"' if auto else ""
        return f"""<label class="field{' field--full' if full else ''}"><span class="field__label">{label}{'' if req else ' <em>(optional)</em>'}</span><input type="{type_}" name="{name}"{r}{a}{extra}></label>"""

    def area(name, label, req=True):
        return f"""<label class="field field--full"><span class="field__label">{label}</span><textarea name="{name}" rows="5"{' required' if req else ''}></textarea></label>"""

    def actions(label):
        return f"""<div class="form__foot"><button class="btn btn--solid" type="submit">{label}</button><p class="form__status" role="status" aria-live="polite"></p></div>"""

    forms = {
        "rfq": ("Request a quote", f"""
          <form class="form" data-form="Request for quote" novalidate>
            {hp}
            {field('name', 'Full name', auto='name')}
            {field('company', 'Company', auto='organization')}
            {field('email', 'Work email', 'email', auto='email')}
            {field('phone', 'Phone', 'tel', req=False, auto='tel')}
            <label class="field"><span class="field__label">Service</span><select name="service" required><option value="">Select a service</option>{opts}</select></label>
            {field('sites', 'Number of sites', 'number', req=False, extra=' min="1" inputmode="numeric"')}
            {field('standards', 'Standards or scope', req=False, full=True, extra=' placeholder="e.g. ISO 9001, ISO 14001, EcoVadis"')}
            {area('message', 'Tell us about your requirement')}
            {actions('Send request')}
          </form>"""),
        "feedback": ("Feedback", f"""
          <form class="form" data-form="Feedback" novalidate>
            {hp}
            {field('name', 'Full name', auto='name')}
            {field('email', 'Email', 'email', auto='email')}
            {field('topic', 'Subject', full=True)}
            <fieldset class="field field--full rating"><legend class="field__label">How was your experience?</legend>
              {''.join(f'<label><input type="radio" name="rating" value="{n}"{" required" if n == 1 else ""}><span>{n}</span></label>' for n in range(1, 6))}
            </fieldset>
            {area('message', 'Your feedback')}
            {actions('Send feedback')}
          </form>"""),
        "grievance": ("Grievance", f"""
          <form class="form" data-form="Grievance" novalidate>
            {hp}
            {field('name', 'Full name', auto='name')}
            {field('email', 'Email', 'email', auto='email')}
            {field('phone', 'Phone', 'tel', req=False, auto='tel')}
            {field('reference', 'Project or reference', req=False)}
            {area('message', 'Describe your grievance')}
            {actions('Submit grievance')}
          </form>"""),
        "whistleblower": ("Whistleblower", f"""
          <form class="form" data-form="Whistleblower report" data-anonymous-form novalidate>
            {hp}
            <label class="check field--full"><input type="checkbox" name="anonymous" data-anonymous> <span>Report anonymously</span></label>
            <div class="form__identity" data-identity>
              {field('name', 'Full name', auto='name')}
              {field('email', 'Email', 'email', auto='email')}
            </div>
            <label class="field field--full"><span class="field__label">Category</span><select name="category" required><option value="">Select a category</option><option>Bribery or corruption</option><option>Fraud</option><option>Conflict of interest</option><option>Harassment or discrimination</option><option>Health, safety or environment</option><option>Data privacy</option><option>Other</option></select></label>
            {area('message', 'What happened? Include dates, places and people if you can.')}
            <p class="form__note field--full" data-anon-note hidden>Anonymous reports need the secure form service, which is not connected yet. Please share your email for now, or contact VSQC leadership directly.</p>
            {actions('Submit report')}
          </form>"""),
    }
    tabs = "".join(
        f'<button class="tab" role="tab" type="button" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if k == "rfq" else "false"}" data-tab="{k}">{label}</button>'
        for k, (label, _) in forms.items())
    panels = "".join(
        f'<div class="panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}"{"" if k == "rfq" else " hidden"}>{f}</div>'
        for k, (_, f) in forms.items())

    html = head("Contact VSQC — India, Sri Lanka, UAE", CONTACT["intro"],
                '<link rel="preload" as="image" href="poster-1.jpg">') + header("contact") + f"""
  <main>
    {page_hero('Contact us', 'Start your compliance journey', CONTACT['intro'], 1,
               '<a class="btn btn--solid" href="#forms">Write to us</a>' + f'<a class="btn btn--ghost" href="mailto:{e(SITE["email"])}">{e(SITE["email"])}</a>')}

    <section class="sec sec--split">
      <div>{sec_head('Locations', 'Offices in <em>three countries</em>')}</div>
      <ul class="names rv">{''.join(f'<li>{e(o)}</li>' for o in SITE['offices'])}</ul>
    </section>

    <section class="sec" id="forms">
      {sec_head('Forms', 'How can we <em>help</em>?', 'Request a quote or share your experience through our online forms. For concerns or complaints, use the secure grievance and whistleblower forms.')}
      <div class="tabs rv" role="tablist" aria-label="Contact forms">{tabs}</div>
      {panels}
    </section>
  </main>
""" + footer()
    write("contact.html", html)


def build_404():
    html = head("Page not found — VSQC", "This page could not be found.") + header("") + f"""
  <main id="content">
    <section class="notfound">
      <p class="eyebrow"><span class="hairline"></span>Page not found</p>
      <p class="notfound__code">404</p>
      <p class="phero__lead">The page you were looking for has moved or no longer exists.</p>
      <div class="notfound__actions">
        <a class="btn btn--solid" href="index.html">Back to home</a>
        <a class="btn btn--ghost" href="contact.html">Contact us</a>
      </div>
    </section>
  </main>
""" + footer()
    # absolute asset paths so the 404 page also renders under nested URLs
    html = html.replace('href="styles.css"', 'href="/styles.css"').replace('src="site.js"', 'src="/site.js"')
    write("404.html", html)


def build_server_config():
    """serve.json for the local preview: /policies and /policies.html both work,
    and query strings (?form=rfq) are kept. Most hosts (Netlify, Vercel,
    GitHub Pages) already serve extensionless URLs the same way."""
    rewrites = [{"source": f"/{p}", "destination": f"/{p}.html"} for p in PAGES + ["index"]]
    rewrites += [{"source": "/", "destination": "/index.html"},
                 {"source": "/services", "destination": "/index.html"}]
    cfg = {"cleanUrls": False, "directoryListing": False, "rewrites": rewrites}
    (OUT / "serve.json").write_text(json.dumps(cfg, indent=2))
    print("wrote serve.json")


if __name__ == "__main__":
    build_home()
    build_services()
    build_portal()
    build_achievements()
    build_policies()
    build_team()
    build_contact()
    build_404()
    build_server_config()
