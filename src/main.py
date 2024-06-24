import asyncio
import websockets
import random
import json
from urllib.parse import parse_qs

from game.manager import manager

PORT = 42069




class ws:
    def __init__(self, websocket) -> None:
        self.socket = websocket
        self.room: str = ''

class NetworkManager:
    def __init__(self):
        self.game: dict[str, manager]= {}
        self.counter = 0

    async def handle_connection(self, websocket, path):
        query_string = path.split("?")[-1]
        params = parse_qs(query_string)
        user = params.get('type', [''])[0]
        name = params.get('name', [''])[0]
        if user == "host":
            await self.hostHandler(ws(websocket), name)
        if user == "player":
            await self.playerHandler(ws(websocket), name)
        else:
            print("Invalid user type")
            await websocket.send("Invalid user type")


    async def hostHandler(self, ws: ws, name):
        print('[INFO]host connected:', name)
        async def sendInfo(msg: str):
            obj = {'type': 'info', 'params': {'message': msg}}
            await ws.socket.send(json.dumps(obj))

        async def sendError(err: str):
            obj = {'type': 'error', 'params': {'message': err}}
            await ws.socket.send(json.dumps(obj))

        def create():
            room = self.gen_key()
            ws.room = room
            self.game[room] = manager(ws)
            return room

        async def reconnect(params):
            room = params['key']
            if room not in self.game:
                print("Room not available")
                await sendError("Room not available")
                return
            self.game[room].host = ws
            ws.room = room
            await sendInfo(f"Reconnected to room {room}")

        async for message in ws.socket:
            msg = json.loads(message)
            print("message from host: ", msg)
            params = msg['params']
            typeHost = msg['type']
            if typeHost == 'reconnect':
                await reconnect(params)

            if typeHost == 'create':
                room = create()
                print(f"[INFO]: room created [{room}] ")
                await ws.socket.send(json.dumps({"type": "info", "key": room}))

            if typeHost == 'start':
                if(ws.room != ''):
                    await self.game[ws.room].start_game()
                else:
                    await sendInfo("You are not in any room")


    async def playerHandler(self, ws: ws, name):
        async def sendInfo(msg: str):
            obj = {'type': 'info', 'params': {'message': msg}}
            await ws.socket.send(json.dumps(obj))

        async def genInfo(ws):
            obj = {"type": "info", "params":{'players': [vars(p)['name'] for p in self.game[ws.room].players ]}}
            await self.game[ws.room].host.socket.send(json.dumps(obj))

        async def join(params):
            room = params['code']
            if room not in self.game:
                return "Room not available"
            
            self.game[room].add_player(name, ws=ws)
            ws.room = room
            await genInfo(ws)
            return f"Joined room {room}"
        
        def leave():
            room = ws.room
            ws.room = ''
            self.game[room].remove_player(ws)
            return "Left room"

        async def play(params):
            g = self.game[ws.room]
            await g.move(params['dice'])
            print("Play method called")

        print('[INFO] player connected:', name)
        async for message in ws.socket:
            msg = json.loads(message)
            params = msg['params']
            if msg["type"] == "join":
                joinmsg = await join(params)
                if joinmsg == "Room not available":
                    await sendInfo(joinmsg)
                    break
                print(joinmsg)
                await sendInfo(joinmsg)
            if msg['type'] == 'play':
                await play(params)
            if msg["type"] == 'leave':
                leave()
            if msg['type'] == "disconnect":
                pass
            if msg['type'] == 'setJail':
                g = self.game[ws.room]
                var = g.players[g.current_turn].inJail
                g.players[params['player']].inJail = not var
            if msg['type'] == 'actions':
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
