#!/usr/bin/env python3
"""Build SEO pages for N Maphikana Plumbing.

Generates:
  services/<slug>/index.html   one landing page per service (unique content + schema)
  areas/index.html             service-area page
  sitemap.xml, robots.txt
It reuses the header, mobile menu and footer from index.html so every page stays
in sync. Re-run after editing index.html or this file:

    python3 tools/build_seo.py

Set SITE to the live domain before publishing (used for canonical URLs, the
sitemap and structured data).
"""
import html
import json
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.nmaphikanaplumbing.co.za"  # <-- change to the real domain
TODAY = date.today().isoformat()

BUSINESS = "N Maphikana Plumbing"
PHONE_DISPLAY = "073 430 2133"
PHONE_INTL = "+27734302133"
WHATSAPP = "https://wa.me/27734302133"
EMAIL = "bolonjabs@gmail.com"
MAPS = "https://www.google.com/maps/place/?q=place_id:ChIJA0LNvH5TzB0RRniq-S024cQ"

AREAS = [
    "St Dumas", "Kuils River", "Kraaifontein", "Wallacedene", "Brackenfell",
    "Bellville", "Durbanville", "Blue Downs", "Eerste River", "Kleinvlei",
    "Scottsdene", "Zevenwacht", "Haasendal", "Sarepta", "Delft",
    "Cape Town Northern Suburbs",
]

