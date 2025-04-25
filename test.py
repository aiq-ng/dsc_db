import asyncio
import websockets
import json

async def receive_targets():
    uri = "ws://89.117.1.173:8090/ws/targets"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            target_data = json.loads(message)
            print(f"Received new target: {target_data}")

asyncio.run(receive_targets())
