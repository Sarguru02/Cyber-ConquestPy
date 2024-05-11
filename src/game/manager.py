import random
from . import property as Props
from .property import DEFAULT_BOARD
from .property import Player


class manager:
    def __init__(self):
        self.board = DEFAULT_BOARD
        self.players = []
        self.current_player = None
        self.current_turn = 0

    def add_player(self, name, socket=None):
        player = Player(name, socket=socket)
        print(player)
        self.players.append(player)

    def handleLanding(self, landingBox, dicevalue):
        if landingBox.type == Props.JAIL:
            # the player should not be able to move for 3 turns
            # the player should be released in the game loop when his turn comes
            self.current_player.inJail = True
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
            self.current_player.cash -= 200 * \
                len(self.current_player.properties)
            return "You paid 200 for each property you own"

        if landingBox.type == Props.KRONOS:
            self.current_player.cash = int(self.current_player.cash * 0.9)
            return "kronos"

        if landingBox.type == Props.CRYPTO_LOCKER:
            for i in range(len(self.current_player.properties) // 2):
                self.current_player.properties[-1].owner = "Bank"
                self.current_player.properties.pop()
            return "You lost half of your properties"

        if landingBox.type == Props.NORMAL:
            if (landingBox.owner != "Bank"):
                if (landingBox.owner != self.current_player):
                    self.current_player.cash -= int(landingBox.price * 0.1)
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
        ch = random.randint(1, 7)
        if ch == 1:
            self.current_player.cash += 100
            return (
                "You won a hackathon. Collect $100 as a reward for your coding skills"
            )
        elif ch == 2:
            self.current_player.cash += 50
            return "Report a Critical Bug and receive a reward of $50 from a tech giant. Collect $50"
        elif ch == 3:
            self.current_player.cash = max(0, self.current_player.cash - 50)
            self.current_player.position += 3
            return "Attend a tech conference. Pay $50 for the conference fee. Gain knowledge and advance 3 spaces."
        elif ch == 4:
            self.current_player.cash = max(0, self.current_player.cash - 50)
            return "Your computer has been infected with Cryptolocker Pay a $50 ransom to unlock your files."
        elif ch == 5:
            self.current_player.cash += 20
            return "Collect $20 as an investment in your company."
        elif ch == 6:
            if len(self.current_player.properties) > 0:
                self.current_player.cash += 25 * \
                    len(self.current_player.properties)
                return "Invest in cryptocurrency early. Collect $25 for each property you own."
        elif ch == 7:
            self.current_player.cash += 50
            return "Collect $50 in royalties."

    def handleCommunityChest(self, ch):
        ch = random.randint(1, 8)
        if ch == 1:
            self.current_player.cash += 50
            return "Contribute to an open-source project. Collect $50 in recognition of your tech skills."
        elif ch == 2:
            self.current_player.cash = max(0, self.current_player.cash - 25)
            return "Your antivirus software has detected a virus. Pay $25 for cleanup."
        elif ch == 3:
            self.current_player.cash += 100
            return "Your tech company is going public. Collect $100"
        elif ch == 4:
            self.current_player.cash += 10
            return (
                "Your tech blog gains popularity. Collect $10 as advertising revenue."
            )
        elif ch == 5:
            self.current_player.cash += 60
            return "Work on a VR project. Collect $60 for your futuristic creation."
        elif ch == 6:
            self.current_player.cash = max(0, self.current_player.cash - 75)
            return "Acquire a rival tech startup. Pay $75 for the purchase."
        elif ch == 7:
            self.current_player.cash = max(0, self.current_player.cash - 50)
            return "Upgrade your home with smart tech. Pay $50 for the upgrade."
        elif ch == 8:
            if len(self.current_player.properties) > 0:
                self.current_player.cash += 25 * \
                    len(self.current_player.properties)
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
            self.current_player = self.players[self.current_turn % len(
                self.players)]
