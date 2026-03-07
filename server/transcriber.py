from __future__ import annotations

import os
import tempfile
import yt_dlp

_model = None


def _get_model():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel("base", device="cpu", compute_type="int8")
    return _model


def transcribe_video(url: str) -> dict:
    """Download audio from video URL and transcribe using Whisper."""
    tmp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(tmp_dir, "audio.m4a")

    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "outtmpl": audio_path,
        "quiet": True,
        "no_warnings": True,
        "retries": 5,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    if not os.path.exists(audio_path):
        for f in os.listdir(tmp_dir):
            audio_path = os.path.join(tmp_dir, f)
            break

    try:
        model = _get_model()
        segments, info = model.transcribe(
            audio_path,
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
        )

        lines = []
        full_text_parts = []
        for seg in segments:
            m_start, s_start = int(seg.start) // 60, int(seg.start) % 60
            time_str = f"{m_start:02d}:{s_start:02d}"
            text = seg.text.strip()
            if text:
                lines.append({"time": time_str, "text": text})
                full_text_parts.append(text)

        return {
            "language": info.language,
            "duration": round(info.duration, 1),
            "segments": lines,
            "full_text": "\n".join(full_text_parts),
        }
    finally:
        try:
            os.remove(audio_path)
            os.rmdir(tmp_dir)
        except OSError:
            pass
