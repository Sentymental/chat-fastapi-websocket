"""
Socket Manager that will be responsible
for sending messages beteween users
and maintain connections
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response, Request
from fastapi.templating import Jinja2Templates
from schema.schemas import UserValidator
from dependency.dependencies import SocketManager

app = FastAPI(
    title="WebChat",
    description="Web chat application",
    version="0.0.1",
)


# Initialize Socket Manager
manager = SocketManager()

# Locate template:
templates = Jinja2Templates(directory="static/templates")

@app.get("/")
def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/chat")
def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.get("/api/current_user")
def get_user(request: Request):
    return request.cookies.get("X-Authorization")


@app.post("/api/register")
def register_user(user, response: Response):
    response.set_cookie(key="X-Authorization", value=user.username, httponly=True)


# Create Endpoints:
@app.websocket("/api/chat")
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

