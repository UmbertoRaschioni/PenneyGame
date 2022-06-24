import unittest
from main import check_sequence
from main import check_victory
from main import gamemove
from main import gameloop
from main import Situation


class Tests(unittest.TestCase):
    def test_check_same_sequence(self):
        """this function tests if the sequence is correctly recognized

        GIVEN: a sequence chosen by a player and a sequence of coin tosses which are the same
        WHEN: I check if the sequence chosen by a player appears in the coin tosses
        THEN: function returns True
        """
        self.assertTrue(check_sequence('TTH', 'TTH', 3))

    def test_check_different_sequence(self):
        """this function tests if the sequence is correctly recognized not to appear in the tosses

        GIVEN: a sequence chosen by a player and a sequence of coin tosses which are different
        WHEN: I check if the sequence chosen by a player appears in the coin tosses
        THEN: function return False
        """
        self.assertFalse(check_sequence('TTH', 'HTH', 3))

    def test_check_sequence_appears_at_the_end(self):
        """this function tests if the sequence is correctly recognized to appear in the sequence of coin tosses

        GIVEN: a sequence chosen by a player and a longer sequence of coin tosses
        WHEN: I check if the sequence chosen by a player appears in the coin tosses
        THEN: function returns True
        """
        self.assertTrue(check_sequence('TTH', 'HTHTTH', 3))

    def test_check_sequence_given_zero_coin_tosses(self):
        """this function tests if the sequence is correctly recognized given an empty sequence

        GIVEN: a sequence chosen by a player and an empty sequence of coin tosses
        WHEN: I check if the sequence chosen by a player appears in the coin tosses
        THEN: function returns False
        """
        self.assertFalse(check_sequence('TTH', '', 3))

    def test_check_sequence_given_one_coin_toss(self):
        """this function tests if the sequence is correctly recognized given a single coin toss

        GIVEN: a sequence chosen by a player and a single coin toss
        WHEN: I check if the sequence chosen by a player appears in the coin tosses
        THEN: function returns False
        """
        self.assertFalse(check_sequence('TTH', 'H', 3))

    def test_check_sequence_given_two_tosses(self):
        """this function tests if the sequence is correctly recognized given 2 tosses

        GIVEN: a sequence chosen by a player and 2 coin tosses
        WHEN: I check if the sequence chosen by a player appears in the coin tosses
        THEN: function returns False
        """
        self.assertFalse(check_sequence('TTH', 'TH', 3))

    def test_check_victory_player_one(self):
        """this function tests if check_victory returns the correct value

        GIVEN: the two sequences chosen by players and a sequence of coin tosses
        WHEN: I check which player wins
        THEN: function returns player 1 won
        """
        self.assertEqual(check_victory('TTH', 'TTT', 'TTH', 3), Situation.p1_wins)

    def test_check_victory_player_two(self):
        """this function tests if check_victory returns the correct value

        GIVEN: the two sequences chosen by players and a sequence of coin tosses
        WHEN: I check which player wins
        THEN: function returns player 2 won
        """
        self.assertEqual(check_victory('TTH', 'TTT', 'TTT', 3), Situation.p2_wins)

    def test_check_victory_of_nobody(self):
        """this function tests if check_victory returns the correct value

        GIVEN: the two sequences chosen by players and a sequence of coin tosses
        WHEN: I check which player wins
        THEN: function returns nobody won
        """
        self.assertEqual(check_victory('TTH', 'TTT', '', 3), Situation.nobody_won_yet)

    def test_check_victory_player_one_with_longer_sequence(self):
        """this function tests if check_victory returns the correct value

        GIVEN: the two sequences chosen by players and a sequence of coin tosses which are all 3 different
        WHEN: I check which player wins
        THEN: function returns player 1 won
        """
        self.assertEqual(check_victory('TTH', 'TTT', 'HHHTTH', 3), Situation.p1_wins)

    def test_gamemove_appending_to_sequence(self):
        """this function tests if gamemove appends H with probability=0

         GIVEN: zero-probability to toss a T, sequences chosen by the two players and a sequence of coin tosses
         WHEN: I append a new toss to the sequence
         THEN: function appends the new toss correctly and returns the sequence after the toss
         """
        self.assertEqual(gamemove(0, 'TTT', 'TTH', '', 3)[0], 'H')
        self.assertEqual(gamemove(1, 'TTT', 'TTH', '', 3)[1], Situation.nobody_won_yet)

    def test_gamemove_correct_lenght(self):
        """this function tests if lenght of gamemove is correct after a toss

        GIVEN: a probability to toss T, sequences chosen by the two players and a sequence of coin tosses
        WHEN: I append a new toss to the sequence
        THEN: lenght of gamemove is the number of coin tosses after appending a new toss
        """
        self.assertEqual(len(gamemove(0.5, 'TTT', 'TTH', 'TTTT', 3)[0]), 5)

    def test_gamemove_victory_player_one(self):
        """this function tests if gamemove returns the player who won

        GIVEN: zero-probability to toss T, sequences chosen by players and a sequence of coin tosses
        WHEN: I append a new toss to the sequence
        THEN: function returns player 1 won
        """
        self.assertEqual(gamemove(0, 'TTH', 'TTT', 'TT', 3)[1], Situation.p1_wins)

    def test_gamemove_victory_player_two(self):
        """this function tests if gamemove returns the player who won

        GIVEN: one-probability to toss T, sequences chosen by players and a sequence of coin tosses
        WHEN: I append a new toss to the sequence
        THEN: function returns player 2 won
        """
        self.assertEqual(gamemove(1, 'TTH', 'TTT', 'TT', 3)[1], Situation.p2_wins)

    def test_gamemove_victory_of_nobody(self):
        """this function tests if gamemove returns the player who won

        GIVEN: a probability to toss T, sequences chosen by players and a sequence of coin tosses
        WHEN: I append a new toss to the sequence
        THEN: function returns nobody won yet
        """
        self.assertEqual(gamemove(1, 'TTT', 'TTH', '', 3)[1], Situation.nobody_won_yet)

    def test_gameloop(self):
        """this function tests if gameloop returns the win ratio of player 1

        GIVEN: a zero-probability to toss T and sequences chosen by players
        WHEN: I play the game multiple times
        THEN: function returns a win ratio of 100%
        """
        self.assertEqual(gameloop(0, 'HHH', 'HHT', 3), 1)


if __name__ == '__main__':
    unittest.main()
