# Turković — web stranica

Statična stranica spremna za GitHub Pages, s automatskom dnevnom arhivom
cjenika u CSV obliku (sukladno Zakonu o obveznom isticanju sidrene cijene).

## Struktura

- `index.html`, `style.css`, `assets/` — sama stranica
- `data/izvor-cijena.csv` — **izvor istine** za cijene. Format prati stvarni
  export format (Sifra;Naziv;Jedinicna mjera;Trenutna cijena;Sidrena cijena,
  `;`-odvojeno, decimalni zarez). Kad mijenjate cijenu proizvoda, uređujete
  **samo stupac "Trenutna cijena"** u ovoj datoteci.
  **Stupac "Sidrena cijena" se NE mijenja** — to je fiksna referentna
  (najniža) cijena i ostaje onakva kakva je unesena, zauvijek.
- `data/archive/poslovnica-savska1-1-01-{timestamp}.csv` — dnevni snapshotovi
  cjenika, zadnjih 30 dana. Naziv datoteke prati fiksni obrazac: prefiks
  (naziv poslovnice i broj) je uvijek isti, mijenja se samo timestamp
  (format `YYYYMMDDHHMMSS`).
- `data/manifest.json` — popis dostupnih arhivskih datuma i imena datoteka,
  čita ga stranica da prikaže arhivu i odredi koji je najnoviji CSV
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

Ako u tabu **Actions** ne vidite "Dnevni cjenik snapshot" nego samo
"pages build and deployment" — to znači da `.github/workflows/` folder
još nije stvarno pushan u repozitorij. Provjerite da je taj folder (i
skrivene datoteke unutra) doista commitan; GitHub katkad ne prikaže
workflow dok barem jednom ne detektira `.yml` datoteku na `main` grani.

## Važna napomena o pouzdanosti rasporeda

GitHub Actions `schedule` (cron) **nije jamčeno točan do minute** — u
razdobljima velikog opterećenja GitHuba pokretanje zna kasniti (rijetko i
desetak minuta). Za apsolutnu pravnu sigurnost oko roka "do 8h ujutro"
razmislite o dodatnom vanjskom "watchdogu" (npr. usluga poput
cron-job.org koja pozove `workflow_dispatch` preko GitHub API-ja u ranije
vrijeme, ili internom serveru s vlastitim cronom) kao rezervi.

## Ažuriranje cijena

Kad promijenite cijenu, uredite **samo stupac "Trenutna cijena"** u
`data/izvor-cijena.csv` i pushajte — sljedeći dnevni snapshot (ili ručno
pokrenut workflow) uhvatit će novu vrijednost pod novim, ispravno
imenovanim CSV-om. Sidrenu cijenu ne dirajte.