SERVICES = [
    {
        "slug": "emergency-plumbing", "name": "Emergency Plumbing", "img": "emergency-valve.webp",
        "img_alt": "Red valve wheel on pipework", "price": "R450", "price_note": "call-out fee, waived if you go ahead with the repair",
        "title": "24/7 Emergency Plumber Kuils River & Cape Town | N Maphikana Plumbing",
        "desc": "Emergency plumber in Kuils River, St Dumas, Kraaifontein & Cape Town, open 24/7. Burst pipes, burst geysers, floods & sewer backups. Call 073 430 2133.",
        "h1": "24/7 Emergency Plumber in Kuils River &amp; Cape Town",
        "lead": "Burst pipe, flooding or no water? We answer day and night, 7 days a week, and send a plumber to you.",
        "intro": [
            "Plumbing emergencies never happen at a convenient time. Whether it's 2am on a Sunday or a public holiday, N Maphikana Plumbing answers the phone and sends a plumber to stop the damage and fix the problem.",
            "We handle every kind of urgent plumbing job across St Dumas, Kuils River, Kraaifontein and the Cape Town northern suburbs, and we always explain the cost before work begins.",
        ],
        "what": ["Burst and leaking pipes isolated and repaired", "Burst geysers made safe and replaced", "Overflowing or blocked toilets", "Sewer and drain backups",
                 "Taps and valves that won't close", "Water shut-off and damage control"],
        "signs_title": "When to call an emergency plumber",
        "signs": ["Water coming through a ceiling or wall", "No hot or cold water in the house", "Sewage backing up or a strong drain smell",
                  "Your water meter keeps running with every tap closed", "Water pouring from the geyser overflow pipe"],
        "faqs": [
            ("How quickly can you get to me?", "We dispatch a plumber as soon as you call and give you an estimated arrival time on the phone. Call or WhatsApp 073 430 2133 any time, day or night."),
            ("What should I do while I wait?", "Close your main water stopcock to stop the flow, and if the problem involves the geyser, switch the geyser off at the electrical distribution board."),
            ("Will I know the cost upfront?", "Yes. We tell you the call-out fee before we dispatch and give you a price for the repair before any work starts."),
        ],
    },
    {
        "slug": "burst-geysers", "name": "Burst Geysers", "img": "emergency.webp",
        "img_alt": "Water gushing from a tap", "price": "R8,950", "price_note": "150 L geyser supplied and installed with COC",
        "title": "Burst Geyser Replacement Kuils River & Cape Town | N Maphikana Plumbing",
        "desc": "Burst geyser in Kuils River, Kraaifontein or Cape Town? 24/7 geyser replacement with Certificate of Compliance and insurance claim help. Call 073 430 2133.",
        "h1": "Burst Geyser Replacement in Kuils River &amp; Cape Town",
        "lead": "We make a burst geyser safe, replace it to SANS 10252 with a Certificate of Compliance, and help with your insurance claim.",
        "intro": [
            "A burst geyser can soak ceilings, walls and furniture within minutes. Our plumbers isolate the water and electricity, remove the damaged unit and install a new geyser so you have hot water again as soon as possible.",
            "Because most burst geysers are covered by home insurance, we supply the damage report, photos, quote and Certificate of Compliance your insurer needs.",
        ],
        "what": ["Emergency isolation of water and power", "Removal and disposal of the old geyser", "Supply and installation of a new geyser",
                 "New pressure valve, vacuum breakers and drip tray", "Certificate of Compliance (COC)", "Insurance claim reports and photos"],
        "signs_title": "Signs your geyser has burst or is about to",
        "signs": ["Water dripping through the ceiling", "Constant dripping from the overflow pipe outside", "No hot water and the geyser keeps tripping",
                  "Rusty or discoloured hot water", "A bulging or damp ceiling board"],
        "faqs": [
            ("What should I do if my geyser bursts?", "Switch the geyser off at the distribution board, close the cold-water supply to the geyser (or the main stopcock) and call us on 073 430 2133."),
            ("Will you help with my insurance claim?", "Yes. We provide the damage report, photos, quote and Certificate of Compliance, and can liaise with your insurer directly."),
            ("How long does a geyser replacement take?", "In most cases we can replace a burst geyser on the same day, depending on access and stock of the right size."),
        ],
    },
    {
        "slug": "burst-pipes", "name": "Burst Pipes", "img": "pipes.webp",
        "img_alt": "Copper elbow pipe fittings", "price": "R950", "price_note": "starting price for a standard burst pipe repair",
        "title": "Burst Pipe Repairs Kuils River & Cape Town | N Maphikana Plumbing",
        "desc": "Fast burst pipe and leak repairs in Kuils River, St Dumas, Kraaifontein & Cape Town. Copper, PEX & PVC, walls, ceilings & gardens. 24/7: 073 430 2133.",
        "h1": "Burst Pipe Repairs in Kuils River &amp; Cape Town",
        "lead": "We find the leak, repair the pipe and pressure-test the system, opening up only what's needed.",
        "intro": [
            "Burst and leaking pipes waste water, push up your municipal bill and can cause serious damage to walls, floors and foundations if they're left alone.",
            "Our plumbers repair copper, PEX and PVC pipework inside walls, in ceilings, under floors and in gardens, and replace corroded sections so the problem doesn't come back.",
        ],
        "what": ["Locating hidden and underground leaks", "Repairing copper, PEX and PVC pipes", "Leaks inside walls and ceilings",
                 "Garden and underground supply pipes", "Replacing corroded pipe sections", "Pressure testing after repairs"],
        "signs_title": "Signs of a burst or leaking pipe",
        "signs": ["Damp patches or mould on walls or ceilings", "A water bill that's suddenly higher", "Low water pressure at the taps",
                  "The sound of running water when everything is off", "Wet or sinking spots in the garden"],
        "faqs": [
            ("Why do pipes burst?", "Common causes are old or corroded pipes, high water pressure, ground movement and tree roots. We'll tell you the cause and how to prevent it."),
            ("Will you have to break my walls?", "We open only as much as needed to reach the pipe, and we'll explain what will be opened before we start."),
            ("Can you lower my water pressure?", "Yes. If high pressure is causing leaks we can fit a pressure-reducing valve to protect your plumbing."),
        ],
    },
    {
        "slug": "geyser-installation-repair", "name": "Geyser Installation & Repair", "img": "geyser.webp",
        "img_alt": "Copper hot-water pipework with valves", "price": "R1,250", "price_note": "starting price for element and thermostat repairs",
        "title": "Geyser Installation & Repairs Kuils River & Cape Town | N Maphikana Plumbing",
        "desc": "Geyser installation and repairs in Kuils River, Kraaifontein, Brackenfell & Cape Town. Elements, thermostats, valves & new geysers with COC. 073 430 2133.",
        "h1": "Geyser Installation &amp; Repairs in Kuils River &amp; Cape Town",
        "lead": "New geysers, elements, thermostats and valves, installed to SANS 10252 with a Certificate of Compliance.",
        "intro": [
            "Your geyser is one of the hardest-working appliances in your home. We install new geysers and repair existing ones so you get reliable hot water without wasting electricity.",
            "Every installation is done to SANS 10252 and comes with a Certificate of Compliance where required.",
        ],
        "what": ["New geyser installations", "Element and thermostat replacement", "Pressure control valves and vacuum breakers",
                 "Drip trays and overflow pipes", "Geyser blankets and timers", "Certificate of Compliance (COC)"],
        "signs_title": "Signs your geyser needs attention",
        "signs": ["No hot water or only lukewarm water", "The geyser trips the distribution board", "Water dripping from the overflow pipe",
                  "Knocking or hissing noises", "Rust-coloured hot water"],
        "faqs": [
            ("How long does a geyser last?", "Most geysers last around 10 to 15 years, depending on water quality and maintenance. We can check yours and advise whether to repair or replace it."),
            ("Can a geyser timer save electricity?", "Yes. A timer heats water only when you need it, which can reduce your electricity use."),
            ("Do you issue a Certificate of Compliance?", "Yes. Geyser installations are done to SANS 10252 and we issue a COC where it's required."),
        ],
    },
    {
        "slug": "heat-pumps", "name": "Heat Pumps", "img": "heat-pump.webp",
        "img_alt": "Heating pump installation", "price": "R24,500", "price_note": "starting price, supplied and installed",
        "title": "Heat Pump Installation Kuils River & Cape Town | N Maphikana Plumbing",
        "desc": "Heat pump installation in Kuils River, St Dumas, Kraaifontein & Cape Town. Cut water-heating costs with an efficient heat pump. Free quote: 073 430 2133.",
        "h1": "Heat Pump Installation in Kuils River &amp; Cape Town",
        "lead": "Cut your water-heating costs with an energy-efficient heat pump, sized and installed for your household.",
        "intro": [
            "Water heating is one of the biggest costs on most electricity bills. A heat pump moves heat from the air into your water and can use around a third of the electricity of a standard geyser element.",
            "We size the heat pump for your household, connect it to your existing geyser where possible and set it up for the best efficiency.",
        ],
        "what": ["Household sizing and recommendations", "Heat pump supply and installation", "Retrofits to existing geysers",
                 "Timers and controls", "Servicing and maintenance", "Advice on combining with solar"],
        "signs_title": "A heat pump is a good fit if",
        "signs": ["Your electricity bill is high because of water heating", "Your household uses a lot of hot water",
                  "You want hot water that's less affected by load-shedding schedules", "Your geyser is due for replacement",
                  "Your roof isn't suitable for solar panels"],
        "faqs": [
            ("Do heat pumps work in winter?", "Yes. Heat pumps are designed for the Cape climate; efficiency drops slightly in cold weather but they still heat water effectively."),
            ("Can a heat pump connect to my existing geyser?", "In most homes, yes. We'll check your geyser's age and condition during the quote."),
            ("Are heat pumps noisy?", "Modern units run quietly, similar to an air-conditioner. We'll recommend a good spot to install it."),
        ],
    },
    {
        "slug": "solar-panels", "name": "Solar Panels", "img": "solar.webp",
        "img_alt": "Installers fitting solar panels on a roof", "price": "R32,000", "price_note": "starting price for a solar water heating system",
        "title": "Solar Geyser & Solar Panel Installation Kuils River & Cape Town | N Maphikana Plumbing",
        "desc": "Solar panel and solar geyser installation in Kuils River, Kraaifontein, Brackenfell & Cape Town. Hot water through load-shedding. Quote: 073 430 2133.",
        "h1": "Solar Panel &amp; Solar Geyser Installation in Kuils River &amp; Cape Town",
        "lead": "Use the Cape sun to heat your water and keep hot water flowing through load-shedding.",
        "intro": [
            "Solar water heating is one of the most effective ways to cut your electricity bill. We install solar geyser panels and solar water heating systems, and convert existing geysers to run on solar.",
            "We check your roof's orientation and space first, so the system we recommend actually works for your home.",
        ],
        "what": ["Solar water heating systems", "Evacuated tube and flat-plate collectors", "Converting existing geysers to solar",
                 "PV-assisted geyser systems", "Backup element and timer setup", "Maintenance and repairs"],
        "signs_title": "Solar is a good fit if",
        "signs": ["You have a north-facing roof with good sun", "You want lower electricity bills over the long term",
                  "You want hot water during load-shedding", "Your geyser is due for replacement", "You're planning to stay in your home"],
        "faqs": [
            ("Will I have hot water on cloudy days?", "Yes. Solar systems keep a backup element on a timer, so you still have hot water when the sun isn't strong."),
            ("Evacuated tubes or flat-plate panels?", "Both work well. Evacuated tubes perform better in colder weather; flat plates are robust and simple. We'll recommend the best fit for your home."),
            ("Can you check if my roof is suitable?", "Yes. We assess roof direction, angle, space and strength as part of the quote."),
        ],
    },
    {
        "slug": "bathrooms", "name": "Bathrooms", "img": "shower.webp",
        "img_alt": "Chrome hand shower running", "price": "R65,000", "price_note": "starting price for a full bathroom renovation",
        "title": "Bathroom Renovations & Installs Kuils River & Cape Town | N Maphikana Plumbing",
        "desc": "Bathroom renovations and plumbing installs in Kuils River, St Dumas, Kraaifontein & Cape Town. Showers, baths, toilets & basins. Quote: 073 430 2133.",
        "h1": "Bathroom Renovations &amp; Installs in Kuils River &amp; Cape Town",
        "lead": "From a new shower to a complete bathroom makeover, plumbed properly and finished neatly.",
        "intro": [
            "A bathroom renovation is only as good as the plumbing behind the walls. We handle the full plumbing side of your new bathroom, from moving pipes and drains to fitting your new fixtures.",
            "Tell us what you have in mind and we'll give you a clear quote and timeline before work begins.",
        ],
        "what": ["Complete bathroom renovations", "Walk-in showers and shower mixers", "Baths, including freestanding baths",
                 "Toilets and concealed cisterns", "Basins, vanities and taps", "Removal of old fittings"],
        "signs_title": "Time for a bathroom upgrade if",
        "signs": ["Taps and fittings keep leaking", "Low water pressure in the shower", "Cracked or stained basins, baths or toilets",
                  "Mould from poor drainage or leaks", "You want a more modern, easier-to-clean space"],
        "faqs": [
            ("How long does a bathroom renovation take?", "It depends on the size and scope of the job. We give you a timeline in your quote before work starts."),
            ("Can you work with my own design or fittings?", "Yes. We can install fittings you've chosen or help you choose ones that suit your budget."),
            ("Do you remove the old bathroom?", "Yes. We remove and dispose of old fittings as part of the job."),
        ],
    },
    {
        "slug": "blocked-drainage", "name": "Blocked Drainage", "img": "drains.webp",
        "img_alt": "Chrome bath mixer and drain", "price": "R850", "price_note": "starting price for drain unblocking",
        "title": "Blocked Drains Kuils River & Cape Town | Drain Unblocking 24/7 | N Maphikana Plumbing",
        "desc": "Blocked drain or toilet in Kuils River, St Dumas, Kraaifontein or Cape Town? 24/7 drain unblocking, jetting & CCTV inspections. Call 073 430 2133.",
        "h1": "Blocked Drains &amp; Drain Unblocking in Kuils River &amp; Cape Town",
        "lead": "Blocked sinks, toilets, showers and sewer lines cleared fast, day or night.",
        "intro": [
            "A blocked drain quickly becomes a smelly, unhygienic problem. We clear blockages in kitchens, bathrooms and main sewer lines using the right equipment for the job.",
            "Where blockages keep coming back, we can inspect the line with a drain camera to find the real cause.",
        ],
        "what": ["Blocked sinks, basins and showers", "Blocked and overflowing toilets", "Main sewer line blockages",
                 "Electric eel drain clearing", "High-pressure drain jetting", "CCTV drain inspections and root removal"],
        "signs_title": "Signs of a blocked drain",
        "signs": ["Water draining slowly from sinks or showers", "Gurgling sounds from drains or the toilet", "Bad smells from drains",
                  "Water backing up into the bath or shower", "An overflowing gully outside"],
        "faqs": [
            ("What causes blocked drains?", "Fat and oil, wet wipes, hair, food waste and tree roots are the most common causes."),
            ("Should I use chemical drain cleaners?", "We don't recommend them. They can damage pipes and often don't clear the blockage. Call us instead."),
            ("What is a CCTV drain inspection?", "We send a small camera down the drain to see exactly what's causing the problem, so we can fix it properly."),
        ],
    },
]


