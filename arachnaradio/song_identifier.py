import base64
import hashlib
import hmac
import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()

ACR_HOST = os.getenv("ACR_HOST")  # e.g., https://identify-us-west-2.acrcloud.com
ACR_KEY = os.getenv("ACR_KEY")
ACR_SECRET = os.getenv("ACR_SECRET")

def identify_song(file_path: Path):
    http_method = "POST"
    http_uri = "/v1/identify"
    data_type = "audio"
    signature_version = "1"
    timestamp = str(int(time.time()))

    # Trim and convert to 10s wav clip
    sample = AudioSegment.from_file(file_path)
    sample = sample.set_channels(1).set_frame_rate(8000)
    sample = sample[:10000]
    sample.export("temp_clip.wav", format="wav")

    with open("temp_clip.wav", "rb") as f:
        sample_bytes = f.read()
        sample_size = len(sample_bytes)

    string_to_sign = "\n".join([
        http_method,
        http_uri,
        ACR_KEY,
        data_type,
        signature_version,
        timestamp
    ])

    sign = base64.b64encode(
        hmac.new(ACR_SECRET.encode('ascii'), string_to_sign.encode('ascii'), hashlib.sha1).digest()
    ).decode('ascii')

    files = {
        'sample': ('temp_clip.wav', sample_bytes, 'audio/wav')
    }

    data = {
        'access_key': ACR_KEY,
        'sample_bytes': sample_size,
        'timestamp': timestamp,
        'signature': sign,
        'data_type': data_type,
        'signature_version': signature_version
    }

    print("📡 Requesting:", ACR_HOST + http_uri)
    print("🧾 Signature:", sign)
    print("🧾 Timestamp:", timestamp)
    print("🧾 Sample size (bytes):", sample_size)

    response = requests.post(ACR_HOST + http_uri, files=files, data=data)
    os.remove("temp_clip.wav")

    print("📥 Raw response text:")
    print(response.text)

    try:
        result = response.json()
        metadata = result['metadata']['music'][0]
        title = metadata.get('title')
        artist = metadata.get('artists')[0]['name']
        print(f"🎶 Match: {title} by {artist}")
        return title, artist
    except Exception:
        print("❌ No match found.")
        return None, None
