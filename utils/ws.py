from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect, status


class BedDataManager:
    def __init__(self):
        self.connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, bed_id: int, ws: WebSocket):
        if not self.connections.get(bed_id):
            self.connections[bed_id] = [ws]
        else:
            self.connections[bed_id].append(ws)
        await ws.accept()

    async def send_data(self, bed_id: int, data: dict):
        try:
            [await ws.send_json(data) for ws in self.connections[bed_id]]
        except KeyError:
            pass

    async def disconnect(self, bed_id: int, ws: WebSocket):
        self.connections[bed_id].remove(ws)


bed_data_manager = BedDataManager()
