from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory="images"), name="images")

# ... (Keep your other @app.get routes below here exactly as they are)

@app.get("/api/vocabulary")
def get_vocabulary():
    with open("data/vocabulary.json", "r", encoding="utf-8") as file:
        return json.load(file)
@app.get("/api/culture/{age}")
def get_culture_content(age: int):
    # Load the JSON data
    with open("data/culture.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        
    # Route to the correct content block based on the child's age
    if age <= 5:
        return data["ages_3_to_5"]
    else:
        return data["ages_6_to_10"]
@app.get("/api/stories")
def get_stories():
    with open("data/stories.json", "r", encoding="utf-8") as file:
        return json.load(file)
    from pydantic import BaseModel

class TutorRequest(BaseModel):
    child_name: str
    age: int
    current_word: str
    child_question: str

@app.post("/api/ai-tutor")
def ask_ai_tutor(request: TutorRequest):
    user_msg = request.child_question.lower()
    
    # Immersion logic: Default to encouraging Oshikwanyama responses
    if "hi" in user_msg or "hello" in user_msg or "mhola" in user_msg:
        reply = "Mhola, {name}! 🦉 Ndishi tu popi Oshikwanyama! (Hello! Let's speak Oshikwanyama!) Try saying 'Etango' (Sun) or 'Omeya' (Water)."
    elif "water" in user_msg or "omeya" in user_msg:
        reply = "Nawa unene! 💧 Omeya means water. Can you say: 'Onda pumbwa omeya' (I need water)?"
    elif "sun" in user_msg or "etango" in user_msg:
        reply = "Tala nawa! ☀️ Etango oli li pombada (The sun is high up). You're doing great!"
    else:
        reply = "Maliha! 🦉 Let's try together. Say 'Wa lalapo' for Good morning, or 'Tangi' for Thank you!"

    return {"reply": reply.format(name=request.child_name)}