import random
from . import property as Props
from .property import DEFAULT_BOARD
from .property import Player


class GameManager:
    def __init__(self):
        self.board = DEFAULT_BOARD
        self.players = []
        self.current_player = None
        self.current_turn = 0

    def add_player(self, name):
        player = Player(name)
        print(player)
        self.players.append(player)

    def handleLanding(self, landingBox, dicevalue):
        if (landingBox.type == Props.JAIL):
            # the player should not be able to move for 3 turns
            # the player should be released in the game loop when his turn comes
            self.current_player.inJail = True
            return "You are in jail"
        if (landingBox.type == Props.GO):
            # the player should get 200
            return "You got 200"
        if (landingBox.type == Props.CHANCE):
            # define method for chance - if even dice value, get money. if odd dice value, lose money
            return self.handleChance(dicevalue)
        if (landingBox.type == Props.COMMUNITY_CHEST):
            # define method for community chest - if even dice value, lose money. if odd dice value, get money
            return self.handleCommunityChest(dicevalue)

        if (landingBox.type == Props.INCOME_TAX):
            # the player should lose 200 for every property he owns
            self.current_player.cash -= 200 * \
                len(self.current_player.properties)
            return "You paid 200 for each property you own"

        if (landingBox.type == Props.KRONOS):
            self.current_player.cash = int(self.current_player.cash*0.9)
            return "kronos"

        if (landingBox.type == Props.CRYPTO_LOCKER):
            for i in range(len(self.current_player.properties)//2):
                self.current_player.properties[-1].owner = "Bank"
                self.current_player.properties.pop()
            return "You lost half of your properties"

    def print_board(self):
        for box in self.board:
            print(box)
        return

    def handleChance(self):
        ch = random.randint(1, 7)
        if ch == 1:
            document = {
                **self.current_player,
                'cash': int(self.current_player.cash) + 100,
                'position': self.current_player.position,
            }
            print(f"Document: {document}")
            print(f"Title: Hackathon Victory")
            print(
                f"Message: Congratulations You won a hackathon. Collect $100 as a reward for your coding skills")
            print(f"Balance: {document['cash']}")
        elif ch == 2:
            document2 = {
                **self.current_player,
                'cash': int(self.current_player.cash) + 50,
                'position': self.current_player.position,
            }
            print(f"Document: {document2}")
            print(f"Title: Bug Bounty Payout")
            print(
                f"Message: Report a Critical Bug and receive a reward of $50 from a tech giant. Collect $50")
            print(f"Balance: {document2['cash']}")
        elif ch == 3:
            document3 = {
                **self.current_player,
                'cash': int(self.current_player.cash) - 50 if int(self.current_player.cash) - 50 > 0 else 0,
                'position': self.current_player.position + 3,
            }
            print(f"Document: {document3}")
            print(f"Title: Tech Conference")
            print(f"Message: Attend a tech conference. Pay $50 for the conference fee. Gain knowledge and advance 3 spaces.")
            print(f"Balance: {document3['cash']}")
        elif ch == 4:
            document4 = {
                **self.current_player,
                'cash': int(self.current_player.cash) - 50 if int(self.current_player.cash) - 50 > 0 else 0,
                'position': self.current_player.position,
            }
            print(f"Document: {document4}")
            print(f"Title: Cryptolocker Virus")
            print(f"Message: Your computer has been infected with Cryptolocker Pay a $50 ransom to unlock your files.")
            print(f"Balance: {document4['cash']}")
        elif ch == 5:
            document5 = {
                **self.current_player,
                'cash': int(self.current_player.cash) + 20,
                'position': self.current_player.position,
            }
            print(f"Document: {document5}")
            print(f"Title: Tech Startup")
            print(f"Message: Collect $20 as an investment in your company.")
            print(f"Balance: {document5['cash']}")
        elif ch == 6:
            if 'propertiesOwned' in self.current_player:
                document6 = {
                    **self.current_player,
                    'cash': int(self.current_player.cash) + 25 * len(self.current_player['propertiesOwned']),
                    'position': self.current_player.position,
                }
                print(f"Document: {document6}")
                print(f"Title: Cryptocurrency Investment")
                print(
                    f"Message: Invest in cryptocurrency early. Collect $25 for each property you own.")
                print(f"Balance: {document6['cash']}")
        elif ch == 7:
            document7 = {
                **self.current_player,
                'cash': int(self.current_player.cash) + 50,
                'position': self.current_player.position,
            }
            print(f"Document: {document7}")
            print(f"Title: Tech Patent")
            print(f"Message: Collect $50 in royalties.")
            print(f"Balance: {document7['cash']}")
        else:
            print("Default case")

    def handleCommunityChest(self):
        ch = random.randint(1, 8)
        if ch == 1:
            document = {
                **self.current_player,
                'cash': int(self.current_player.cash) + 50,
                'position': self.current_player.position,
            }
            print(f"Document: {document}")
            print(f"Title: Open-Source Contribution")
            print(
                "Message: Contribute to an open-source project. Collect $50 in recognition of your tech skills.")
            print(f"Balance: {document['cash']}")
        elif ch == 2:
            document2 = {
                **self.current_player,
                'cash': int(self.current_player.cash) - 25 if int(self.current_player.cash) - 25 > 0 else 0,
                'position': self.current_player.position,
            }
            print(f"Document: {document2}")
            print(f"Title: Virus Scan")
            print(
                "Message: Your antivirus software has detected a virus. Pay $25 for cleanup.")
            print(f"Balance: {document2['cash']}")
        elif ch == 3:
            document3 = {
                **self.current_player,
                'cash': int(self.current_player.cash) + 100,
                'position': self.current_player.position,
            }
            print(f"Document: {document3}")
            print(f"Title: Tech IPO")
            print("Message: Your tech company is going public. Collect $100")
            print(f"Balance: {document3['cash']}")
        elif ch == 4:
            document4 = {
                **self.current_player,
                'cash': int(self.current_player.cash) + 10,
                'position': self.current_player.position,
            }
            print(f"Document: {document4}")
            print(f"Title: Tech Blog")
            print(
                "Message: Your tech blog gains popularity. Collect $10 as advertising revenue.")
            print(f"Balance: {document4['cash']}")
        elif ch == 5:
            document5 = {
                **self.current_player,
                'cash': int(self.current_player.cash) + 60,
                'position': self.current_player.position,
            }
            print(f"Document: {document5}")
            print(f"Title: Virtual Reality Project")
            print(
                "Message: Work on a VR project. Collect $60 for your futuristic creation.")
            print(f"Balance: {document5['cash']}")
        elif ch == 6:
            document6 = {
                **self.current_player,
                'cash': int(self.current_player.cash) - 75 if int(self.current_player.cash) - 75 > 0 else 0,
                'position': self.current_player.position,
            }
            print(f"Document: {document6}")
            print(f"Title: Tech Acquisition")
            print("Message: Acquire a rival tech startup. Pay $75 for the purchase.")
            print(f"Balance: {document6['cash']}")
        elif ch == 7:
            document7 = {
                **self.current_player,
                'cash': int(self.current_player.cash) - 50 if int(self.current_player.cash) - 50 > 0 else 0,
                'position': self.current_player.position,
            }
            print(f"Document: {document7}")
            print(f"Title: Smart Home Upgrade")
            print("Message: Upgrade your home with smart tech. Pay $50 for the upgrade.")
            print(f"Balance: {document7['cash']}")
        elif ch == 8:
            if 'propertiesOwned' in self.current_player:
                document8 = {
                    **self.current_player,
                    'cash': int(self.current_player.cash) + 25 * len(self.current_player['propertiesOwned']),
                    'position': self.current_player.position,
                }
                print(f"Document: {document8}")
                print(f"Title: BlockChain Investment")
                print(
                    "Message: Invest in blockchain technology. Collect $25 for each property you own.")
                print(f"Balance: {document8['cash']}")
        else:
            print("Default case")

    def start(self):
        self.current_player = self.players[0]
        self.print_board()
        while True:
            if (self.current_player.inJail):
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
                f"{self.current_player.name} moved to {self.board[self.current_player.position].property_name}")
            self.handleLanding(landedBox, dice)
            blabla = input("What would you like to do?")
            if (blabla == "buy"):
                print(self.current_player.buy_property(
                    self.board[self.current_player.position]))
                print(self.current_player)
            elif (blabla == "sell"):
                print(self.current_player.sell_property(
                    self.board[self.current_player.position], self.players[1]))
                print(self.current_player)
            elif (blabla == "quit"):
                break
            print(self.current_player)
            self.current_turn += 1
            self.current_player = self.players[self.current_turn % len(
                self.players)]
