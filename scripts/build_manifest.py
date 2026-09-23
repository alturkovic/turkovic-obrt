#!/usr/bin/env python3
"""Generira data/manifest.json iz sadržaja data/archive/ i briše zapise
starije od 30 dana. Pokreće ga GitHub Action svaki dan.

Očekivano ime arhivske datoteke: poslovnica-savska1-1-01-{YYYYMMDDHHMMSS}.csv
Prefiks (naziv poslovnice i broj) je fiksan, mijenja se samo timestamp.
"""
import os
import re
import json
import datetime

HERE = os.path.dirname(__file__)
ARCHIVE_DIR = os.path.join(HERE, "..", "data", "archive")
MANIFEST_PATH = os.path.join(HERE, "..", "data", "manifest.json")
KEEP_DAYS = 30

FILENAME_RE = re.compile(r"^poslovnica-savska1-1-01-(\d{14})\.csv$")


def main():
    today = datetime.date.today()
    cutoff = today - datetime.timedelta(days=KEEP_DAYS - 1)

    entries = []
    for fname in os.listdir(ARCHIVE_DIR):
        m = FILENAME_RE.match(fname)
        if not m:
            continue
        ts = m.group(1)
        try:
            dt = datetime.datetime.strptime(ts, "%Y%m%d%H%M%S")
        except ValueError:
            continue

        if dt.date() < cutoff:
            os.remove(os.path.join(ARCHIVE_DIR, fname))
            print(f"Obrisano (starije od {KEEP_DAYS} dana): {fname}")
            continue

        entries.append((dt, fname))

    entries.sort(key=lambda e: e[0], reverse=True)
    manifest = [
        {"date": dt.date().isoformat(), "timestamp": dt.strftime("%Y-%m-%d %H:%M UTC"), "file": "archive/" + fname}
        for dt, fname in entries
    ]

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"manifest.json ažuriran, {len(manifest)} zapisa")


if __name__ == "__main__":
    main()
