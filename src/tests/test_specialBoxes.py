import unittest
from game.manager import manager

class SpecialBoxes(unittest.TestCase):
    def test_RIP(self):
        m = manager()
        m.add_player("Player1")
        m.current_player = m.players[0]
        m.handleLanding(m.board[9], 9)
        self.assertEqual(m.current_player.cash, 10000)

    def test_chance(self):
        m = manager()
        m.add_player("Player1")
        m.current_player = m.players[0]
        m.handleLanding(m.board[10], 7)
        bla = m.current_player.cash
        self.assertNotEqual(m.current_player.cash, 10000)
        m.handleLanding(m.board[22], 7)
        self.assertNotEqual(bla, m.current_player.cash)

    def test_communityChest(self):
        m = manager()
        m.add_player("Player1")
        m.current_player = m.players[0]
        m.handleLanding(m.board[2], 2)
        bla = m.current_player.cash
        self.assertNotEqual(m.current_player.cash, 10000)
        m.handleLanding(m.board[18], 17)
        self.assertNotEqual(bla, m.current_player.cash)

    def test_jail(self):
        m = manager()
        m.add_player("Player1")
        m.current_player = m.players[0]
        self.assertEqual(m.current_player.inJail, False)
