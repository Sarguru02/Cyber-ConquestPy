import asyncio
import websockets
import random
import json

from game.manager import manager

PORT = 42069


class ws:
    def __init__(self, websocket) -> None:
        self.socket = websocket
        self.room = None

class NetworkManager:
    def __init__(self):
        self.game: dict[str, manager]= {}
        self.counter = 0

    async def handle_connection(self, websocket, path):
        params = path.split("?")[-1].split("&")
        user = params[0].split("=")[-1]
        name = params[1].split("=")[-1]
        if user == "host":
            await self.hostHandler(ws(websocket), name)
        if user == "player":
            await self.playerHandler(ws(websocket), name)


    async def hostHandler(self, ws: ws, name):
        print('host connected:', name)
        room = self.gen_key()
        await ws.socket.send(json.dumps({"key": room}))
        self.game[room] = manager()
        self.game[room].host = ws.socket
        async for message in ws.socket:
            msg = json.loads(message)
            print(msg)
            await ws.socket.send(message)

    async def playerHandler(self, ws: ws, name):
        async def genInfo(ws):
            obj = {"type": "info", "params":{'players': [vars(p)['name'] for p in self.game[ws.room].players ]}}
            await self.game[ws.room].host.send(json.dumps(obj))

        async def join(params):
            room = params['code']
            if room not in self.game:
                return "Room not available"
            
            self.game[room].add_player(name, socket=ws.socket)
            ws.room = room
            await genInfo(ws)
            return "Joined room"
        
        def leave():
            room = ws.room
            ws.room = None
            self.game[room].remove_player(ws.socket)
            return "Left room"

        print('player connected:', name)
        async for message in ws.socket:
            print(message)
            msg = json.loads(message)
            params = msg['params']
            if msg["type"] == "join":
                joinmsg = await join(params)
                if joinmsg == "Room not available":
                    await ws.socket.send(joinmsg)
                    break
                await ws.socket.send(joinmsg)
            if msg['type'] == 'play':
                pass
            if msg["type"] == 'leave':
                leave()
            if msg['type'] == "disconnect":
                pass

    def gen_key(self):
        chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
        key="CC"
        for i in range(6):
            key += random.choice(chars)
        return key


async def main():
    network_manager = NetworkManager()
    async with websockets.serve(network_manager.handle_connection, "localhost", PORT):
        print("Listening on port", PORT)
        await asyncio.Future()


asyncio.run(main())