def esc(s):
    return html.escape(s, quote=True)


def plain(s):
    return html.unescape(s)


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def relink(fragment, prefix):
    """Point in-page anchors and asset paths at the home page from a sub-folder."""
    fragment = fragment.replace('href="#top"', f'href="{prefix}"')
    fragment = re.sub(r'href="#', f'href="{prefix}#', fragment)
    fragment = re.sub(r'(src|href)="(assets/|services/|areas/)', lambda m: f'{m.group(1)}="{prefix}{m.group(2)}', fragment)
    return fragment


INDEX = read("index.html")
CHROME_TOP = INDEX[INDEX.index('  <div class="progress"'):INDEX.index('  <main id="main">')]
CHROME_BOTTOM = INDEX[INDEX.index('  <footer class="footer">'):INDEX.index('</body>')]
FONTS = INDEX[INDEX.index('  <link rel="preconnect" href="https://fonts.googleapis.com">'):INDEX.index('  <link rel="preload"')]

PHONE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.3a1 1 0 01.9.7l1.5 4.5a1 1 0 01-.5 1.2l-2.3 1.1a11 11 0 005.5 5.5l1.1-2.3a1 1 0 011.2-.5l4.5 1.5a1 1 0 01.7 1V19a2 2 0 01-2 2h-1C9.7 21 3 14.3 3 6V5z"/></svg>'
CHECK_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path stroke-linecap="round" stroke-linejoin="round" d="M8 12.5l2.5 2.5L16 9.5"/></svg>'
ALERT_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01M10.3 3.9L1.8 18a2 2 0 001.7 3h17a2 2 0 001.7-3L13.7 3.9a2 2 0 00-3.4 0z"/></svg>'


