import asyncio
import websockets
from game.manager import manager
import random
import json


class NetworkManager:
    def __init__(self):
        self.game = manager()
        self.started = asyncio.Event()
        self.host = None
        self.counter = 0

    async def handle_connection(self, websocket, path):
        params = path.split("?")[-1].split("&")
        user = params[0].split("=")[-1]
        name = params[1].split("=")[-1]
        if user == "host":
            if self.host is None:
                await self.hostHandler(websocket, name)
            else:
                await websocket.send("Host is already connected")
        if user == "player":
            await self.playerHandler(websocket, name)

    async def hostHandler(self, websocket, name):
        self.host = websocket
        print('host connected:', name)
        key = self.gen_key()
        await websocket.send(json.dumps({"key": key}))
        async for message in websocket:
            msg = json.loads(message)
            print(msg)

    async def playerHandler(self, websocket, name):
        self.game.add_player(name, websocket)
        async for message in websocket:
            msg = json.loads(message)
            print(msg)

    async def start_game(self, connections):
        self.counter += 1
        self.game = connections
        websockets.broadcast(connections, f"Game{self.counter} started!")

    def gen_key(self):
        n = random.randint(1000, 9999)
        return f"CC{n}"


async def main():
    network_manager = NetworkManager()
    async with websockets.serve(network_manager.handle_connection, "localhost", 42069):
        await asyncio.Future()


asyncio.run(main())
