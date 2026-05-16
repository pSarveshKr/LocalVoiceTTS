from pathlib import Path

from pydub import AudioSegment


def merge_audios(file_paths: list[str], output_path: str, pause_ms: int = 300) -> str:
    """Merge generated audio clips into one WAV file."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    combined = AudioSegment.empty()
    silence = AudioSegment.silent(duration=max(0, pause_ms))
    added_any = False

    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            continue

        combined += AudioSegment.from_file(path) + silence
        added_any = True

    if not added_any:
        raise ValueError("No audio files were available to merge.")

    if pause_ms > 0 and len(combined) >= pause_ms:
        combined = combined[:-pause_ms]

    combined.export(output, format="wav")
    return str(output)
