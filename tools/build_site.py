#!/usr/bin/env python3
"""
Build the static demo for the Corporate Insurance Info Website (project 40746021).

Single source of truth: the CONTENT dict below. Every page is rendered from the
same header/footer shell so nav, SEO tags and schema stay consistent.

Run:  python3 tools/build_site.py
Out:  dist/
"""

import html
import os
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

SITE = {
    "brand": "Vantage Harbour",
    "brand_sub": "Assurance Group",
    "tagline": "Independent insurance advisers",
    "base_url": "https://anirudhatalmale6-alt.github.io/corporate-insurance-demo",
    "phone": "(000) 000-0000",
    "address_line": "100 Harbour Street, Suite 1200",
    "address_city": "Toronto, ON M5J 0A1",
    "map_query": "100+Harbour+Street+Toronto+ON",
    "hours": "Mon – Fri, 9:00 – 17:30",
    "year": "2026",
}

DEMO_BANNER = (
    "Design demo — every name, figure, photo and address on this site is "
    "placeholder content. None of it describes a real company."
)

NAV = [
    ("index.html", "Home"),
    ("about.html", "About Us"),
    ("team.html", "Our Team"),
    ("contact.html", "Contact"),
]


# ---------------------------------------------------------------- helpers

def e(text):
    return html.escape(str(text), quote=True)


def monogram(initials, tone="a"):
    """Placeholder portrait: initials on a soft gradient. Swapped for real photos later."""
    tones = {
        "a": ("#1d3b57", "#0e2235"),
        "b": ("#2d5570", "#16344c"),
        "c": ("#3c4f60", "#1e2c38"),
        "d": ("#234a5e", "#122a38"),
    }
    c1, c2 = tones[tone]
    gid = f"g{initials.lower()}{tone}"
    return (
        f'<svg class="avatar" viewBox="0 0 160 160" role="img" '
        f'aria-label="Placeholder portrait" xmlns="http://www.w3.org/2000/svg">'
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>'
        f"</linearGradient></defs>"
        f'<rect width="160" height="160" fill="url(#{gid})"/>'
        f'<circle cx="80" cy="64" r="27" fill="rgba(255,255,255,.14)"/>'
        f'<path d="M80 99c-26 0-44 16-48 38h96c-4-22-22-38-48-38z" fill="rgba(255,255,255,.14)"/>'
        f'<text x="80" y="92" text-anchor="middle" font-family="Georgia,serif" '
        f'font-size="52" fill="#ffffff" fill-opacity=".92">{e(initials)}</text>'
        f"</svg>"
    )


# ---------------------------------------------------------------- content

VALUES = [
    (
        "Independence",
        "We are not tied to a single carrier. Every recommendation is the one we "
        "would choose if the policy were our own.",
        "M12 2 3 6v6c0 5 3.8 8.9 9 10 5.2-1.1 9-5 9-10V6l-9-4z",
    ),
    (
        "Plain language",
        "Policy wording is dense by design. We translate it, in writing, before "
        "anything is signed.",
        "M4 5h16v11H8l-4 4V5z",
    ),
    (
        "Continuity",
        "The adviser who writes your file is the adviser who answers the phone "
        "when something happens.",
        "M12 3a9 9 0 1 0 9 9h-3a6 6 0 1 1-6-6V3z M12 7v5l4 2",
    ),
]

STATS = [
    ("Placeholder", "Year established"),
    ("Placeholder", "Clients advised"),
    ("Placeholder", "Carrier partners"),
    ("Placeholder", "Advisers on staff"),
]

PRACTICE = [
    ("Commercial lines", "Property, general liability, fleet and umbrella cover for owner-operated businesses."),
    ("Professional risk", "Errors & omissions, directors & officers, and cyber liability."),
    ("Group benefits", "Health, dental and disability programmes for small and mid-size employers."),
    ("Personal lines", "Home, auto, recreational property and high-value personal articles."),
]

