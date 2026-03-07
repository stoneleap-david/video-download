from urllib.parse import quote

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from extractor import extract_video_info, download_video_stream

app = FastAPI(title="万能视频提取器 API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "服务运行正常"}


@app.get("/api/parse")
def parse_video(url: str):
    try:
        info = extract_video_info(url)
        return info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/download")
def download_video(url: str, format_id: str):
    try:
        stream, filename, content_type = download_video_stream(url, format_id)
        encoded = quote(filename)
        return StreamingResponse(
            stream,
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded}",
            },
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


