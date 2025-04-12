from pathlib import Path
from arachnaradio.whisper_transcriber import transcribe_clip
from arachnaradio.song_identifier import identify_song
from arachnaradio.match_logger import log_match
from arachnaradio.mention_logger import log_mention, mentioned_artists
import re
# 🎧 Your tracked artist list (replace with dynamic loading later)
favorite_artists = [
    "SPELLLING", "Bridget St. John", "Ibibio Sound Machine", "Broadcast", "Mercury"
]


def clean_transcript(transcript: str) -> str:
    # Remove timestamps and [Music] tags
    return transcript.strip()


def is_music_segment(transcript: str) -> bool:
    if "[Music]" in transcript:
        return True

    # Heuristic: if transcript is all short lines and mostly starts with ♪ or is repetitive, it's probably lyrics
    lines = transcript.splitlines()
    lyric_lines = [line for line in lines if line.strip().startswith("♪") or len(line.strip()) < 60]
    
    # If more than half the lines look like lyrics, treat as music
    return len(lyric_lines) > 0.5 * len(lines)

def process_clip(file_path: Path, station: str = "KALX"):
    print(f"🧠 Transcribing {file_path.name}...")
    transcribe_clip(Path("data/clip.mp3"), model_name="small.en")  # uses small.en


    # 🧼 Clean transcript for both artist matching and user output
    cleaned = clean_transcript(transcript)

    print(f"📝 Transcript:\n{cleaned}\n")  # 👈 Always print cleaned transcript

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
    print()
