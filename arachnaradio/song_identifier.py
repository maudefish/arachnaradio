import base64
import hashlib
import hmac
import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
from pydub import AudioSegment
from arachnaradio.whisper_transcriber import transcribe_clip


load_dotenv()

ACR_HOST = os.getenv("ACR_HOST")  # e.g., https://identify-us-west-2.acrcloud.com
ACR_KEY = os.getenv("ACR_KEY")
ACR_SECRET = os.getenv("ACR_SECRET")

def identify_song(file_path: Path):
    # Prepare audio clip (10s mono wav)
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_channels(1).set_frame_rate(8000)
    audio = audio[:10000]
    audio.export("temp_clip.wav", format="wav")

    with open("temp_clip.wav", "rb") as f:
        sample_bytes = f.read()
        sample_size = len(sample_bytes)

    os.remove("temp_clip.wav")

    # ACRCloud authentication
    http_method = "POST"
    http_uri = "/v1/identify"
    data_type = "audio"
    signature_version = "1"
    timestamp = str(int(time.time()))

    string_to_sign = "\n".join([
        http_method,
        http_uri,
        ACR_KEY,
        data_type,
        signature_version,
        timestamp
    ])

    signature = base64.b64encode(
        hmac.new(ACR_SECRET.encode('ascii'), string_to_sign.encode('ascii'), hashlib.sha1).digest()
    ).decode('ascii')

    files = {
        'sample': ('temp_clip.wav', sample_bytes, 'audio/wav')
    }

    data = {
        'access_key': ACR_KEY,
        'sample_bytes': sample_size,
        'timestamp': timestamp,
        'signature': signature,
        'data_type': data_type,
        'signature_version': signature_version
    }

    response = requests.post(ACR_HOST + http_uri, files=files, data=data)
    result = response.json()

    if result.get("status", {}).get("code") == 0:
        metadata = result["metadata"]["music"][0]

        match_info = {
            "title": metadata.get("title"),
            "artist": metadata.get("artists", [{}])[0].get("name"),
            "album": metadata.get("album", {}).get("name"),
            "score": metadata.get("score"),
            "label": metadata.get("label"),
            "play_offset_ms": metadata.get("play_offset_ms"),
            "acrid": metadata.get("acrid"),
            "genres": [g.get("name") for g in metadata.get("genres", [])]
        }

        print(f"🎶 Match: {match_info['title']} by {match_info['artist']}")
        return match_info

    print("❌ No match found.")
    return None
    