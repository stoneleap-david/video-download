from __future__ import annotations

import re
import tempfile
import os
from typing import Generator
import yt_dlp

PLATFORM_MAP = {
    "bilibili": {"name": "Bilibili", "color": "#00A1D6"},
    "youtube": {"name": "YouTube", "color": "#FF0000"},
    "douyin": {"name": "抖音", "color": "#FE2C55"},
    "tiktok": {"name": "TikTok", "color": "#010101"},
    "kuaishou": {"name": "快手", "color": "#FF4906"},
    "xiaohongshu": {"name": "小红书", "color": "#FF2442"},
    "weibo": {"name": "微博", "color": "#E6162D"},
}

REFERER_MAP = {
    "bilibili": "https://www.bilibili.com",
    "youtube": "https://www.youtube.com",
    "douyin": "https://www.douyin.com",
    "kuaishou": "https://www.kuaishou.com",
    "xiaohongshu": "https://www.xiaohongshu.com",
}


def _detect_platform(extractor_key: str) -> dict:
    key = extractor_key.lower()
    for k, v in PLATFORM_MAP.items():
        if k in key:
            return v
    return {"name": extractor_key, "color": "#10B981"}


def _get_referer(extractor_key: str) -> str | None:
    key = extractor_key.lower()
    for k, v in REFERER_MAP.items():
        if k in key:
            return v
    return None


def _format_duration(seconds: int | float | None) -> str:
    if not seconds:
        return "00:00"
    s = int(seconds)
    h, m, sec = s // 3600, (s % 3600) // 60, s % 60
    if h > 0:
        return f"{h}:{m:02d}:{sec:02d}"
    return f"{m:02d}:{sec:02d}"


def _format_filesize(size: int | float | None) -> str:
    if not size:
        return "未知大小"
    if size >= 1024 ** 3:
        return f"{size / 1024 ** 3:.1f} GB"
    if size >= 1024 ** 2:
        return f"{size / 1024 ** 2:.0f} MB"
    if size >= 1024:
        return f"{size / 1024:.0f} KB"
    return f"{size} B"


def _build_quality_label(fmt: dict) -> str:
    height = fmt.get("height")
    fps = fmt.get("fps")
    if height:
        label = f"{height}P"
        if fps and fps > 30:
            label += f" {fps}fps"
        return label
    abr = fmt.get("abr")
    if abr:
        return f"音频 {int(abr)}kbps"
    return fmt.get("format_note", "未知")


def extract_video_info(url: str) -> dict:
    """Use yt-dlp Python API to extract video metadata without downloading."""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "ignoreerrors": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info = ydl.sanitize_info(info)

    if not info:
        raise ValueError("无法解析该链接")

    platform = _detect_platform(info.get("extractor_key", ""))

    raw_formats = info.get("formats") or []

    seen_heights = set()
    formats = []
    for fmt in reversed(raw_formats):
        if fmt.get("vcodec") == "none":
            continue
        height = fmt.get("height")
        if not height or height in seen_heights:
            continue
        seen_heights.add(height)

        size = fmt.get("filesize") or fmt.get("filesize_approx")
        formats.append({
            "format_id": fmt["format_id"],
            "quality": _build_quality_label(fmt),
            "size": _format_filesize(size),
        })

    formats.sort(
        key=lambda x: int(m.group()) if (m := re.search(r"\d+", x["quality"])) else 0,
        reverse=True,
    )

    if not formats and raw_formats:
        best = raw_formats[-1]
        size = best.get("filesize") or best.get("filesize_approx")
        formats.append({
            "format_id": best["format_id"],
            "quality": _build_quality_label(best),
            "size": _format_filesize(size),
        })

    return {
        "url": url,
        "title": info.get("title", "未知标题"),
        "thumbnail": info.get("thumbnail", ""),
        "duration": _format_duration(info.get("duration")),
        "platform": platform["name"],
        "platformColor": platform["color"],
        "author": f"@{info.get('uploader') or info.get('channel') or '未知'}",
        "formats": formats,
    }


