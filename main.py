import os
import io
from uuid import uuid4
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
from fastapi.responses import StreamingResponse

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextAudio(BaseModel):
    text: str

@app.post("/text")
def create_text(ta: TextAudio):
    text = ta.text
    tts = gTTS(text=text, lang='en')
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return StreamingResponse(audio_bytes, media_type="audio/mpeg")

@app.get("/")
def index():
    return {"message": "FastAPI with gTTS is running!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
