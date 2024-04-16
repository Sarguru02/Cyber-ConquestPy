from typing import Self


class Property:
    def __init__(self, property_name, price, owner="Bank"):
        self.property_name = property_name
        self.price = price
        self.owner = owner


class Player:
    def __init__(self, name) -> None:
        self.properties = []
        self.name = name
        self.cash = 10000
        self.getOutOfJailFree = 0
        self.inJail = False
        self.position = 0

    def buy_property(self, property):
        if self.cash >= property.price:
            self.properties.append(property)
            self.cash -= property.price
            property.owner = self
            return "Property bought"
        return "Insufficient funds"

    def sell_property(self, property, new_owner: Self):
        if property in self.properties:
            self.properties.remove(property)
            new_owner.properties.append(property)
            property.owner = new_owner
            self.cash += property.price
            new_owner.cash -= property.price
            return "Property sold"
        return "Property not owned"
