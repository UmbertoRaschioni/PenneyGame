import unittest
from main import *

class Tests(unittest.TestCase):
    def test_check_sequence(self):
        self.assertTrue(check_sequence('TTT', 'TTT'))
        self.assertTrue(check_sequence('TTH', 'TTH'))
        self.assertFalse(check_sequence('TTH', 'HTH'))
        self.assertFalse(check_sequence('TTH', 'HT'))
        self.assertFalse(check_sequence('TTH', 'H'))
        self.assertFalse(check_sequence('TTH', ''))

    def test_check_victory(self):
        self.assertEqual(check_victory('TTH','TTT','TTH'), 0)
        self.assertEqual(check_victory('TTH', 'TTT', ''), -1)
        self.assertEqual(check_victory('TTH', 'TTT', 'TTT'), 1)

    def test_gamemove(self):
        self.assertEqual(gamemove(0, 'TTT', 'TTT', '')[0], 'H')
        self.assertEqual(len(gamemove(0, 'TTT', 'TTT', '')[0]), 1)
        self.assertEqual(len(gamemove(0, 'TTT', 'TTT', 'TTTT')[0]), 5)
        self.assertEqual(gamemove(0, 'TTH', 'TTT', 'TT')[1], 0)
        self.assertEqual(gamemove(1, 'TTH', 'TTT', 'TT')[1], 1)




if __name__ == '__main__':
    unittest.main()