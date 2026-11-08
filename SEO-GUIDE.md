# SEO guide: N Maphikana Plumbing

Nobody can guarantee a #1 position on Google. The website is now built the way Google
recommends for local businesses; the steps below are what moves it up the results.
For local searches ("plumber Kuils River", "burst geyser near me"), the **Google
Business Profile** and **reviews** matter as much as the website.

## What the website already has

- `sitemap.xml` and `robots.txt` listing every page.
- One page per service, each with its own title, description, content, FAQ and price:
  `/services/emergency-plumbing/`, `/services/burst-geysers/`, `/services/burst-pipes/`,
  `/services/geyser-installation-repair/`, `/services/heat-pumps/`, `/services/solar-panels/`,
  `/services/bathrooms/`, `/services/blocked-drainage/`.
- An areas page (`/areas/`) and an "Areas we serve" section on the home page.
- Structured data Google reads: Plumber (LocalBusiness), Service, FAQ and Breadcrumbs.
- Canonical URLs, Open Graph/Twitter preview image (`assets/img/og-image.jpg`), fast WebP images.

## 1. Before you publish

1. **Buy a domain**, ideally `.co.za` (for example `nmaphikanaplumbing.co.za`).
2. Open `tools/build_seo.py`, set `SITE = "https://www.your-domain.co.za"`, and run:
   ```bash
   python3 tools/build_seo.py
   ```
   Also replace `https://www.nmaphikanaplumbing.co.za` in `index.html` (canonical, og:url,
   og:image and the JSON-LD block) with the same domain.
3. Host it with HTTPS (Netlify, Vercel, Cloudflare Pages or your web host all work).
4. Replace the remaining placeholders: PIRB number `000000`, and confirm the prices.

## 2. Google Search Console (free)

1. Go to <https://search.google.com/search-console> and add your domain.
2. Verify ownership (DNS record or HTML file).
3. **Sitemaps → submit** `sitemap.xml`.
4. Use **URL Inspection → Request indexing** for the home page and each service page.

## 3. Google Business Profile (most important for "near me" searches)

1. Make sure the **name, address and phone** are exactly the same everywhere
   (website, Google, Facebook, directories). Right now Google shows
   *25346 Plajjte Street, Wallace's Dene, Kraaifontein* but the website shows
   *33 Pama Cres, St Dumas, 7580*. Pick one and update the other.
2. Primary category: **Plumber**. Add secondary categories such as
   *Drainage service*, *Water heater installation service*, *Solar hot water system supplier*,
   *Bathroom remodeler*.
3. Add every service (geyser installation, burst geysers, heat pumps, solar, bathrooms,
   blocked drains, burst pipes, emergency plumbing) and your **service areas**
   (Kuils River, Kraaifontein, Brackenfell, Bellville, Durbanville, Blue Downs, Eerste River…).
4. Add the website link, hours (Open 24 hours), logo and **at least 10 real job photos**.
5. Post an update or photo every week.

## 4. Reviews

- Ask every happy customer for a Google review. Send them this link on WhatsApp:
  `https://search.google.com/local/writereview?placeid=ChIJA0LNvH5TzB0RRniq-S024cQ`
- Reply to every review. Ask customers to mention the service and suburb
  ("fixed our burst geyser in Kuils River") — never write or buy fake reviews.

## 5. Directory listings (citations)

List the business with the same name, address and phone on: Yellow Pages SA, Brabys,
Snupit, Cylex South Africa, Hotfrog ZA, Facebook Page, Bing Places and Apple Business Connect.

## 6. Keep it growing

- Add real project photos and short write-ups ("Heat pump install in Brackenfell").
- Share the service pages on Facebook and WhatsApp status.
- Check Search Console monthly to see which searches show the site and improve those pages.
