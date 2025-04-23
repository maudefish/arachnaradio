from pathlib import Path
import subprocess
import requests

def query_ollama(prompt: str, model: str = "mistral") -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False  # set to True if you want token-by-token streaming
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        print(data.get("response", "").strip())
        return data.get("response", "").strip()

    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama API error: {e}")
        return "[Summary failed – Ollama API error]"
def generate_event_summary(transcript: str, station: str) -> str:
    prompt = f"""
You are an assistant helping extract music events from radio transcripts.

Here's a transcript of an audio clip from {station} radio:

---
{transcript}
---

Extract the events mentioned in this transcript. Each event should include:
- `artist`: Name(s) of the artist(s)
- `venue`: Name of the venue
- `date`: Date of the event (or "Unknown" if not mentioned)
- `station`: Always return "{station}" here

Return the result as a list of JSON dictionaries. Do NOT comment on missing information or include superfluous information. Stick to this format below. Example:

[
  {{
    "artist": "Artist A, Artist B",
    "venue": "The Chapel",
    "date": "April 22, 2025",
    "station": "KALX",
  }},
  {{
    "artist": "Artist C",
    "venue": "The Independent",
    "date": "Unknown",
    "station": "KALX",
  }}
]
"""
    try:
        return query_ollama(prompt)
    except (requests.exceptions.ConnectionError, OSError) as e:
        print("⚠️ Ollama is not running. Skipping event summary generation.")
        return "[Event summary unavailable – Ollama not running]"

if __name__ == "__main__":
    test_transcript = "This Friday at The Chapel, SPELLLING and Broadcast will be performing live!"
    station = "KALX"

    summary = generate_event_summary(test_transcript, station)
    print("\n🧪 Test Event Summary Output:")
    print(summary)