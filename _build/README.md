# Site source (not published)

The live HTML in the repo root is generated from these files.

- `gen.py` – page templates and copy (home, services, packages, FAQ, contact, thanks, areas)
- `services_data.py` – the 7 service pages
- `cities.py` – the 10 area pages
- `site.css` – all styles (inlined into each page at build time)
- `scenes.py` – generates the stage/broadcast images in `images/`

Rebuild: `python3 gen.py` writes pages to `out/`; copy `out/*.html` and `out/sitemap.xml` to the repo root.
Launch-pricing end date: `PROMO_END` in `gen.py`. Form key: `FORM_KEY` in `gen.py`.
