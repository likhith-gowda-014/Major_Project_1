from fastapi import FastAPI
from app.routes import chatbot

app = FastAPI(title="AI Digital Twin Backend")

# Include API routes
app.include_router(chatbot.router)

@app.get("/")
async def root():
    return {"message": "AI Digital Twin API is running!"}