HISTORY = [
    ("Placeholder year", "Founding", "A short paragraph describing how and why the agency was started, and by whom. Replace with the real account."),
    ("Placeholder year", "First office", "Where the practice opened and the market it served at the time."),
    ("Placeholder year", "Commercial practice", "The point at which commercial lines became a dedicated part of the business."),
    ("Placeholder year", "Today", "Current size, footprint and the kind of client the agency serves best."),
]

TEAM = [
    ("Placeholder Name", "Principal & Managing Adviser", "AB", "a",
     "Two or three sentences of biography: route into insurance, the lines they "
     "specialise in, designations held, and one human detail. Replace with the real bio."),
    ("Placeholder Name", "Director, Commercial Lines", "CD", "b",
     "Two or three sentences of biography. Mention the industries they know best "
     "and the size of risk they typically place."),
    ("Placeholder Name", "Senior Adviser, Group Benefits", "EF", "c",
     "Two or three sentences of biography covering benefits plan design and the "
     "employers they work with most often."),
    ("Placeholder Name", "Claims & Client Service Lead", "GH", "d",
     "Two or three sentences of biography focused on claims advocacy and what "
     "clients can expect during a loss."),
    ("Placeholder Name", "Adviser, Personal Lines", "IJ", "b",
     "Two or three sentences of biography covering household, auto and "
     "high-value personal articles."),
    ("Placeholder Name", "Operations Manager", "KL", "a",
     "Two or three sentences of biography covering renewals, documentation and "
     "the back office that keeps files accurate."),
]

FAQ = [
    ("Do you charge a fee for advice?",
     "Placeholder answer. State plainly how the agency is remunerated — commission, "
     "fee, or a mix — so a visitor is not left guessing."),
    ("Which carriers do you place business with?",
     "Placeholder answer. List the carrier panel, or describe it in general terms if "
     "the list changes often."),
    ("How quickly can I get a certificate of insurance?",
     "Placeholder answer. Give a realistic turnaround so expectations are set before "
     "the first call."),
]


# ---------------------------------------------------------------- shell

def head(page_file, title, description, extra_head=""):
    canonical = f"{SITE['base_url']}/{page_file}" if page_file != "index.html" else f"{SITE['base_url']}/"
    full_title = f"{title} | {SITE['brand']} {SITE['brand_sub']}"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(canonical)}">
<meta name="robots" content="noindex, nofollow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(SITE['brand'] + ' ' + SITE['brand_sub'])}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(canonical)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0e2235">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/css/site.css">
{extra_head}</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<p class="demo-banner" role="note">{e(DEMO_BANNER)}</p>
"""


def header(page_file):
    links = "".join(
        f'<li><a href="{f}"{" aria-current=\"page\"" if f == page_file else ""}>{e(label)}</a></li>'
        for f, label in NAV
    )
    return f"""<header class="site-head">
  <div class="wrap head-inner">
    <a class="brand" href="index.html">
      <span class="brand-mark" aria-hidden="true">VH</span>
      <span class="brand-text">
        <strong>{e(SITE['brand'])}</strong>
        <span>{e(SITE['brand_sub'])}</span>
      </span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav">
      <span class="nav-toggle-bars" aria-hidden="true"></span>
      <span class="sr-only">Menu</span>
    </button>
    <nav id="primary-nav" class="primary-nav" aria-label="Primary">
      <ul>{links}</ul>
      <a class="nav-cta" href="contact.html">Speak with an adviser</a>
    </nav>
  </div>
</header>
<main id="main">
"""


def footer():
    links = "".join(f'<li><a href="{f}">{e(label)}</a></li>' for f, label in NAV)
    return f"""</main>
<footer class="site-foot">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <span class="brand-mark" aria-hidden="true">VH</span>
      <p><strong>{e(SITE['brand'])} {e(SITE['brand_sub'])}</strong><br>{e(SITE['tagline'])}</p>
    </div>
    <div>
      <h2>Pages</h2>
      <ul class="plain">{links}</ul>
    </div>
    <div>
      <h2>Office</h2>
      <address>
        {e(SITE['address_line'])}<br>{e(SITE['address_city'])}<br>
        <a href="tel:0000000000">{e(SITE['phone'])}</a><br>
        {e(SITE['hours'])}
      </address>
    </div>
  </div>
  <div class="wrap foot-base">
    <p>&copy; {e(SITE['year'])} {e(SITE['brand'])} {e(SITE['brand_sub'])}. Placeholder content — demo build.</p>
    <p>Licensing and regulatory disclosures go here.</p>
  </div>
