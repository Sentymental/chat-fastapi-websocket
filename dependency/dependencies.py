"""
File that will contain all dependencies
"""
from fastapi import WebSocket
from typing import Any


# Building our SocketManager:
class SocketManager:
    """
    Create socket manager class that will be responsible
    for maintain connections and users
    """

    def __init__(self):
        self.active_connections: list[tuple[WebSocket, str]] = []

    async def connect(self, websocket: WebSocket, user: str):
        await websocket.accept()
        self.active_connections.append((websocket, user))

    def disconnect(self, websocket: WebSocket, user: str):
        self.active_connections.remove((websocket, user))

    async def broadcast(self, data: Any):
        for conn in self.active_connections:
            await conn[0].send_json(data)
