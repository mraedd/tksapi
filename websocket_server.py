import asyncio
import websockets
import json

clients = set()

async def handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            pass  # we don't expect incoming msgs, just send
    finally:
        clients.remove(websocket)

async def broadcast(data):
    if clients:
        await asyncio.wait([client.send(data) for client in clients])

start_server = websockets.serve(handler, "localhost", 8000)

# Run the server loop
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()