</footer>
<script src="assets/js/site.js" defer></script>
</body>
</html>
"""


def page(page_file, title, description, body, extra_head=""):
    out = head(page_file, title, description, extra_head) + header(page_file) + body + footer()
    (DIST / page_file).write_text(out, encoding="utf-8")


# ---------------------------------------------------------------- pages

def build_home():
    values = "".join(
        f"""<article class="value-card">
      <svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="{p}"/></svg>
      <h3>{e(t)}</h3><p>{e(d)}</p>
    </article>"""
        for t, d, p in VALUES
    )
    stats = "".join(
        f'<div class="stat"><span class="stat-num">{e(n)}</span><span class="stat-lab">{e(l)}</span></div>'
        for n, l in STATS
    )
    practice = "".join(
        f'<article class="practice"><h3>{e(t)}</h3><p>{e(d)}</p></article>'
        for t, d in PRACTICE
    )
    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">{e(SITE['tagline'])}</p>
      <h1>Cover that is explained<br>before it is sold.</h1>
      <p class="lede">A short, confident positioning paragraph goes here — two sentences
      that tell a visitor what the agency does, who it does it for, and why that is
      worth a phone call. Replace with your own words.</p>
      <div class="hero-actions">
        <a class="btn" href="contact.html">Speak with an adviser</a>
        <a class="btn btn-ghost" href="about.html">Read our history</a>
      </div>
      <p class="hero-note">No forms to qualify you, no call centre. One adviser, start to finish.</p>
    </div>
    <div class="hero-art" aria-hidden="true">
      <svg viewBox="0 0 420 420" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="hg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stop-color="#1b3f5d"/><stop offset="1" stop-color="#0b1b2a"/>
          </linearGradient>
        </defs>
        <rect width="420" height="420" rx="4" fill="url(#hg)"/>
        <g stroke="rgba(255,255,255,.10)" stroke-width="1">
          <path d="M0 105h420M0 210h420M0 315h420M105 0v420M210 0v420M315 0v420"/>
        </g>
        <path d="M210 70l105 44v88c0 68-45 112-105 128-60-16-105-60-105-128v-88l105-44z"
              fill="none" stroke="#b8893c" stroke-width="2.5" stroke-opacity=".95"/>
        <path d="M210 110l66 28v60c0 45-29 74-66 86-37-12-66-41-66-86v-60l66-28z"
              fill="rgba(184,137,60,.12)"/>
        <path d="M178 208l24 24 46-50" fill="none" stroke="#e8c88b" stroke-width="4"
              stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap stat-row">{stats}</div>
</section>

<section class="section">
  <div class="wrap">
    <p class="eyebrow">What we stand for</p>
    <h2 class="section-title">Three commitments, in writing.</h2>
    <div class="value-grid">{values}</div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Where we work</p>
      <h2 class="section-title">Lines of business.</h2>
      <p class="lede">One paragraph framing the practice areas below — the sorts of
      risk the agency places most often and the clients it suits. Replace with your copy.</p>
      <a class="link-arrow" href="contact.html">Ask about your own cover</a>
    </div>
    <div class="practice-grid">{practice}</div>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <p class="eyebrow">Common questions</p>
    <h2 class="section-title">Before you call.</h2>
    <dl class="faq">
      {"".join(f"<dt>{e(q)}</dt><dd>{e(a)}</dd>" for q, a in FAQ)}
    </dl>
  </div>
</section>

<section class="cta">
  <div class="wrap cta-inner">
    <div>
      <h2>Ready when you are.</h2>
      <p>No obligation, no pressure. A short conversation about what you already have.</p>
    </div>
    <a class="btn btn-light" href="contact.html">Contact the office</a>
  </div>
</section>
"""
    page("index.html", "Independent Insurance Advisers",
         "Placeholder meta description for the home page — one sentence naming the agency, "
         "its location and the cover it places.", body)


