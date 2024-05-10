import random
from game.property import DEFAULT_BOARD
from game.property import Player

class Game:
    def __init__(self):
        self.board = DEFAULT_BOARD
        self.players = []
        self.current_player = None
        self.current_turn = 0

    def add_player(self, name ):
        player = Player(name)
        print(player)
        self.players.append(player)

    def start(self):
        self.current_player = self.players[0]
        while True:
            print(f"{self.current_player.name}'s turn")
            print("Rolling dice...")
            dice = random.randint(1, 6) + random.randint(1, 6)
            print(f"Dice: {dice}")
            self.current_player.move(dice)
            print(f"{self.current_player.name} moved to {self.board[self.current_player.position].property_name}")
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


game = Game()
game.add_player("Player1")
game.add_player("Player2")
game.start()
