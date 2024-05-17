from typing import Self

NORMAL = "normal"
CHANCE = "chance"
COMMUNITY_CHEST = "community_chest"
JAIL = "No Internet"
KRONOS = "kronos"
GO = "go"
INCOME_TAX = "income_tax"
CRYPTO_LOCKER = "crypto_locker"
RIP = "RIP"


class Property:
    def __init__(self, property_name, price, isBuyable: bool, type=NORMAL):
        self.property_name = property_name
        self.type = type
        if not isBuyable:
            self.owner = None
            price = None
        else:
            self.owner = "Bank"
        self.price = price

    def __str__(self) -> str:
        return f"Property {{name: {self.property_name}, price: {self.price}, owner: {self.owner}}}"


DEFAULT_BOARD = [
    Property("Go", None, False, GO),
    Property("Cloud", 1000, True),
    Property("Community Chest", None, False, COMMUNITY_CHEST),
    Property("DSA", 1000, True),
    Property("Income Tax", None, False, INCOME_TAX),
    Property("Memory Game", 1000, True),
    Property("Git", 1000, True),
    Property("Crypto Locker", None, False, CRYPTO_LOCKER),
    Property("Panchathanthiram", 1000, True),
    Property("RIP", None, False, RIP),
    Property("Chance", None, False, CHANCE),
    Property("Windows", 1000, True),
    Property("AI", 1000, True),
    Property("Connection", 1000, True),
    Property("No Internet", None, False, JAIL),
    Property("Linux", 1000, True),
    Property("Sales Pitch", 1000, True),
    Property("Cyber Security", 1000, True),
    Property("Community Chest", None, False, COMMUNITY_CHEST),
    Property("Current Affairs", 1000, True),
    Property("Blockchain", 1000, True),
    Property("Kronos", None, False, KRONOS),
    Property("Chance", None, False, CHANCE),
    Property("MCQ", 1000, True),
    Property("Fact Or Myth", 1000, True),
    Property("Tech Anagram", 1000, True),
    Property("Web Development", 1000, True),
    Property("Hist Places", 1000, True),
]


class Player:
    def __init__(self, name, socket=None) -> None:
        self.properties = []
        self.name = name
        self.cash = 10000
        self.getOutOfJailFree = 0
        self.inJail = False
        self.position = 0
        self.socket = socket

    def buy_property(self, property):
        if property.type is not NORMAL:
            return "Property not buyable"

        if self.cash < property.price:
            return "Insufficient funds"

        self.properties.append(property)
        self.cash -= property.price
        property.owner = self
        return "Property bought"

    def sell_property(self, property, new_owner: Self):
        if property not in self.properties:
            return "Property not owned"

        self.properties.remove(property)
        new_owner.properties.append(property)
        property.owner = new_owner
        self.cash += property.price
        new_owner.cash -= property.price
        return "Property sold"

    def move(self, dicevalue):
        if self.position + dicevalue >= len(DEFAULT_BOARD):
            self.cash += 200
        self.position = (self.position + dicevalue) % len(DEFAULT_BOARD)

    def __str__(self) -> str:
        return f"Player {self.name} has {self.cash} cash and {len(self.properties)} properties"
