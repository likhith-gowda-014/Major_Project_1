from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.memory import memory
from app.models.database import get_users
import os
from gpt4all import GPT4All

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

# Get the absolute path to the models directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
MODEL_PATH = os.path.join(BASE_DIR, "../models/mistral-7b-instruct-v0.2.Q4_K_M.gguf")

# Normalize the path for different OS
MODEL_PATH = os.path.normpath(MODEL_PATH)

# Check if the model exists
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Please download it and place it in the correct directory.")

# Initialize GPT-4All model
try:
    gpt4all_model = GPT4All(MODEL_PATH, device="cpu") #ensure it runs on CPU not on GPU
except Exception as e:
    raise RuntimeError(f"Failed to load GPT-4All model: {e}")

class ChatRequest(BaseModel):
    user_id: int
    message: str

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Retrieve conversation memory
        past_conversations = memory.get_memory(request.user_id)
        context = " ".join(past_conversations["documents"]) if past_conversations else ""

        # Construct prompt
        prompt = f"Context: {context}\nUser: {request.message}\nAI:"

        # Generate response with GPT-4All
        with gpt4all_model.chat_session():  # Ensures efficient execution
            reply = gpt4all_model.generate(prompt, max_tokens=200)

        # Store message in memory
        memory.store_message(request.user_id, request.message, reply)

        return {"reply": reply}

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"Model error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
