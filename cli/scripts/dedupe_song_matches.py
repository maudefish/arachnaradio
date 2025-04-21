#🧹 dedupe_song_matches.py

import csv
from pathlib import Path

INPUT_PATH = Path("data/logs/song_matches.csv")
OUTPUT_PATH = Path("data/logs/song_matches_deduped.csv")

def dedupe_csv(input_path, output_path):
    with open(input_path, "r") as infile, open(output_path, "w", newline="") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        previous = None
        for row in reader:
            current = (row["title"], row["artist"], row["station"])
            if current != previous:
                writer.writerow(row)
            previous = current

    print(f"✅ Cleaned CSV written to {output_path}")

if __name__ == "__main__":
    dedupe_csv(INPUT_PATH, OUTPUT_PATH)
