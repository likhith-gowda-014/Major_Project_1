from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chatbot

app = FastAPI(title="AI Digital Twin Backend")

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, or specify ["http://localhost:3000"] for React
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include API routes
app.include_router(chatbot.router)

@app.get("/")
async def root():
    return {"message": "AI Digital Twin API is running!"}