def download_video_stream(url: str, format_id: str) -> tuple[Generator, str, str]:
    """Download video with yt-dlp best practices and stream the file."""
    tmp_dir = tempfile.mkdtemp()
    output_tpl = os.path.join(tmp_dir, "%(title)s [%(id)s].%(ext)s")

    ydl_opts = {
        # skill: prefer mp4 container with h264+aac for max compatibility
        "format": (
            f"{format_id}+bestaudio[ext=m4a]/"
            f"{format_id}+bestaudio/"
            f"best[ext=mp4]/best/{format_id}"
        ),
        "outtmpl": output_tpl,
        "merge_output_format": "mp4",
        # skill: concurrent fragments for faster downloads
        "concurrent_fragment_downloads": 4,
        # skill: retries for robustness
        "retries": 10,
        "fragment_retries": 10,
        "quiet": True,
        "no_warnings": True,
    }

    # skill: detect platform for Referer anti-hotlink bypass
    with yt_dlp.YoutubeDL({"quiet": True}) as probe:
        probe_info = probe.extract_info(url, download=False)
    extractor_key = (probe_info or {}).get("extractor_key", "")

    referer = _get_referer(extractor_key)
    if referer:
        ydl_opts["http_headers"] = {"Referer": referer}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if not os.path.exists(filename):
            base = os.path.splitext(filename)[0]
            filename = base + ".mp4"

    safe_title = re.sub(r'[^\w\u4e00-\u9fff\-.]', '_', info.get("title", "video"))
    download_name = f"{safe_title}.mp4"

    def file_stream():
        try:
            with open(filename, "rb") as f:
                while chunk := f.read(1024 * 256):
                    yield chunk
        finally:
            try:
                os.remove(filename)
                os.rmdir(tmp_dir)
            except OSError:
                pass

    return file_stream(), download_name, "video/mp4"


def _is_danmaku(lang: str, formats: list) -> bool:
    """Filter out Bilibili danmaku (bullet comments) which are XML-based."""
    if lang in ("danmaku",):
        return True
    return all(f.get("ext") == "xml" for f in formats)


def _pick_text_format(formats: list) -> dict | None:
    """Pick the best text-based subtitle format, skip XML/danmaku."""
    text_fmts = [f for f in formats if f.get("ext") not in ("xml",)]
    if not text_fmts:
        return None
    for ext in ("json3", "vtt", "srt", "srv1", "srv2", "srv3", "ass"):
        match = next((f for f in text_fmts if f.get("ext") == ext), None)
        if match:
            return match
    return text_fmts[0]


def _fetch_subtitle_text(sub_url: str, ext: str, referer: str | None = None) -> str:
    """Fetch subtitle content from URL, proxied through backend to bypass 403."""
    import requests
    headers = {}
    if referer:
        headers["Referer"] = referer
    try:
        resp = requests.get(sub_url, headers=headers, timeout=15)
        resp.raise_for_status()
        raw = resp.text
    except Exception:
        return ""

    if ext == "json3":
        try:
            import json
            data = json.loads(raw)
            events = data.get("events") or []
            lines = []
            for e in events:
                segs = e.get("segs")
                if not segs:
                    continue
                ms = e.get("tStartMs", 0)
                s = ms // 1000
                m, sec = s // 60, s % 60
                time_str = f"{m:02d}:{sec:02d}"
                text = "".join(seg.get("utf8", "") for seg in segs).strip()
                if text:
                    lines.append(f"{time_str}  {text}")
            return "\n".join(lines)
        except Exception:
            return raw

    if ext in ("vtt", "srt"):
        lines = []
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.isdigit():
                continue
            if "-->" in line:
                continue
            if line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
                continue
            lines.append(line)
        return "\n".join(lines)

    return raw


def extract_subtitles(url: str) -> list[dict]:
    """Extract subtitles and return their text content directly."""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info = ydl.sanitize_info(info)

    if not info:
        return []

    extractor_key = info.get("extractor_key", "")
    referer = _get_referer(extractor_key)

    results = []

    subs = info.get("subtitles") or {}
    auto_subs = info.get("automatic_captions") or {}

    for lang, formats in subs.items():
        if _is_danmaku(lang, formats):
            continue
        best = _pick_text_format(formats)
        if not best or not best.get("url"):
            continue
        text = _fetch_subtitle_text(best["url"], best.get("ext", ""), referer)
        if text:
            results.append({
                "lang": lang,
                "name": best.get("name", lang),
                "content": text,
                "auto": False,
            })

    if not results:
        preferred_langs = ("zh-Hans", "zh", "zh-CN", "en", "ja", "zh-TW")
        for lang, formats in auto_subs.items():
            if lang not in preferred_langs:
                continue
            if _is_danmaku(lang, formats):
                continue
            best = _pick_text_format(formats)
            if not best or not best.get("url"):
                continue
            text = _fetch_subtitle_text(best["url"], best.get("ext", ""), referer)
            if text:
                results.append({
                    "lang": lang,
                    "name": best.get("name", lang),
                    "content": text,
                    "auto": True,
                })

    return results
