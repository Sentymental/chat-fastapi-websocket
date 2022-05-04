"""
Socket Manager that will be responsible
for sending messages beteween users
and maintain connections
"""
import logging
import json
import uvicorn

from fastapi import (
    BackgroundTasks,
    FastAPI,
    Depends,
    WebSocket,
    WebSocketDisconnect,
    Response,
    Request,
)
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from schema.schemas import UserValidator
from dependency.notifier import Notifier

from starlette.websockets import WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title="WebChat",
    description="Web chat application",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize Socket Manager
notifier = Notifier()

# Locate template:
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/templates")


@app.get("/{room_name}/{user_name}")
async def get(request: Request, room_name: str, user_name: str):
    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "room_name": room_name, "user_name": user_name},
    )


# Create Endpoints:
@app.websocket("/ws/{room_name}")
async def websocket_endpoint(
    websocket: WebSocket, room_name: str, background_tasks: BackgroundTasks
):
    await notifier.connect(websocket, room_name)
    try:
        while True:
            data = await websocket.receive_text()
            d = json.loads(data)
            d["room_name"] = room_name

            room_members = (
                notifier.get_members(room_name)
                if notifier.get_members(room_name) is not None
                else []
            )

            if websocket not in room_members:
                print("Sender not in room member: Reconnecting...")
                await notifier.connect(websocket, room_name)

            await notifier._notify(f"{data}", room_name)

    except WebSocketDisconnect:
        notifier.remove(websocket, room_name)


if __name__ == "__main__":
    uvicorn.run(app)
