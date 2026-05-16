import re
import uuid
from pathlib import Path

from fastapi import Body, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydub import AudioSegment

try:
    from .audio_merger import merge_audios
    from .tts_engine import synthesize
except ImportError:
    from audio_merger import merge_audios
    from tts_engine import synthesize


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
FRONTEND_DIR = PROJECT_DIR / "frontend"
VOICES_DIR = BASE_DIR / "voices"
OUTPUT_DIR = BASE_DIR / "output"

VOICES_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="LocalVoice TTS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/app", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


def _safe_voice_name(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_. -]+", "", name).strip().replace(" ", "_")
    if cleaned in {"", ".", ".."}:
        raise HTTPException(status_code=400, detail="Use a valid voice name.")
    return cleaned


def _voice_path(name: str) -> Path:
    return VOICES_DIR / f"{_safe_voice_name(name)}.wav"


@app.get("/")
def root():
    return RedirectResponse(url="/app")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload-voice")
async def upload_voice(name: str = Form(...), file: UploadFile = File(...)):
    voice_name = _safe_voice_name(name)
    source_name = file.filename or ""
    suffix = Path(source_name).suffix.lower()

    if suffix not in {".wav", ".mp3", ".mpeg"}:
        raise HTTPException(status_code=400, detail="Upload a WAV or MP3 voice sample.")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    output_path = VOICES_DIR / f"{voice_name}.wav"

    if suffix == ".wav":
        output_path.write_bytes(data)
    else:
        temp_path = OUTPUT_DIR / f"upload-{uuid.uuid4().hex}{suffix}"
        temp_path.write_bytes(data)
        try:
            audio = AudioSegment.from_file(temp_path)
            audio.export(output_path, format="wav")
        finally:
            temp_path.unlink(missing_ok=True)

    return {"status": "ok", "voice": voice_name}


@app.get("/voices")
def list_voices():
    voices = sorted(path.stem for path in VOICES_DIR.glob("*.wav"))
    return {"voices": voices}


@app.delete("/voices/{name}")
def delete_voice(name: str):
    path = _voice_path(name)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Voice not found.")

    path.unlink()
    return {"status": "deleted", "voice": path.stem}


@app.post("/synthesize")
async def synthesize_line(text: str = Form(...), voice: str = Form(...)):
    voice_path = _voice_path(voice)
    clean_text = text.strip()

    if not voice_path.exists():
        raise HTTPException(status_code=404, detail=f"Voice '{voice}' not found.")
    if not clean_text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    output_file = OUTPUT_DIR / f"{uuid.uuid4().hex}.wav"

    try:
        synthesize(clean_text, str(voice_path), str(output_file))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return FileResponse(
        str(output_file),
        media_type="audio/wav",
        filename="line.wav",
    )


@app.post("/combine")
async def combine_all(data: dict = Body(...)):
    lines = data.get("lines", [])
    if not isinstance(lines, list) or not lines:
        raise HTTPException(status_code=400, detail="Add at least one dialog line.")

    pause_ms = int(data.get("pause_ms", 300))
    pause_ms = min(max(pause_ms, 0), 5000)
    audio_files: list[str] = []

    for line in lines:
        if not isinstance(line, dict):
            continue

        text = str(line.get("text", "")).strip()
        voice = str(line.get("voice", "")).strip()
        if not text or not voice:
            continue

        voice_path = _voice_path(voice)
        if not voice_path.exists():
            raise HTTPException(status_code=404, detail=f"Voice '{voice}' not found.")

        output_file = OUTPUT_DIR / f"{uuid.uuid4().hex}.wav"
        try:
            synthesize(text, str(voice_path), str(output_file))
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

        audio_files.append(str(output_file))

    if not audio_files:
        raise HTTPException(status_code=400, detail="No valid dialog lines were found.")

    final_output = OUTPUT_DIR / f"dialog-{uuid.uuid4().hex}.wav"
    merge_audios(audio_files, str(final_output), pause_ms=pause_ms)

    return FileResponse(
        str(final_output),
        media_type="audio/wav",
        filename="dialog.wav",
    )
