import os
from pathlib import Path
from typing import Optional


MODEL_NAME = os.getenv(
    "LOCALVOICE_TTS_MODEL",
    "tts_models/multilingual/multi-dataset/xtts_v2",
)
DEFAULT_LANGUAGE = os.getenv("LOCALVOICE_LANGUAGE", "en")

_tts_model = None
_device = None


def _load_model():
    """Load XTTS lazily so the API can start before the first synthesis."""
    global _tts_model, _device

    if _tts_model is not None:
        return _tts_model

    try:
        import torch
        from TTS.api import TTS
    except ImportError as exc:
        raise RuntimeError(
            "Missing TTS dependencies. Run: pip install -r requirements.txt"
        ) from exc

    _device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[TTS] Loading {MODEL_NAME} on {_device}. First run may download the model.")
    os.environ["COQUI_TOS_AGREED"] = "1"
    _tts_model = TTS(MODEL_NAME).to(_device)
    return _tts_model


def synthesize(
    text: str,
    voice_sample_path: str,
    output_path: str,
    language: Optional[str] = None,
) -> str:
    """Convert text to speech using a local voice sample."""
    clean_text = text.strip()
    if not clean_text:
        raise ValueError("Text cannot be empty.")

    voice_path = Path(voice_sample_path)
    if not voice_path.exists():
        raise FileNotFoundError(f"Voice sample not found: {voice_path}")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    model = _load_model()
    model.tts_to_file(
        text=clean_text,
        speaker_wav=str(voice_path),
        language=language or DEFAULT_LANGUAGE,
        file_path=str(output),
    )
    return str(output)