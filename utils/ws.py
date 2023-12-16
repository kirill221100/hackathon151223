from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect, status


class MessageManager:
    def __init__(self):
        self.connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, thread_id: int, ws: WebSocket):
        if not self.connections.get(thread_id):
            self.connections[thread_id] = [ws]
        else:
            self.connections[thread_id].append(ws)
        await ws.accept()

    async def send_data(self, thread_id: int, data: dict):
        try:
            [await ws.send_json(data) for ws in self.connections[thread_id]]
        except KeyError:
            pass

    async def disconnect(self, thread_id: int, ws: WebSocket):
        self.connections[thread_id].remove(ws)


message_manager = MessageManager()
