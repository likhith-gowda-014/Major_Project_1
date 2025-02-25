from fastapi import WebSocket, WebSocketDisconnect, APIRouter

router = APIRouter(prefix="/ws", tags=["WebSocket"])

clients = {}

@router.websocket("/chat/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: str):
    await websocket.accept()
    clients[user_id] = websocket

    try:
        while True:
            message = await websocket.receive_text()
            # AI-to-AI interaction logic goes here...
            await websocket.send_text(f"AI Response: {message[::-1]}")
    except WebSocketDisconnect:
        del clients[user_id]