def head(title, desc, canonical, prefix, ld, image="assets/img/og-image.jpg"):
    return f"""<!DOCTYPE html>
<html lang="en-ZA">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#06222a">
  <meta name="geo.region" content="ZA-WC">
  <meta name="geo.placename" content="Kuils River, Cape Town">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="en_ZA">
  <meta property="og:site_name" content="{BUSINESS}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/{image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(desc)}">
  <meta name="twitter:image" content="{SITE}/{image}">
{FONTS}  <link rel="icon" type="image/png" href="{prefix}assets/img/favicon.png">
  <link rel="apple-touch-icon" href="{prefix}assets/img/apple-touch-icon.png">
  <link rel="stylesheet" href="{prefix}assets/css/style.css">
  <script>
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) document.documentElement.classList.add('js-anim');
  </script>
  <script type="application/ld+json">
{json.dumps(ld, indent=2, ensure_ascii=False)}
  </script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
"""


def page_hero(prefix, img, alt, crumbs, eyebrow, h1, lead):
    crumb_html = " <span aria-hidden=\"true\">/</span> ".join(
        f'<a href="{href}">{label}</a>' if href else f'<span aria-current="page">{label}</span>' for label, href in crumbs)
    return f"""    <section class="page-hero">
      <div class="page-hero__media"><img id="heroImg" src="{prefix}assets/img/{img}" alt="{esc(alt)}" fetchpriority="high"></div>
      <div class="container page-hero__content">
        <nav class="breadcrumbs" aria-label="Breadcrumb" data-hero>{crumb_html}</nav>
        <span class="eyebrow" data-hero>{eyebrow}</span>
        <h1 data-hero>{h1}</h1>
        <p class="hero__lead" data-hero>{lead}</p>
        <div class="hero__ctas" data-hero>
          <a class="btn btn--gold" href="tel:{PHONE_INTL}">{PHONE_SVG} Call {PHONE_DISPLAY}</a>
          <a class="btn btn--ghost" href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp us</a>
        </div>
      </div>
    </section>
"""


