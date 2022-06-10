import unittest
from main import *


class Tests(unittest.TestCase):
    def test_check_sequence(self):
        """this function tests if the sequence is correctly recognized

        GIVEN: a sequence chosen by a player and a sequence of coin tosses
        WHEN: I check if the sequence chosen by a player appears in the coin tosses
        THEN: function returns True if sequence chosen appears in the coin tosses, False if not
        """
        self.assertTrue(check_sequence('TTH', 'TTH'))
        self.assertFalse(check_sequence('TTH', 'HTH'))
        self.assertFalse(check_sequence('TTH', 'HT'))
        self.assertFalse(check_sequence('TTH', 'H'))
        self.assertFalse(check_sequence('TTH', ''))
        self.assertTrue(check_sequence('TTH', 'HTHTTH'))

    def test_check_victory(self):
        """this function tests if check_victory returns the correct value

        GIVEN: the two sequences chosen by players and a sequence of coin tosses
        WHEN: I check which player wins
        THEN: function returns the value I expect
        """
        self.assertEqual(check_victory('TTH', 'TTT', 'TTH'), 0)
        self.assertEqual(check_victory('TTH', 'TTT', ''), -1)
        self.assertEqual(check_victory('TTH', 'TTT', 'TTT'), 1)
        self.assertEqual(check_victory('TTH', 'TTT', 'HHHTTH'), 0)

    def test_gamemove(self):
        """this function tests if gamemove appends the correct toss

         GIVEN: probability to toss a T, sequences chosen by the two players and a sequence of coin tosses
         WHEN: I append a new toss to the sequence
         THEN: function appends the new toss correctly and returns the sequence after the toss and the player who won
         """
        self.assertEqual(gamemove(0, 'TTT', 'TTH', '')[0], 'H')
        self.assertEqual(len(gamemove(0.5, 'TTT', 'TTH', '')[0]), 1)
        self.assertEqual(len(gamemove(0.5, 'TTT', 'TTH', 'TTTT')[0]), 5)
        self.assertEqual(gamemove(0, 'TTH', 'TTT', 'TT')[1], 0)
        self.assertEqual(gamemove(1, 'TTH', 'TTT', 'TT')[1], 1)
        self.assertEqual(gamemove(1, 'TTT', 'TTH', '')[1], -1)

    def test_gameloop(self):
        """this function tests if gameloop returns the correct number

        GIVEN: probability to toss a T and the two sequences chosen by players
        WHEN: I play the game multiple times
        THEN: function returns the number of times player 1 won divided by total number of games played"""
        self.assertEqual(gameloop(1, 'TTT', 'TTH'), 1)


if __name__ == '__main__':
    unittest.main()
