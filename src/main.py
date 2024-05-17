import asyncio
import websockets
from game.manager import manager


class NetworkManager:
    def __init__(self):
        self.connections = []
        self.game = manager()
        self.started = asyncio.Event()
        self.host = None
        self.counter = 0

    async def handle_connection(self, websocket, path):
        if path.split("/")[-1] == "host":
            if self.host is None:
                self.host = websocket
            else:
                await websocket.send("Host already connected!")
                return
        if path.split("/")[-1] == "player":
            if self.host is not None:
                websockets.broadcast(self.connections, "New player connected!")
                self.connections.append(websocket)
            else:
                await websocket.send("Host not connected!")
                return
        async for message in websocket:
            pass

    async def start_game(self, connections):
        self.counter += 1
        self.game = connections
        websockets.broadcast(connections, f"Game{self.counter} started!")


async def main():
    network_manager = NetworkManager()
    async with websockets.serve(network_manager.handle_connection, "localhost", 42069):
        await asyncio.Future()


asyncio.run(main())
