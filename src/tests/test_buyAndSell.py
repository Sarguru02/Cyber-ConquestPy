from game.property import Player, Property

import unittest

class TestBuyAndSell(unittest.TestCase):
    def test_buy_property(self):
        property = Property('Test Property', 1000, True)
        player1 = Player('Player 1')

        player1.buy_property(property)
        self.assertEqual(player1.cash, 9000)
        self.assertIs(property.owner, player1)
        self.assertIn(property, player1.properties)

    def test_sell_property(self):
        property = Property('Test Property', 1000, True)
        player1 = Player('Player 1')
        player2 = Player('Player 2')

        player1.buy_property(property)
        player1.sell_property(property, player2)
        self.assertEqual(player1.cash, 10000)
        self.assertNotIn(property, player1.properties)
        self.assertIs(property.owner, player2)
        self.assertIn(property, player2.properties)
        self.assertEqual(player2.cash, 9000)
