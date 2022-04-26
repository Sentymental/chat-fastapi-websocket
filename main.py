"""
Socket Manager that will be responsible
for sending messages beteween users
and maintain connections
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response, Request
from .schema.schemas import UserValidator
from .dependency.dependencies import SocketManager


app = FastAPI(
    title="WebChat",
    description="Web chat application",
    version="0.0.1",
)


# Initialize Socket Manager
manager = SocketManager()

# Create Endpoints:
@app.websocket("/v1/api/chat")
async def chat(websocket: WebSocket):
    sender = websocket.cookies.get("X-Authorization")
    if sender:
        await manager.connect(websocket, sender)
        response = {"sender": sender, "message": "Connected..."}
        await manager.broadcast(response)

        try:
            while True:
                data = await websocket.receive_json()
                await manager.broadcast(data)

        except WebSocketDisconnect:
            manager.disconnect(websocket, sender)
            response["message"] = "Disconnected..."
            await manager.broadcast(response)


# Get cookie data:
@app.get("/v1/api/current_user")
def get_user(request: Request):
    return request.cookies.get("X-Authorization")


# Set cookie data:
@app.post("/v1/api/register")
def register_user(user: UserValidator, response: Response):
    response.set_cookie(key="X-Authorization", value=user.username, httponly=True)