def build_about():
    timeline = "".join(
        f"""<li>
      <span class="t-year">{e(y)}</span>
      <div><h3>{e(t)}</h3><p>{e(d)}</p></div>
    </li>"""
        for y, t, d in HISTORY
    )
    body = f"""
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">About us</p>
    <h1>A brokerage built around<br>one adviser per file.</h1>
    <p class="lede">Opening paragraph of the company story. Two or three sentences
    that set up the detail below. Replace with the real account.</p>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="prose">
      <h2>Who we are</h2>
      <p>Placeholder body copy. Describe the agency as it stands today: how many
      advisers, which markets, and the kind of client it serves best. Two or three
      paragraphs is the right length for this slot.</p>
      <p>A second paragraph can cover the approach — how a file is handled from
      first conversation through renewal, and what makes that different from a
      call-centre experience.</p>
      <h2>How we are paid</h2>
      <p>Placeholder paragraph. Stating this plainly, early, is one of the fastest
      ways to earn trust on an insurance site.</p>
    </div>
    <aside class="card-aside">
      <h2>At a glance</h2>
      <dl class="facts">
        <dt>Established</dt><dd>Placeholder</dd>
        <dt>Head office</dt><dd>{e(SITE['address_city'])}</dd>
        <dt>Advisers</dt><dd>Placeholder</dd>
        <dt>Licensed in</dt><dd>Placeholder</dd>
        <dt>Carrier panel</dt><dd>Placeholder</dd>
      </dl>
      <a class="link-arrow" href="team.html">Meet the team</a>
    </aside>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <p class="eyebrow">History</p>
    <h2 class="section-title">How the firm grew.</h2>
    <ol class="timeline">{timeline}</ol>
  </div>
</section>

<section class="section">
  <div class="wrap narrow prose">
    <p class="eyebrow">Values</p>
    <h2 class="section-title">What clients can hold us to.</h2>
    <p>Placeholder paragraph introducing the values. Keep it short — the three
    commitments on the home page already carry the message.</p>
    <ul class="ticks">
      <li>A written summary of cover, exclusions and deductibles before anything is bound.</li>
      <li>A named adviser and a direct line — not a queue.</li>
      <li>Claims advocacy on your side of the table.</li>
      <li>An annual review whether or not anything has changed.</li>
    </ul>
  </div>
</section>

<section class="cta">
  <div class="wrap cta-inner">
    <div><h2>Questions about your current policy?</h2>
    <p>Send it over. We will read it and tell you what we see.</p></div>
    <a class="btn btn-light" href="contact.html">Get in touch</a>
  </div>
</section>
"""
    page("about.html", "About Us",
         "Placeholder meta description for the About page — the agency's history, "
         "size and approach in one sentence.", body)


def build_team():
    cards = "".join(
        f"""<article class="person">
      <div class="person-photo">{monogram(initials, tone)}</div>
      <h3>{e(name)}</h3>
      <p class="role">{e(role)}</p>
      <p class="bio">{e(bio)}</p>
      <p class="person-contact"><a href="contact.html">Contact {e(name.split()[0])}</a></p>
    </article>"""
        for name, role, initials, tone, bio in TEAM
    )
    body = f"""
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Our team</p>
    <h1>The people behind the brand.</h1>
    <p class="lede">One short paragraph introducing the team. Placeholder portraits
    below are swapped for real photographs — any aspect ratio, they are cropped to
    a consistent square automatically.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2 class="section-title">Advisers and staff</h2>
    <div class="team-grid">{cards}</div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap narrow prose">
    <h2>Joining the practice</h2>
    <p>Placeholder paragraph for recruitment, or delete this block entirely — it is
    an optional section in the editor.</p>
    <a class="link-arrow" href="contact.html">Enquire about a role</a>
  </div>
</section>
"""
    page("team.html", "Our Team",
         "Placeholder meta description for the Team page — advisers, roles and "
         "specialisms.", body)


