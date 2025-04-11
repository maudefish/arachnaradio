from pathlib import Path
import subprocess

# This assumes whisper.cpp is in the same directory as your project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
WHISPER_CPP_MAIN = PROJECT_ROOT / "whisper.cpp" / "build" / "bin" / "whisper-cli"
MODEL_PATH = PROJECT_ROOT / "whisper.cpp" / "models" / "base.en.bin"

def transcribe_clip(audio_path: Path) -> str:
    if not WHISPER_CPP_MAIN.exists():
        raise FileNotFoundError(f"Whisper.cpp binary not found at {WHISPER_CPP_MAIN}")
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Whisper model not found at {MODEL_PATH}")

    result = subprocess.run(
        [str(WHISPER_CPP_MAIN), "-m", str(MODEL_PATH), "-f", str(audio_path)],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()
