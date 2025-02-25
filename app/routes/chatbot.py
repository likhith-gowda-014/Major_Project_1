from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.memory import memory
from app.models.database import get_users
import os
from gpt4all import GPT4All

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

# Load the GPT-4All model
MODEL_PATH = "models/mistral-7b.Q4_K_M.gguf"  # Update this based on your model
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Please download it.")

gpt4all_model = GPT4All(MODEL_PATH)

class ChatRequest(BaseModel):
    user_id: int
    message: str

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Retrieve conversation memory
        past_conversations = memory.get_memory(request.user_id)
        context = " ".join(past_conversations["documents"]) if past_conversations else ""

        # Generate response using GPT-4All
        prompt = f"Context: {context}\nUser: {request.message}\nAI:"
        reply = gpt4all_model.generate(prompt, max_tokens=200)

        # Store message in memory
        memory.store_message(request.user_id, request.message, reply)

        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
