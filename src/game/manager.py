import json
import random
from typing import List

from . import property as Props
from .property import DEFAULT_BOARD
from .property import Player

async def sendmsg(socket, msg):
    await socket.send(json.dumps({'type': 'message', 'params': {'message': msg}}))


class manager:
    def __init__(self, host):
        self.board = DEFAULT_BOARD
        self.players: List[Player] = []
        self.current_turn = 0
        self.host= host

    def add_player(self, name, ws):
        player = Player(name, socket=ws)
        self.players.append(player)

    def remove_player(self, ws):
        self.players = [p for p in self.players if p.ws is not ws]


    def handleLanding(self, landingBox, dicevalue):
        current_player = self.players[self.current_turn]
        # this function handles all the landing boxes and special boxes. Special boxes are the ones given in the constants in Props
        if landingBox.type == Props.JAIL:
            # the player should not be able to move for 3 turns
            # the player should be released in the game loop when his turn comes
            current_player.inJail = True
            return "You are in jail"
        if landingBox.type == Props.GO:
            # the player should get 200
            return "You got 200"
        if landingBox.type == Props.CHANCE:
            # define method for chance - if even dice value, get money. if odd dice value, lose money
            return self.handleChance(dicevalue)
        if landingBox.type == Props.COMMUNITY_CHEST:
            # define method for community chest - if even dice value, lose money. if odd dice value, get money
            return self.handleCommunityChest(dicevalue)

        if landingBox.type == Props.INCOME_TAX:
            # the player should lose 200 for every property he owns
            current_player.cash -= 200 * len(current_player.properties)
            return "You paid 200 for each property you own"

        if landingBox.type == Props.KRONOS:
            current_player.cash = int(current_player.cash * 0.9)
            return "kronos"

        if landingBox.type == Props.CRYPTO_LOCKER:
            for i in range(len(current_player.properties) // 2):
                current_player.properties[-1].owner = "Bank"
                current_player.properties.pop()
            return "You lost half of your properties"

        if landingBox.type == Props.NORMAL:
            if landingBox.owner != "Bank":
                if landingBox.owner != current_player:
                    current_player.cash -= int(landingBox.price * 0.1)
                    landingBox.owner.cash += int(landingBox.price * 0.1)
                    return "You gotta pay the rent! 🙃"
                return "Enjoy your property bruhh 👍"
            else:
                return "You can buy this if you want... 🤷‍♂️"

    def print_board(self):
        for box in self.board:
            print(box)
        return

    def handleChance(self, ch):
        current_player = self.players[self.current_turn]
        ch = random.randint(1, 7)
        if ch == 1:
            current_player.cash += 100
            return (
                "You won a hackathon. Collect $100 as a reward for your coding skills"
            )
        elif ch == 2:
            current_player.cash += 50
            return "Report a Critical Bug and receive a reward of $50 from a tech giant. Collect $50"
        elif ch == 3:
            current_player.cash = max(0, current_player.cash - 50)
            current_player.position += 3
            return "Attend a tech conference. Pay $50 for the conference fee. Gain knowledge and advance 3 spaces."
        elif ch == 4:
            current_player.cash = max(0, current_player.cash - 50)
            return "Your computer has been infected with Cryptolocker Pay a $50 ransom to unlock your files."
        elif ch == 5:
            current_player.cash += 20
            return "Collect $20 as an investment in your company."
        elif ch == 6:
            if len(current_player.properties) > 0:
                current_player.cash += 25 * len(current_player.properties)
                return "Invest in cryptocurrency early. Collect $25 for each property you own."
        elif ch == 7:
            current_player.cash += 50
            return "Collect $50 in royalties."

    def handleCommunityChest(self, ch):
        current_player = self.players[self.current_turn]
        ch = random.randint(1, 8)
        if ch == 1:
            current_player.cash += 50
            return "Contribute to an open-source project. Collect $50 in recognition of your tech skills."
        elif ch == 2:
            current_player.cash = max(0, current_player.cash - 25)
            return "Your antivirus software has detected a virus. Pay $25 for cleanup."
        elif ch == 3:
            current_player.cash += 100
            return "Your tech company is going public. Collect $100"
        elif ch == 4:
            current_player.cash += 10
            return (
                "Your tech blog gains popularity. Collect $10 as advertising revenue."
            )
        elif ch == 5:
            current_player.cash += 60
            return "Work on a VR project. Collect $60 for your futuristic creation."
        elif ch == 6:
            current_player.cash = max(0, current_player.cash - 75)
            return "Acquire a rival tech startup. Pay $75 for the purchase."
        elif ch == 7:
            current_player.cash = max(0, current_player.cash - 50)
            return "Upgrade your home with smart tech. Pay $50 for the upgrade."
        elif ch == 8:
            if len(current_player.properties) > 0:
                current_player.cash += 25 * len(current_player.properties)
                return "Invest in blockchain technology. Collect $25 for each property you own."
            return "Do nothing"
        else:
            return "Default case"

    def start(self):
        self.current_player = self.players[0]
        self.print_board()
        while True:
            if self.current_player.inJail:
                print(f"{self.current_player.name} is in CryptoLocker")
                self.current_player.inJail = False
                continue
            print(f"{self.current_player.name}'s turn")
            print("Rolling dice...")
            dice = random.randint(1, 6) + random.randint(1, 6)
            print(f"Dice: {dice}")
            self.current_player.move(dice)
            landedBox = self.board[self.current_player.position]
            print(
                f"{self.current_player.name} moved to {self.board[self.current_player.position].property_name}"
            )
            print(self.handleLanding(landedBox, dice))
            blabla = input("What would you like to do?")
            if blabla == "buy":
                print(
                    self.current_player.buy_property(
                        self.board[self.current_player.position]
                    )
                )
                print(self.current_player)
            elif blabla == "sell":
                print(
                    self.current_player.sell_property(
                        self.board[self.current_player.position], self.players[1]
                    )
                )
                print(self.current_player)
            elif blabla == "quit":
                break
            print(self.current_player)
            self.current_turn += 1
            self.current_player = self.players[self.current_turn % len(self.players)]


    
    async def start_game(self):
        random.shuffle(self.players)
        await self.notify_everyone("Game has started")
        self.current_turn = 0
        obj = {'type': 'info', 'params': {'message': "Its your turn now"}}
        cur = self.players[self.current_turn]
        await cur.ws.socket.send(json.dumps(obj))
        obj['params']['message'] = f"{cur.name}'s turn"
        await self.host.socket.send(json.dumps(obj))

    async def notify_everyone(self, msg):
        for player in self.players:
            await player.ws.socket.send(json.dumps({'type': 'message', 'params': {'message': msg}}))


    async def move(self, dice):
        cur = self.players[self.current_turn]
        cur.move(dice)
        msg = self.handleLanding(self.board[cur.position], dice)
        await sendmsg(cur.socket.socket, msg)
