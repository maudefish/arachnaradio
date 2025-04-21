import pandas as pd
import yaml
from pathlib import Path

MENTIONS_PATH = Path("data/logs/venue_mentions.csv")
ALIAS_PATH = Path("data/venue_aliases.yaml")

def load_venue_aliases(path: Path) -> dict:
    if path.exists():
        with open(path) as f:
            return yaml.safe_load(f)
    return {}

def resolve_canonical_venue(name: str, alias_map: dict) -> str:
    name_lower = name.strip().lower()
    for canonical, info in alias_map.items():
        if name_lower == canonical.lower():
            return canonical
        for alias in info.get("aliases", []):
            if name_lower == alias.lower():
                return canonical
    return None  # unmatched

def find_unmatched_venues():
    df = pd.read_csv(MENTIONS_PATH)
    if "venue" not in df.columns:
        print("No 'venue' column found in CSV.")
        return

    alias_map = load_venue_aliases(ALIAS_PATH)
    venue_names = df["venue"].dropna().unique()
    unmatched = set()

    for name in venue_names:
        if not resolve_canonical_venue(name, alias_map):
            unmatched.add(name)

    print("\n🧹 Unmatched Venue Names:")
    for venue in sorted(unmatched):
        print(f"  - {venue}")

    print(f"\nFound {len(unmatched)} unmatched out of {len(venue_names)} unique venues.")

if __name__ == "__main__":
    find_unmatched_venues()
# Compare stripped/lowered versions
master_names = set(df_master["name"].str.strip().str.lower())
log_names = set(df_logs["venue"].str.strip().str.lower())

print("Missing:", log_names - master_names)
