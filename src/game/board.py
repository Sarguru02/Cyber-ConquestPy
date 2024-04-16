from .property import Property
class Board:
    def __init__(self):
        self.board = []

    def add(self, property: Property):
        self.board.append(property)
