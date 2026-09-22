#!/usr/bin/env python3
"""Generira data/manifest.json iz sadržaja data/archive/ i briše zapise
starije od 30 dana. Pokreće ga GitHub Action svaki dan."""
import os
import json
import datetime

ARCHIVE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "archive")
MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "manifest.json")
KEEP_DAYS = 30


def main():
    today = datetime.date.today()
    cutoff = today - datetime.timedelta(days=KEEP_DAYS - 1)

    entries = []
    for fname in os.listdir(ARCHIVE_DIR):
        if not fname.endswith(".csv"):
            continue
        date_str = fname[:-4]
        try:
            file_date = datetime.date.fromisoformat(date_str)
        except ValueError:
            continue

        if file_date < cutoff:
            os.remove(os.path.join(ARCHIVE_DIR, fname))
            print(f"Obrisano (starije od {KEEP_DAYS} dana): {fname}")
            continue

        entries.append(date_str)

    entries.sort(reverse=True)
    manifest = [{"date": d, "file": f"archive/{d}.csv"} for d in entries]

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"manifest.json ažuriran, {len(manifest)} zapisa")


if __name__ == "__main__":
    main()
