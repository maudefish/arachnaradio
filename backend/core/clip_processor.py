from pyprojroot import here
from pathlib import Path
from backend.core.whisper_transcriber import transcribe_clip
from backend.core.song_identifier import identify_song
from backend.core.alias_resolver import resolve_canonical_name, maybe_add_alias_to_yaml
from backend.core.llm_helper import generate_event_summary
from backend.core.event_extractor import extract_rows_from_summary, append_events_to_csv
from backend.services.song_match_logger import log_match
from backend.services.artist_mention_logger import log_mention, mentioned_artists
from backend.services.venue_mention_logger import check_for_mentioned_venues, log_venue_mention
from backend.data_io.loaders import load_known_artists, load_known_venues
from backend.services.transcript_logger import log_transcript, clean_transcript
# from backend.services.user_loader import load_user_profile
from backend.core.fuzzy_matcher import fuzzy_match_venues_from_phrases
from backend.services.fuzzy_miss_logger import log_fuzzy_misses
from backend.utils.time_utils import extract_timestamp

import re
                    
ARTISTS_PATH = here("data/masters/artists_master.yaml") 
VENUES_PATH = here("data/masters/venues_master.yaml")                   

known_artists = load_known_artists(ARTISTS_PATH)
known_venues, alias_data = load_known_venues(VENUES_PATH)

def is_music_segment(transcript: str) -> bool:
    # Check for common indicators of music in the raw transcript
    music_indicators = ["[music]", "(music)", "*Music*", "[MUSIC]", "♪", "♫", "🎵", "[instrumental]", "(instrumental)", "[song]", "(song)", "[MUSIC PLAYING]", "music)"]
    return any(indicator.lower() in transcript.lower() for indicator in music_indicators)

def process_clip(file_path: Path, station: str = "KALX", model_name: str = "base.en"):
    artist_hits = []
    print(f"🧠 Transcribing {file_path.name}...")
    transcript = transcribe_clip(file_path, model_name=model_name)

    # 🧼 Clean transcript for both artist matching and user output
    cleaned = clean_transcript(transcript)

    print(f"📝 Raw Transcript (model: {model_name})")
    print(transcript)
    # print(cleaned)

    # 1. Check for SONG ID
    if is_music_segment(transcript):
        print("🎵 Music segment detected — trying ACRCloud...")
        match = identify_song(file_path)
        if match and match.get("title") and match.get("artist"):
            log_match(str(file_path), match, station=station)
        else:
            print("❌ No match found for music segment.")
    
    # 2. If not a song, maybe an ARTIST mention?
    else: 
        print(f"🗣 Speech detected — checking for artist or venue mentions...")
        artist_hits = mentioned_artists(cleaned, known_artists)
        if artist_hits:
            print(f"🎯 Mentioned: {', '.join(artist_hits)}")
            log_mention(str(file_path), cleaned, station=station, matches=artist_hits)
        else:
            print(f"🕸 No artist mentions found.")
    
    # 3. Check for VENUE mention
    
    # This next call checks ONLY for direct string matches of canonical/alias names
    venue_hits = check_for_mentioned_venues(cleaned, known_venues, alias_data, return_aliases=True)
    venue_hits = list(set(venue_hits))  # Remove duplicates

    fuzzy_hits, fuzzy_misses = fuzzy_match_venues_from_phrases(cleaned, venue_hits, known_venues, alias_data, 90, True) # those that remain may be matched w/ fuzz
    log_fuzzy_misses(fuzzy_misses, station=station, timestamp=extract_timestamp(file_path))


    venue_hits = venue_hits + fuzzy_hits
    print(f"\nfuzzy_hits: {fuzzy_hits}\n")
    print(f"\nfuzzy_misses: {fuzzy_misses}\n")
    if venue_hits:
        canonical_names = [v[0] for v in venue_hits]
        print(f"📍 Venue(s) mentioned: {', '.join(canonical_names)}\n")
        # 1. Log raw mention data to CSV
        log_venue_mention(
            filename=str(file_path),
            transcript=cleaned,
            station=station,
            venues=venue_hits,
            alias_data=alias_data,         # ✅ pass this in
            master_names=known_venues      # ✅ pass canonical names
        )

        for canonical in canonical_names:

            # 2. Generate LLM-style summary
            summary = generate_event_summary(cleaned, station, file_path, canonical)
            # print(f"📝 Event Summary: {summary}")

            # 3. Extract structured events from summary
            events = extract_rows_from_summary(summary, station, file_path)

            # 4. Append to structured CSV log
            append_events_to_csv(events)

    else:
        events = []
        print("📍 No venue mentions found.")

    contains_music = is_music_segment(transcript)
    contains_venue = bool(venue_hits)
    contains_artist = bool(artist_hits)
    llm_ready = bool(events)
    log_transcript(
        str(file_path),
        transcript,
        cleaned,
        station=station,
        contains_music=contains_music,
        contains_venue=contains_venue,
        contains_artist=contains_artist,
        llm_summary_ready=llm_ready
    )
    print()