def areas_block(prefix, heading="Areas we serve"):
    chips = "".join(f'<li>{a}</li>' for a in AREAS)
    return f"""    <section class="section section--paper">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow" data-reveal>Service area</span>
          <h2 data-reveal>{heading}</h2>
          <p data-reveal>We're based in St Dumas, Kuils River, and work across the Cape Town northern and eastern suburbs, 24 hours a day, 7 days a week.</p>
        </div>
        <ul class="chips" data-reveal>{chips}</ul>
        <p class="areas-more" data-reveal><a href="{prefix}areas/">See all areas we serve &rarr;</a></p>
      </div>
    </section>
"""


def business_ref():
    return {"@type": "Plumber", "@id": f"{SITE}/#business", "name": BUSINESS}


def service_page(svc):
    prefix = "../../"
    url = f"{SITE}/services/{svc['slug']}/"
    name_plain = plain(svc["name"])
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service",
                "@id": url + "#service",
                "name": name_plain,
                "serviceType": name_plain,
                "description": svc["desc"],
                "url": url,
                "provider": business_ref(),
                "areaServed": [{"@type": "Place", "name": a} for a in AREAS],
                "offers": {"@type": "Offer", "priceCurrency": "ZAR", "price": svc["price"].replace("R", "").replace(",", ""),
                           "description": "From " + svc["price"] + " (" + svc["price_note"] + ")"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Services", "item": SITE + "/#services"},
                    {"@type": "ListItem", "position": 3, "name": name_plain, "item": url},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in svc["faqs"]],
            },
        ],
    }
    what = "".join(f"<li>{CHECK_SVG}{w}</li>" for w in svc["what"])
    signs = "".join(f"<li>{ALERT_SVG}{s}</li>" for s in svc["signs"])
    intro = "".join(f"<p data-reveal>{p}</p>" for p in svc["intro"])
    faqs = "".join(
        f'<details{" open" if i == 0 else ""}><summary>{esc(q)}<i aria-hidden="true"></i></summary><p>{esc(a)}</p></details>'
        for i, (q, a) in enumerate(svc["faqs"]))
    others = "".join(
        f'<li><a href="{prefix}services/{o["slug"]}/">{o["name"].replace("&", "&amp;")}</a></li>' for o in SERVICES if o["slug"] != svc["slug"])
    body = f"""  <main id="main">
{page_hero(prefix, svc['img'], svc['img_alt'], [("Home", prefix), ("Services", prefix + "#services"), (svc['name'].replace('&', '&amp;'), None)],
           "24/7 · St Dumas, Kuils River &amp; Cape Town", svc['h1'], svc['lead'])}
    <section class="section">
      <div class="container svc-layout">
        <article class="svc-body">
          <h2 data-reveal>{svc['name'].replace('&', '&amp;')} by N Maphikana Plumbing</h2>
          {intro}
          <h3 data-reveal>What we do</h3>
          <ul class="checks" data-reveal>{what}</ul>
          <h3 data-reveal>{svc['signs_title']}</h3>
          <ul class="checks checks--warn" data-reveal>{signs}</ul>
          <h3 data-reveal>Frequently asked questions</h3>
          <div class="faq" data-reveal>{faqs}</div>
        </article>
        <aside class="svc-aside">
          <div class="price-card" data-reveal>
            <small>Starting from</small>
            <strong>{svc['price']}</strong>
            <span>{svc['price_note']} · incl. VAT</span>
            <a class="btn btn--gold btn--block" href="tel:{PHONE_INTL}">{PHONE_SVG} Call {PHONE_DISPLAY}</a>
            <a class="btn btn--outline btn--block" href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp for a quote</a>
            <p>Open 24 hours, 7 days a week. Your final price is confirmed before any work starts.</p>
          </div>
          <div class="aside-card" data-reveal>
            <h3>Other services</h3>
            <ul>{others}</ul>
          </div>
        </aside>
      </div>
    </section>
{areas_block(prefix, "Plumbers near you")}  </main>

"""
    page = head(svc["title"], svc["desc"], url, prefix, ld, image="assets/img/og-image.jpg")
    page += relink(CHROME_TOP, prefix) + "\n" + body + relink(CHROME_BOTTOM, prefix) + "</body>\n</html>\n"
    write(f"services/{svc['slug']}/index.html", page)


