from game.board import Board
from game.property import Player, Property

import unittest

class TestPlayer(unittest.TestCase):
    def test_name(self):
        player = Player("Bank")
        self.assertNotEqual(player.name, 'Bank')
