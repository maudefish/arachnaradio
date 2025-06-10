from typing import List, Tuple, Set
from rapidfuzz import process, fuzz
import re
from backend.core.alias_resolver import normalize_name2

def extract_at_phrases(transcript: str, max_words: int = 6) -> list[str]:
    """
    Finds phrases of up to `max_words` words following 'at' in the transcript.
    Doesn't try to stop at punctuation.
    """
    pattern = rf"\bat ((?:\w+[ '\-&]*){{1,{max_words}}})"
    matches = re.findall(pattern, transcript, flags=re.IGNORECASE)
    return [m.strip() for m in matches]

def extract_has_phrases(transcript: str, max_words: int = 6) -> list[str]:
    """
    Finds phrases of up to `max_words` words that come before 'has' in the transcript.
    """
    pattern = rf"(?:\b(?:\w+[ '\-&]*){{1,{max_words}}})\s+has"
    matches = re.findall(pattern, transcript, flags=re.IGNORECASE)
    return [m.strip() for m in matches]

def fuzzy_match_venues_from_phrases(
    transcript: str,
    already_matched: Set[Tuple[str, str]],
    canonical_venues: List[str],
    alias_data: dict,
    score_threshold: int = 85,
    verbose: bool = False
) -> List[Tuple[str, str]]:
    """
    Runs fuzzy matching on venue-like phrases found in a transcript.
    Skips any canonical names or aliases already matched.

    Returns list of (canonical_name, matched_phrase)
    """
    # Normalize canonical names from already matched
    normalized_already_matched = {normalize_name2(canonical) for canonical, _ in already_matched}
    print(f"\nnormalized_already_matched: {normalized_already_matched}\n")

    # Add aliases of already matched canonicals to skip list
    alias_matches = set()
    for canonical, _ in already_matched:
        aliases = alias_data.get(canonical, {}).get("aliases", []) or []
        alias_matches.update(normalize_name2(a) for a in aliases)

    # Union canonical and alias normalized forms
    all_matched_normalized = normalized_already_matched.union(alias_matches)
    print(f"\nall_matched_normalized: {all_matched_normalized}\n")
    # Filter candidates
    remaining_venues = [v for v in canonical_venues if normalize_name2(v) not in all_matched_normalized]
    print(f"\nremaining_venues: {remaining_venues}\n")

    normalized_to_original = {normalize_name2(v): v for v in remaining_venues}
    normalized_candidates = list(normalized_to_original.keys())

    if verbose:
        print(f"\U0001f50d Candidates remaining for fuzzy match: {len(normalized_candidates)}")

    matched = []
    unmatched = []

    # Extract venue-like phrases
    at_phrases = extract_at_phrases(transcript.replace("\n", " "))
    has_phrases = extract_has_phrases(transcript.replace("\n", " "))
    all_phrases = at_phrases + has_phrases

    if verbose:
        print(f"\U0001f3af Extracted phrases for fuzzy matching: {all_phrases}")

    # Normalize already matched phrases
    normalized_matched_phrases = {normalize_name2(p) for _, p in already_matched}

    # Filter out phrases already matched
    filtered_phrases = [
        phrase for phrase in all_phrases
        if normalize_name2(phrase) not in normalized_matched_phrases
    ]

    if verbose:
        print(f"\U0001f3af Filtered fuzzy candidate phrases: {filtered_phrases}")

    # Run fuzzy match
    for phrase in filtered_phrases:
        phrase_norm = normalize_name2(phrase)
        match_norm, score, _ = process.extractOne(phrase_norm, normalized_candidates, scorer=fuzz.WRatio)
        canonical = normalized_to_original[match_norm]

        if score >= score_threshold:
            if verbose:
                print(f"✅ Fuzzy match ({score:.1f}): '{phrase}' → '{canonical}'")
            matched.append((canonical, phrase))
        else:
            if verbose:
                print(f"❌ Fuzzy miss ({score:.1f}): '{phrase}' → '{canonical}'")
            unmatched.append((canonical, phrase))

    return matched, unmatched