def build_contact():
    map_src = f"https://www.google.com/maps?q={SITE['map_query']}&output=embed"
    body = f"""
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1>Speak with an adviser.</h1>
    <p class="lede">A note setting expectations — who answers, and how quickly.
    Replace with your own wording.</p>
  </div>
</section>

<section class="section">
  <div class="wrap contact-grid">
    <div>
      <h2>Send a message</h2>
      <form class="form" novalidate>
        <div class="field">
          <label for="f-name">Full name <span aria-hidden="true">*</span></label>
          <input id="f-name" name="name" type="text" autocomplete="name" required
                 aria-describedby="e-name">
          <p class="err" id="e-name" hidden>Please tell us your name.</p>
        </div>
        <div class="field">
          <label for="f-email">Email <span aria-hidden="true">*</span></label>
          <input id="f-email" name="email" type="email" autocomplete="email" required
                 aria-describedby="e-email">
          <p class="err" id="e-email" hidden>Please enter a valid email address.</p>
        </div>
        <div class="field">
          <label for="f-phone">Phone <span class="opt">(optional)</span></label>
          <input id="f-phone" name="phone" type="tel" autocomplete="tel">
        </div>
        <div class="field">
          <label for="f-topic">What is this about?</label>
          <select id="f-topic" name="topic">
            <option>General enquiry</option>
            <option>Commercial lines</option>
            <option>Professional risk</option>
            <option>Group benefits</option>
            <option>Personal lines</option>
            <option>Existing policy / claim</option>
          </select>
        </div>
        <div class="field">
          <label for="f-msg">Message <span aria-hidden="true">*</span></label>
          <textarea id="f-msg" name="message" rows="5" required aria-describedby="e-msg"></textarea>
          <p class="err" id="e-msg" hidden>Please add a short message.</p>
        </div>
        <button class="btn" type="submit">Send message</button>
        <p class="form-note" role="status" id="form-status">Demo form — nothing is sent.
        On the live site this delivers to your inbox with spam protection.</p>
      </form>
    </div>
    <aside class="contact-aside">
      <h2>Office</h2>
      <address>
        <strong>{e(SITE['brand'])} {e(SITE['brand_sub'])}</strong><br>
        {e(SITE['address_line'])}<br>{e(SITE['address_city'])}
      </address>
      <dl class="facts">
        <dt>Telephone</dt><dd><a href="tel:0000000000">{e(SITE['phone'])}</a></dd>
        <dt>Hours</dt><dd>{e(SITE['hours'])}</dd>
        <dt>Parking</dt><dd>Placeholder detail</dd>
        <dt>Transit</dt><dd>Placeholder detail</dd>
      </dl>
      <p class="muted">Address and telephone are placeholders.</p>
    </aside>
  </div>
</section>

<section class="map-section" aria-label="Office location map">
  <div class="map-fallback" aria-hidden="true">
    <strong>Office location map</strong>
    <span>Loads once the real street address is in place.</span>
  </div>
  <iframe class="map" src="{e(map_src)}" title="Map showing the office location"
          loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
</section>
"""
    page("contact.html", "Contact",
         "Placeholder meta description for the Contact page — address, telephone, "
         "hours and a short message form.", body)


def write_assets():
    (DIST / "assets/img/favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        '<rect width="64" height="64" rx="10" fill="#0e2235"/>'
        '<text x="32" y="43" text-anchor="middle" font-family="Georgia,serif" '
        'font-size="30" fill="#b8893c">V</text></svg>',
        encoding="utf-8",
    )
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    (DIST / "robots.txt").write_text(
        "# Demo preview — not for indexing.\nUser-agent: *\nDisallow: /\n", encoding="utf-8"
    )
    shutil.copyfile(ROOT / "src/site.css", DIST / "assets/css/site.css")
    shutil.copyfile(ROOT / "src/site.js", DIST / "assets/js/site.js")


def main():
    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / "assets/css").mkdir(parents=True, exist_ok=True)
    (DIST / "assets/js").mkdir(parents=True, exist_ok=True)
    (DIST / "assets/img").mkdir(parents=True, exist_ok=True)
    build_home()
    build_about()
    build_team()
    build_contact()
    write_assets()
    for f in sorted(os.listdir(DIST)):
        print("  dist/" + f)
    print("built ok")


if __name__ == "__main__":
    main()
