from pathlib import Path
from backend.core.whisper_transcriber import transcribe_clip
from backend.core.song_identifier import identify_song
from backend.core.alias_resolver import resolve_canonical_name, maybe_add_alias_to_yaml
from backend.core.llm_helper import generate_event_summary
from backend.core.event_extractor import extract_rows_from_summary, append_events_to_csv
from backend.services.match_logger import log_match
from backend.services.mention_logger import log_mention, mentioned_artists
from backend.services.venue_logger import mentioned_venues, log_venue_mention
from backend.services.user_loader import load_user_profile



import re
# 🎧 Your tracked artist list (replace with dynamic loading later)

profile = load_user_profile("1253110124")
favorite_artists = profile["favorite_artists"]
favorite_venues = profile["favorite_venues"]
# print(favorite_artists)

def clean_transcript(transcript: str) -> str:
    # Remove timestamps and [Music] tags
    return transcript.strip()

def is_music_segment(transcript: str) -> bool:
    # Check for common indicators of music in the raw transcript
    music_indicators = ["[music]", "(music)", "*Music*", "[MUSIC]", "♪", "♫", "🎵", "[instrumental]", "(instrumental)", "[song]", "(song)", "[MUSIC PLAYING]", "music)"]
    return any(indicator.lower() in transcript.lower() for indicator in music_indicators)

def process_clip(file_path: Path, station: str = "KALX", model_name: str = "base.en"):
    print(f"🧠 Transcribing {file_path.name}...")
    transcript = transcribe_clip(file_path, model_name=model_name)


    # 🧼 Clean transcript for both artist matching and user output
    cleaned = clean_transcript(transcript)

    print("📝 Raw Transcript:")
    print(transcript)
    # print("\n🧼 Cleaned Transcript:")
    # print(cleaned)
    if is_music_segment(transcript):
        print("🎵 Music segment detected — trying ACRCloud...")
        match = identify_song(file_path)
        if match and match.get("title") and match.get("artist"):
            print(f"🎶 {match['title']} by {match['artist']}")
            log_match(str(file_path), match, station=station)
        else:
            print("❌ No match found for music segment.")
    else:
        print("🗣️ Speech detected — checking for artist mentions...")
        matches = mentioned_artists(cleaned, favorite_artists)
        if matches:
            print(f"🎯 Mentioned: {', '.join(matches)}")
            log_mention(str(file_path), cleaned, station=station, matches=matches)
        else:
            print("🕸️ No artist mentions found.")
    venue_hits = mentioned_venues(cleaned, favorite_venues, return_aliases=True)

    for canonical, alias in venue_hits:
        maybe_add_alias_to_yaml(canonical, alias)

    venue_hits = list(set(venue_hits))  # Remove duplicates
    if venue_hits:
        print(f"📍 Venue(s) mentioned: {', '.join(venue_hits)}")
        log_venue_mention(str(file_path), cleaned, station=station, venues=venue_hits)
        summary = generate_event_summary(cleaned, station)
        print(f"📝 Event Summary: {summary}")
        # Assuming `summary`, `station`, and `filename` are available
        events = extract_rows_from_summary(summary, station, filename)
        append_events_to_csv(events)

    print()
