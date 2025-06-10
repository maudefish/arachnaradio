from pyprojroot import here
from pathlib import Path
import yaml
import re 

VENUES_PATH = here("data/masters/venues_master.yaml")                   

def normalize_text(text: str, norm_swaps: list[tuple[str, str]] = []) -> str:
	text = text.strip().lower()
	if norm_swaps:
		for old, new in norm_swaps:
			text = text.replace(old, new)
	normalized = re.sub(r"\s+", " ", text)
	normalized = re.sub(r"[^\w\s]", "", normalized)       # remove punctuation
	# normalized = normalized.strip().lower()
	return normalized

def yaml_load(path: Path) -> dict:
	with open(path, "r") as file:
		return yaml.safe_load(file)

def get_keys(data: dict) -> list[str]:
	keys = data.keys()
	keys_list = list(keys)
	# print(keys)
	# print(keys_list)
	return keys_list

def get_aspect(data: dict, key: str, aspect: str):
	return data.get(key, {}).get(aspect, [])

def get_aliases(canonical: list[str], alias_dict: dict) -> list[str]:
	aliases = []
	for key in canonical:
		aliases += alias_dict.get(key, {}).get("aliases", [])
	return aliases

# def comb_fuzzy()

def comb_alias(transcript: str, 
	canonical_names: list[str], 
	alias_dict: dict | None = None, 
	norm_swaps: list[tuple[str, str]] = [], 
	fuzzy: bool = False
	) -> list[tuple[str,str]]:
	"""
	Match canonical names (or their aliases) to phrases in a transcript.
	Return: list of (canonical name, alias)
	"""
	matches = []
	transcript = normalize_text(transcript, norm_swaps)
	print(transcript)

	for key in canonical_names:
		candidates = [key] + alias_dict.get(key, {}).get("aliases", []) 
		print(candidates)

		for candidate in candidates:
			if normalize_text(candidate, norm_swaps) in transcript:
				matches.append((key, candidate))
				break
			# if fuzzy:

	return matches


data = yaml_load(VENUES_PATH)
keys = get_keys(data)	
trans = "hi, Thee Stork and eli'sa & the greek \nTheatre"
norm_swaps = [('thee', 'the'), ('&', 'and'), ('theatre', 'theater')]
print(f"\n {comb_alias(trans, keys, data, norm_swaps)}")
