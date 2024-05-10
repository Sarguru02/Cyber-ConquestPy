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

    def add_player(self, name ):
        player = Player(name)
        print(player)
        self.players.append(player)

    def handleLanding(self, landingBox, dicevalue):
        if(landingBox.type == Props.JAIL):
            # the player should not be able to move for 3 turns
            # the player should be released in the game loop when his turn comes
            self.current_player.inJail = True
            return "You are in jail"
        if(landingBox.type== Props.GO):
            # the player should get 200
            return "You got 200"
        if(landingBox.type == Props.CHANCE):
            # define method for chance - if even dice value, get money. if odd dice value, lose money
            return self.handleChance(dicevalue)
        if(landingBox.type==Props.COMMUNITY_CHEST): 
            # define method for community chest - if even dice value, lose money. if odd dice value, get money
            return self.handleCommunityChest(dicevalue)

        if(landingBox.type==Props.INCOME_TAX):
            # the player should lose 200 for every property he owns
            self.current_player.cash -= 200 * len(self.current_player.properties)
            return "You paid 200 for each property you own"
        
        if(landingBox.type == Props.KRONOS):
            self.current_player.cash = int(self.current_player.cash*0.9)
            return "kronos"
        
        if(landingBox.type == Props.CRYPTO_LOCKER):
            for i in range(len(self.current_player.properties)//2):
                self.current_player.properties[-1].owner = "Bank"
                self.current_player.properties.pop()
            return "You lost half of your properties"

    def print_board(self):
        for box in self.board:
            print(box)
        return
    
    def handleChance(self, dicevalue):
        pass

    def handleCommunityChest(self, dicevalue):
        pass


    def start(self):
        self.current_player = self.players[0]
        self.print_board()
        while True:
            if(self.current_player.inJail):
                print(f"{self.current_player.name} is in CryptoLocker")
                self.current_player.inJail = False
                continue
            print(f"{self.current_player.name}'s turn")
            print("Rolling dice...")
            dice = random.randint(1, 6) + random.randint(1, 6)
            print(f"Dice: {dice}")
            self.current_player.move(dice)
            landedBox = self.board[self.current_player.position]
            print(f"{self.current_player.name} moved to {self.board[self.current_player.position].property_name}")
            self.handleLanding(landedBox, dice)
            blabla = input("What would you like to do?")
            if(blabla == "buy"):
                print(self.current_player.buy_property(self.board[self.current_player.position]))
                print(self.current_player)
            elif(blabla == "sell"):
                print(self.current_player.sell_property(self.board[self.current_player.position], self.players[1]))
                print(self.current_player)
            elif(blabla == "quit"):
                break
            print(self.current_player)
            self.current_turn += 1
            self.current_player = self.players[self.current_turn % len(self.players)]
