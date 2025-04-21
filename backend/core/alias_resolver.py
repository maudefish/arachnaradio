import yaml
from pathlib import Path
from typing import Optional
from rapidfuzz import process, fuzz

# Paths
ALIAS_FILE = Path("data/venue_aliases.yaml")

def load_aliases() -> dict:
    if ALIAS_FILE.exists():
        with open(ALIAS_FILE, "r") as f:
            return yaml.safe_load(f) or {}
    return {}

def save_aliases(aliases: dict):
    ALIAS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ALIAS_FILE, "w") as f:
        yaml.dump(aliases, f, sort_keys=True)

def resolve_canonical_name(input_name: str, aliases: Optional[dict] = None, master_list: Optional[list] = None, threshold: int = 92) -> str:
    """
    Resolve the canonical venue name for an input, using exact and fuzzy alias matching.

    Args:
        input_name (str): The input venue name to resolve.
        aliases (dict): Optional preloaded alias dictionary.
        master_list (list): Optional master venue list for fuzzy fallback.
        threshold (int): Minimum fuzzy match score to accept.

    Returns:
        str: Canonical venue name if resolved, else original name.
    """
    input_norm = input_name.strip().lower()

    if aliases is None:
        aliases = load_aliases()

    # 1. Exact alias match
    for canonical, alt_names in aliases.items():
        all_aliases = [canonical.lower()] + [a.lower() for a in alt_names.get("aliases", [])]
        if input_norm in all_aliases:
            return canonical

    # 2. Fuzzy match against known aliases
    alias_lookup = {
        alias: canonical
        for canonical, alt in aliases.items()
        for alias in [canonical] + alt.get("aliases", [])
    }

    match, score, _ = process.extractOne(
        input_name, alias_lookup.keys(), scorer=fuzz.WRatio
    )
    if score >= threshold:
        return alias_lookup[match]

    # 3. Fuzzy match against master venue list if provided
    if master_list:
        match, score, _ = process.extractOne(input_name, master_list, scorer=fuzz.WRatio)
        if score >= threshold:
            return match

    return input_name  # fallback to original


def maybe_add_alias_to_yaml(canonical_name: str, alias: str):
    with open("data/aliases.yaml", "r") as f:
        aliases = yaml.safe_load(f)

    if canonical_name not in aliases:
        aliases[canonical_name] = {"aliases": []}

    if alias not in aliases[canonical_name]["aliases"]:
        aliases[canonical_name]["aliases"].append(alias)
        with open("data/aliases.yaml", "w") as f:
            yaml.dump(aliases, f)
        print(f"✨ Added new alias '{alias}' for '{canonical_name}'")

