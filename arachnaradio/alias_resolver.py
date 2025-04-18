from pathlib import Path
import yaml
from functools import lru_cache

# Path to your YAML file with aliases
ALIAS_PATH = Path("data/venue_aliases.yaml")

@lru_cache(maxsize=1)
def load_aliases() -> dict:
    if not ALIAS_PATH.exists():
        return {}
    with open(ALIAS_PATH, "r") as f:
        return yaml.safe_load(f) or {}

def resolve_venue_name(venue_name: str) -> list:
    """
    Returns all aliases for a given venue name, including the name itself.
    If no aliases are found, returns a list with just the name.
    """
    aliases_map = load_aliases()
    entry = aliases_map.get(venue_name, {})
    aliases = entry.get("aliases", [])
    return list(set([venue_name] + aliases))
