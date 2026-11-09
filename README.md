# bijboergilles.be

Website van Bij Boer Gilles (vzw De Boer Gilles Mobiel), kinderboerderij in Afsnee (Gent).

- `src/data.json`: prijzen, adres, links. Pas prijzen alleen hier aan.
- `src/pages/*.html`: de inhoud per pagina (kopregels, dan `---`, dan HTML).
- `src/layout.html`: menu en voettekst voor alle pagina's.
- `python3 build.py`: bouwt alles naar `docs/`. Die map wordt gepubliceerd (GitHub Pages, branch `main`, map `/docs`).
- Formulieren gaan via formsubmit.co naar het adres in src/data.json (info@bijboergilles.be). De eerste inzending vraagt eenmalig een bevestiging per mail.
