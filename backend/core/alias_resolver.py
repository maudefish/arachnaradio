from pyprojroot import here
import yaml
from pathlib import Path
from typing import Optional
from rapidfuzz import process, fuzz
import re

# Paths
# ALIAS_FILE = here("data/masters/aliases/venue_aliases.yaml")


#from pathlib import Path
from rapidfuzz import process, fuzz
import yaml

# Load alias YAML
with open("data/masters/venues_master.yaml", "r") as f:
    alias_data = yaml.safe_load(f)

def normalize_name(name: str) -> str:
    name = name.lower().strip()
    name = re.sub(r'^the\s+', '', name)               # Remove leading "the"
    name = name.replace('&', 'and')                   # Ampersand to 'and'
    name = name.replace('theatre', 'theater')         # Normalize spelling
    name = re.sub(r"[^\w\s]", "", name)               # Remove punctuation
    name = re.sub(r"\s+", " ", name)                  # Collapse spaces
    return name

# Build alias map + normalized canonicals
canonical_names = list(alias_data.keys())
normalized_canonicals = [normalize_name(c) for c in canonical_names]
alias_map = {}

for canonical, info in alias_data.items():
    alias_map[normalize_name(canonical)] = canonical
    for alias in info.get("aliases", []):
        alias_map[normalize_name(alias)] = canonical

def resolve_canonical_name(input_name: str, use_aliases: bool = True, use_fuzzy: bool = True, score_threshold: int = 50, verbose=False) -> str:
    if not input_name:
        return ""

    input_normalized = normalize_name(input_name)

    # 1. Alias matching
    if use_aliases and input_normalized in alias_map:
        if verbose:
            print(f"\n✅ Alias match: '{input_normalized}' → '{alias_map[input_normalized]}'\n")
        return alias_map[input_normalized]

    # 2. Fuzzy fallback
    if use_fuzzy:
        match, score, _ = process.extractOne(input_normalized, normalized_canonicals, scorer=fuzz.WRatio)
        if score >= score_threshold:
            original = canonical_names[normalized_canonicals.index(match)]
            if verbose:
                print(f"\n🔍 Fuzzy match ({score:.1f}): '{input_normalized}' → '{original}'\n")
            return original

    if verbose:
        print(f"⚠️ Could not resolve: '{input_name}'")
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

