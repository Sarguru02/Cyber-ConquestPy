import asyncio
import websockets

class NetworkManager:
    def __init__(self):
        self.connections = []
        self.game = None
        self.started = asyncio.Event()
        self.counter = 0

    async def handle_connection(self, websocket):
        self.connections.append(websocket)
        websockets.broadcast(self.connections, "New player connected!")
        if len(self.connections) >= 2:
            await self.start_game(self.connections[:2])
            self.connections = self.connections[2:]
        async for message in websocket:
            print(f"Received message: {message}")
            await websocket.send("Hello, world!")

    async def start_game(self, connections):
        self.counter += 1
        self.game = connections
        websockets.broadcast(connections, f"Game{self.counter} started!")

async def main():
    network_manager = NetworkManager()
    async with websockets.serve(network_manager.handle_connection, "localhost", 42069):
        await asyncio.Future()

asyncio.run(main())
