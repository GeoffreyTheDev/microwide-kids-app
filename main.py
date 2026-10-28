import json
import httpx
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# 1. Initialize the app FIRST
app = FastAPI()

# 2. Add CORS middleware so your frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Mount static folders for images (and audio when you add it)
app.mount("/images", StaticFiles(directory="images"), name="images")
# app.mount("/audio", StaticFiles(directory="audio"), name="audio") 

# --- DATA MODELS ---
class ChatRequest(BaseModel):
    child_name: str
    age: int
    current_word: str
    child_question: str

# --- ROUTES ---

@app.get("/api/vocabulary")
def get_vocabulary():
    """Serves the Oshikwanyama vocabulary list"""
    with open("data/vocabulary.json", "r", encoding="utf-8") as file:
        return json.load(file)

@app.get("/api/stories")
def get_stories():
    """Serves the interactive stories library"""
    with open("data/stories.json", "r", encoding="utf-8") as file:
        return json.load(file)

@app.post("/api/ai-tutor")
def ai_tutor_chat(request: ChatRequest):
    """Handles Kulu the Owl's chat responses"""
    # Simple fallback logic for the prototype
    word = request.current_word
    question = request.child_question.lower()
    
    if "hint" in question:
        reply = f"A great hint for {word} is to think about nature! 🌿"
    else:
        reply = f"That is a great question, {request.child_name}! Keep practicing your Oshikwanyama."
        
    return {"reply": reply}

@app.get("/api/tts")
async def generate_speech(word: str):
    """Generates audio on the fly using ElevenLabs TTS"""
    ELEVENLABS_API_KEY = "your_api_key_here" 
    VOICE_ID = "pNInz6obbfdqIjc9VD33"
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": word,
        "model_id": "eleven_multilingual_v2", 
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.7
        }
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        
    if response.status_code == 200:
        return Response(content=response.content, media_type="audio/mpeg")
    else:
        return {"error": "Failed to generate speech"}