import os
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from faster_whisper.audio import decode_audio

from agents.math_agent import MathAgent
from services.vad_service import VADService
from services.stt_service import STTService


STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

app = FastAPI(title="AI Calculator")

math_agent = MathAgent()
vad_service = VADService()
stt_service = STTService()

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/query")
def text_query(payload: QueryRequest):

    query = payload.query.strip()

    if not query:
        raise HTTPException(status_code=400, detail="Empty query.")

    try:
        answer = math_agent.solve(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"answer": answer}


@app.post("/api/voice")
async def voice_query(audio: UploadFile = File(...)):

    suffix = Path(audio.filename or "audio.webm").suffix or ".webm"

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name

    try:
        try:
            audio_array = decode_audio(tmp_path, sampling_rate=16000)
        except Exception:
            raise HTTPException(status_code=400, detail="Could not read audio.")

        if not vad_service.has_speech(audio_array):
            raise HTTPException(status_code=400, detail="No speech detected.")

        transcribed = stt_service.transcribe(tmp_path).strip()

        if not transcribed:
            raise HTTPException(status_code=400, detail="Could not transcribe audio.")

        try:
            answer = math_agent.solve(transcribed)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        return {"transcribed": transcribed, "answer": answer}

    finally:
        os.remove(tmp_path)