def areas_page():
    prefix = "../"
    url = f"{SITE}/areas/"
    title = "Plumber in Kuils River, Kraaifontein, Brackenfell & Bellville | N Maphikana Plumbing"
    desc = "24/7 plumber serving St Dumas, Kuils River, Kraaifontein, Brackenfell, Bellville, Durbanville, Blue Downs & Eerste River. Call or WhatsApp 073 430 2133."
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {**business_ref(), "areaServed": [{"@type": "Place", "name": a} for a in AREAS], "url": SITE + "/", "telephone": PHONE_INTL},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Areas we serve", "item": url}]},
        ],
    }
    cards = "".join(
        f'<article class="area-card" data-reveal><h3>Plumber in {a}</h3><p>Emergency plumbing, geysers, burst pipes, blocked drains, heat pumps, solar and bathrooms in {a}. Open 24/7.</p>'
        f'<a href="tel:{PHONE_INTL}">Call {PHONE_DISPLAY}</a></article>' for a in AREAS)
    svc_links = "".join(f'<li><a href="{prefix}services/{s["slug"]}/">{s["name"].replace("&", "&amp;")}</a></li>' for s in SERVICES)
    q = "33+Pama+Cres,+St+Dumas,+Western+Cape,+7580"
    body = f"""  <main id="main">
{page_hero(prefix, "hero.webp", "Modern bathroom", [("Home", prefix), ("Areas we serve", None)],
           "Open 24 hours · 7 days a week", "Plumber in Kuils River, Kraaifontein &amp; the Cape Town Northern Suburbs",
           "Based in St Dumas, Kuils River, we bring every plumbing service to homes and businesses across the area.")}
    <section class="section">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow" data-reveal>Where we work</span>
          <h2 data-reveal>Local plumbers, <em>close to you.</em></h2>
          <p data-reveal>Wherever you are in the areas below, call or WhatsApp {PHONE_DISPLAY} for a quote based on what you need.</p>
        </div>
        <div class="areas-grid">{cards}</div>
      </div>
    </section>
    <section class="section section--paper">
      <div class="container svc-layout">
        <div>
          <div class="section-head" style="margin-bottom:24px">
            <span class="eyebrow" data-reveal>Our services</span>
            <h2 data-reveal>Everything we do, <em>in every area.</em></h2>
          </div>
          <ul class="link-list" data-reveal>{svc_links}</ul>
        </div>
        <div class="map map--light" data-reveal>
          <iframe title="Map showing {BUSINESS} in St Dumas, Kuils River" src="https://www.google.com/maps?q={q}&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
      </div>
    </section>
  </main>

"""
    page = head(title, desc, url, prefix, ld)
    page += relink(CHROME_TOP, prefix) + "\n" + body + relink(CHROME_BOTTOM, prefix) + "</body>\n</html>\n"
    write("areas/index.html", page)


def sitemap():
    urls = [(SITE + "/", "1.0", "weekly")]
    urls += [(f"{SITE}/services/{s['slug']}/", "0.9", "monthly") for s in SERVICES]
    urls += [(f"{SITE}/areas/", "0.8", "monthly")]
    items = "\n".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>{f}</changefreq>\n    <priority>{p}</priority>\n  </url>"
        for u, p, f in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /tools/\nDisallow: /.claude/\n\nSitemap: {SITE}/sitemap.xml\n")


if __name__ == "__main__":
    for s in SERVICES:
        service_page(s)
    areas_page()
    sitemap()
    print(f"Built {len(SERVICES)} service pages, areas page, sitemap.xml and robots.txt for {SITE}")
