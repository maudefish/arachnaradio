from pathlib import Path
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WHISPER_CPP_MAIN = PROJECT_ROOT / "whisper.cpp" / "build" / "bin" / "whisper-cli"

def transcribe_clip(audio_path: Path, model_name: str = "base.en") -> str:
    model_path = PROJECT_ROOT / "whisper.cpp" / "models" / f"{model_name}.bin"

    if not WHISPER_CPP_MAIN.exists():
        raise FileNotFoundError(f"Whisper.cpp binary not found at {WHISPER_CPP_MAIN}")
    if not model_path.exists():
        raise FileNotFoundError(f"Whisper model not found at {model_path}")

    result = subprocess.run(
        [str(WHISPER_CPP_MAIN), "-m", str(model_path), "-f", str(audio_path)],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()
