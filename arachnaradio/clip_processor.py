from pathlib import Path
from arachnaradio.whisper_transcriber import transcribe_clip
from arachnaradio.song_identifier import identify_song
from arachnaradio.match_logger import log_match
from arachnaradio.mention_logger import log_mention, mentioned_artists
from arachnaradio.venue_logger import mentioned_venues, log_venue_mention
from arachnaradio.user_loader import load_user_profile

import re
# 🎧 Your tracked artist list (replace with dynamic loading later)

profile = load_user_profile("kevin")
favorite_artists = profile["favorite_artists"]
favorite_venues = profile["favorite_venues"]

def clean_transcript(transcript: str) -> str:
    # Remove timestamps and [Music] tags
    return transcript.strip()

def is_music_segment(transcript: str) -> bool:
    # Check for common indicators of music in the raw transcript
    music_indicators = ["[music]", "(music)", "*Music*", "[MUSIC]", "♪", "♫", "[instrumental]", "(instrumental)", "[song]", "(song)", "[MUSIC PLAYING]", "music)"]
    return any(indicator.lower() in transcript.lower() for indicator in music_indicators)

# # def is_music_segment(transcript: str) -> bool:
#     if "[Music]" in transcript:
#         return True

#     # Heuristic: if transcript is all short lines and mostly starts with ♪ or is repetitive, it's probably lyrics
#     lines = transcript.splitlines()
#     lyric_lines = [line for line in lines if line.strip().startswith("♪") or len(line.strip()) < 60]
    
#     # If more than half the lines look like lyrics, treat as music
#     return len(lyric_lines) > 0.5 * len(lines)

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
    venue_hits = mentioned_venues(cleaned, favorite_venues)
    if venue_hits:
        print(f"📍 Venue(s) mentioned: {', '.join(venue_hits)}")
        log_venue_mention(str(file_path), cleaned, station=station, venues=venue_hits)
    print()
