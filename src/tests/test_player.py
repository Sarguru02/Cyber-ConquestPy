from game.property import Player, Property

import unittest

class TestPlayer(unittest.TestCase):
    def test_name(self):
        player = Player("Player1")
        self.assertNotEqual(player.name, 'Bank')
