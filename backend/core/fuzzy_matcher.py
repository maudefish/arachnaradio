from typing import List, Tuple, Set
from rapidfuzz import process, fuzz
import re
from backend.core.alias_resolver import normalize_name


def extract_at_phrases(transcript: str, max_words: int = 6) -> list[str]:
    """
    Finds phrases of up to `max_words` words following 'at' in the transcript.
    Doesn't try to stop at punctuation.
    """
    # This captures "at word1 word2 ... word6"
    pattern = rf"\bat ((?:\w+[ '\-&]*){{1,{max_words}}})"
    matches = re.findall(pattern, transcript, flags=re.IGNORECASE)
    return [m.strip() for m in matches]

def extract_has_phrases(transcript: str, max_words: int = 6) -> list[str]:
    """
    Finds phrases of up to `max_words` words that come before 'has' in the transcript.
    """
    # Matches up to `max_words` words before "has"
    pattern = rf"(?:\b(?:\w+[ '\-&]*){{1,{max_words}}})\s+has"
    matches = re.findall(pattern, transcript, flags=re.IGNORECASE)
    return [m.strip() for m in matches]

def fuzzy_match_venues_from_phrases(
    transcript: str,
    already_matched: Set[str],
    canonical_venues: List[str],
    score_threshold: int = 85,
    verbose: bool = False
) -> List[Tuple[str, str]]:
    """
    Runs fuzzy matching on venue-like phrases found in a transcript.
    Skips any canonical names already found via alias/direct match.

    Returns list of (canonical_name, matched_phrase)
    """
    # ✅ FIX: Extract just the canonical names from the tuple set
    normalized_already_matched = {normalize_name(canonical) for canonical, _ in already_matched}
    remaining_venues = [v for v in canonical_venues if normalize_name(v) not in normalized_already_matched]
    normalized_to_original = {normalize_name(v): v for v in remaining_venues}
    normalized_candidates = list(normalized_to_original.keys())

    if verbose:
        print(f"🔍 Candidates remaining for fuzzy match: {len(normalized_candidates)}")

    matched = []
 
    at_phrases = extract_at_phrases(transcript.replace("\n", " ")) 
    has_phrases = extract_has_phrases(transcript.replace("\n", " "))
    phrases = at_phrases + has_phrases
    if verbose:
        print(f"🎯 Extracted phrases for fuzzy matching: {phrases}")

    for phrase in phrases:

        match_norm, score, _ = process.extractOne(phrase, normalized_candidates, scorer=fuzz.WRatio)
        canonical = normalized_to_original[match_norm]
        print(f"✅ Fuzzy match ({score:.1f}): '{phrase}' → '{canonical}'")
        if score >= score_threshold:
            canonical = normalized_to_original[match_norm]
            if verbose:
                print(f"✅ Fuzzy match ({score:.1f}): '{phrase}' → '{canonical}'")
            matched.append((canonical, phrase))

    return matched
