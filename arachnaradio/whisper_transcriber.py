# whisper_cpp_transcriber.py
from pathlib import Path
import subprocess

WHISPER_CPP_MAIN = Path(__file__).resolve().parents[1] / "whisper.cpp" / "main"
MODEL_BIN = Path(__file__).resolve().parents[1] / "whisper.cpp" / "models" / "small.en.bin"

def transcribe_clip(audio_path: Path):
    result = subprocess.run(
        [str(WHISPER_CPP_MAIN), "-m", str(MODEL_BIN), "-f", str(audio_path)],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()