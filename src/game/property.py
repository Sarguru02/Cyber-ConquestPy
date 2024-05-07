from typing import Self

BOARD_SIZE = 32


class Property:
    def __init__(self, property_name, price, isbuyable: bool, color=None):
        self.property_name = property_name
        self.price = price
        if isbuyable:
            self.owner = "Bank"
            self.color = color
        else:
            self.owner = None


class Player:
    def __init__(self, name) -> None:
        self.properties = []
        self.name = name
        self.cash = 10000
        self.getOutOfJailFree = 0
        self.inJail = False
        self.position = 0

    def buy_property(self, property):
        if property.owner is None:
            return "Not a property"

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

    def changePosition(self, dicevalue):
        self.position = (self.position + dicevalue) % BOARD_SIZE
