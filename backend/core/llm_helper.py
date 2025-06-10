from pathlib import Path
import subprocess
import requests
from backend.utils.time_utils import path_to_weekday

def query_ollama(prompt: str, model: str = "mistral") -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False  # set to True if you want token-by-token streaming
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        print(data.get("response", "").strip())
        return data.get("response", "").strip()

    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama API error: {e}")
        return "[Summary failed – Ollama API error]"
def generate_event_summary(transcript: str, station: str, file_path : Path, venue_hint: list[str:] = []) -> str:
    weekday = path_to_weekday(file_path)
    prompt = f"""
You are an assistant helping extract music events from radio transcripts. Focus ONLY on the event involving the venue {venue_hint}.

Here's a transcript of an audio clip from {station} radio that occurred on {weekday}:

---
{transcript}
---

Extract the event at {venue_hint} mentioned in this transcript. Each event should include:
- `artist`: Name(s) of the artist(s) (properly captilized)
- `venue`: {venue_hint}
- `date`: Date of the event (if a day of week is mentioned, extrapolate the date using today = {weekday} as a reference point. Put "Unknown" if not able to be determined from context.)
- `station`: Always return "{station}" here

Return the result for the event located at {venue_hint} as a JSON dictionary. Do NOT comment on missing information or include superfluous information. Stick to this format below. Example:

[
  {{ 
    "artist": "Artist A, Artist B",
    "venue": "{venue_hint}",
    "date": "April 22",
    "station": "{station}",
  }}
]
"""
    # print(f"\n{prompt}\n")
    try:
        return query_ollama(prompt)
    except (requests.exceptions.ConnectionError, OSError) as e:
        print("⚠️ Ollama is not running. Skipping event summary generation.")
        return "[Event summary unavailable – Ollama not running]"

# if __name__ == "__main__":
#     test_transcript = "This Friday at The Chapel, SPELLLING and Broadcast will be performing live!"
#     station = "KALX"

#     summary = generate_event_summary(test_transcript, station, venue_hint)
#     print("\n🧪 Test Event Summary Output:")
#     print(summary)