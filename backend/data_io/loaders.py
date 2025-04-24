# backend/data_io/loaders.py

from pathlib import Path
import yaml
import pandas as pd

def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}

def load_known_artists(path: Path) -> list[str]:
    data = load_yaml(path)
    return data.get("known_artists", [])

def load_known_venues(path: Path) -> tuple[list[str], dict]:
    data = load_yaml(path)
    return list(data.keys()), data  # ✅ known_venues, alias_data
def load_venue_aliases(path: Path) -> dict:
    return load_yaml(path)

def load_csv(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    else:
        return pd.DataFrame()
