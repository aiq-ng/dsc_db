from fastapi import WebSocket
import json
from datetime import date

connected_clients = set()  # Store WebSocket connections

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except Exception:
        connected_clients.remove(websocket)

async def broadcast_target(target):
    if not isinstance(target, dict):
        target_dict = dict(target)
        target_dict["metadata"] = json.loads(target_dict["metadata"])
        target_dict["created_at"] = target_dict["created_at"].isoformat()
        target_dict["updated_at"] = target_dict["updated_at"].isoformat()
    else:
        target_dict = target.copy()  # Avoid modifying original dict
    # Convert target_date to string if it's a date object
    if isinstance(target_dict.get("target_date"), date):
        target_dict["target_date"] = target_dict["target_date"].isoformat()
    message = json.dumps(target_dict)
    for client in list(connected_clients):
        try:
            await client.send_text(message)
        except Exception:
            connected_clients.remove(client)

