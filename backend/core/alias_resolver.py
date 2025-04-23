from pyprojroot import here
import yaml
from pathlib import Path
from typing import Optional
from rapidfuzz import process, fuzz

# Paths
ALIAS_FILE = here("data/masters/venue_aliases.yaml")


def load_aliases() -> dict:
    if ALIAS_FILE.exists():
        with open(ALIAS_FILE, "r") as f:
            return yaml.safe_load(f) or {}
    return {}

def save_aliases(aliases: dict):
    ALIAS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ALIAS_FILE, "w") as f:
        yaml.dump(aliases, f, sort_keys=True)
def resolve_canonical_name(input_name: str, aliases: Optional[dict] = None, master_list: Optional[list] = None, threshold: int = 92, debug: bool = False) -> str:
    input_norm = input_name.strip().lower()

    if len(input_norm) < 3 or not any(c.isalpha() for c in input_norm):
        if debug:
            print(f"❌ Skipping bad input: '{input_name}'")
        return input_name

    if aliases is None:
        aliases = load_aliases()

    # 1. Exact match
    for canonical, alt_names in aliases.items():
        all_aliases = [canonical.lower()] + [a.lower() for a in alt_names.get("aliases", [])]
        if input_norm in all_aliases:
            return canonical

    # 2. Fuzzy alias matching
    alias_lookup = {
        alias: canonical
        for canonical, alt in aliases.items()
        for alias in [canonical] + alt.get("aliases", [])
    }

    result = process.extractOne(input_name, alias_lookup.keys(), scorer=fuzz.WRatio)
    if result:
        match, score, _ = result
    else:
        match, score = None, 0  # or handle however you want

    if debug:
        print(f"🤖 Fuzzy match: '{input_name}' → '{match}' (score: {score})")

    if score >= threshold:
        return alias_lookup[match]

    # 3. Fuzzy match against master list
    if master_list:
        match, score, _ = process.extractOne(input_name, master_list, scorer=fuzz.WRatio)
        if score >= threshold:
            return match

    return input_name


def maybe_add_alias_to_yaml(canonical_name: str, alias: str):
    if len(alias.strip()) < 2:
        return  # Skip suspiciously short aliases

    print(f"🧪 DEBUG: Received alias = '{alias}' for canonical = '{canonical_name}'")

    with open(ALIAS_FILE, "r") as f:
        aliases = yaml.safe_load(f)

    if canonical_name not in aliases:
        aliases[canonical_name] = {"aliases": []}

    if alias not in aliases[canonical_name]["aliases"]:
        aliases[canonical_name]["aliases"].append(alias)
        with open(ALIAS_FILE, "w") as f:
            yaml.dump(aliases, f)
        print(f"✨ Added new alias '{alias}' for '{canonical_name}'")

