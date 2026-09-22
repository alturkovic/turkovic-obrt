# Turković — web stranica

Statična stranica spremna za GitHub Pages, s automatskom dnevnom arhivom
cjenika u CSV obliku.

## Struktura

- `index.html`, `style.css`, `assets/` — sama stranica
- `data/cjenik.csv` — **izvor istine** za trenutne cijene. Kad mijenjate
  cijenu, uređujete ovu datoteku (format: `Proizvod;Cijena (EUR)`,
  decimalni zarez, `;` kao separator).
- `data/archive/YYYY-MM-DD.csv` — dnevni snapshotovi cjenika, zadnjih 30 dana
- `data/manifest.json` — popis dostupnih arhivskih datuma, čita ga stranica
- `.github/workflows/daily-cjenik.yml` — Action koja svaki dan generira
  novi snapshot (i kad nema promjena), briše zapise starije od 30 dana i
  ažurira manifest
- `scripts/build_manifest.py` — skripta koju Action pokreće

## Postavljanje

1. Napravite novi GitHub repozitorij i pushajte ovaj sadržaj u granu `main`.
2. U repozitoriju: **Settings → Pages → Build and deployment → Source:
   Deploy from a branch**, grana `main`, folder `/ (root)`.
3. **Settings → Actions → General → Workflow permissions**: postavite na
   "Read and write permissions" (potrebno da Action može commitati
   dnevni snapshot).
4. Workflow se pokreće automatski svaki dan u 05:00 UTC (07:00 CEST /
   06:00 CET, dakle prije 8h ujutro po hrvatskom vremenu, s rezervom).
   Možete ga i ručno pokrenuti: **Actions → Dnevni cjenik snapshot →
   Run workflow**.

## Važna napomena o pouzdanosti rasporeda

GitHub Actions `schedule` (cron) **nije jamčeno točan do minute** — u
razdobljima velikog opterećenja GitHuba pokretanje zna kasniti (rijetko i
desetak minuta). Za apsolutnu pravnu sigurnost oko roka "do 8h ujutro"
razmislite o dodatnom vanjskom "watchdogu" (npr. usluga poput
cron-job.org koja pozove `workflow_dispatch` preko GitHub API-ja u ranije
vrijeme, ili internom serveru s vlastitim cronom) kao rezervi.

## Ažuriranje cijena

Kad promijenite cijenu, samo uredite `data/cjenik.csv` i pushajte —
sljedeći dnevni snapshot (ili ručno pokrenut workflow) uhvatit će novu
vrijednost. Sama stranica uvijek nudi na preuzimanje **trenutni**
`data/cjenik.csv`, dok tablica "Arhiva" ispod njega prikazuje povijest
zadnjih 30 dana.
