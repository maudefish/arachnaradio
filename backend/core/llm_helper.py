from pathlib import Path
import subprocess

def query_ollama(prompt: str, model: str = "mistral") -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30
        )
        response = result.stdout.decode("utf-8")
        print(response)
        return response.strip()
    except subprocess.TimeoutExpired:
        return "⚠️ LLM timeout."

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

Return the result as a list of JSON dictionaries. Do NOT comment on missing information. Stick to this format below. Example:

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
    return query_ollama(prompt)

if __name__ == "__main__":
    test_transcript = "This Friday at The Chapel, SPELLLING and Broadcast will be performing live!"
    station = "KALX"

    summary = generate_event_summary(test_transcript, station)
    print("\n🧪 Test Event Summary Output:")
    print(summary)