import numpy as np
import random
import math
import pickle
import tqdm


def check_sequence(s, sequence):
    """
    Check if s in sequence
    :param s: sequence chosen from p1 or p2
    :param sequence: sequence of coins tossed
    :return: True if s in sequence
    """
    return s in sequence[-3:]


def check_victory(s1, s2, sequence):
    """
    Check if someone won
    :param s1: sequence of p1
    :param s2: sequence of p2
    :param sequence: sequence of coins tossed
    :return: 0 if p1 won, 1 if p2 won, -1 if no one won
    """
    if check_sequence(s1, sequence):
        return 0
    if check_sequence(s2, sequence):
        return 1
    return -1


def gamemove(probability, s1, s2, sequence):
    sequence += random.choices('HT', weights=[1 - probability, probability], k=1)[0]
    ret = check_victory(s1, s2, sequence)
    return sequence, ret


def gameloop(probability, s1, s2):
    # setting number of victories for player 1 (p1w) and player 2 (p2w)
    # to zero
    p1w = 0
    # setting an empty initial sequence in order to append future tosses
    sequence = ""
    # playing the game 1000 times in order to have good statistics
    # (could be increased as you wish)
    tests = 100
    for number in range(tests):
        i = 0
        while True:
            sequence, ret = gamemove(probability, s1, s2, sequence)
            if ret == 0:
                p1w += 1
            if ret >= 0:
                break
            i += 1
        # sequence returns empty after each game

    return p1w / tests


if __name__ == "__main__":
    # p represents probability to toss T, it doesn't consider probabilities
    # under 0.1 and over 0.9 because the simulation would be too much long,
    # and the results are not interesting in those ranges
    p = np.arange(0.1, 0.9, 0.01)
    intransitiveness = np.zeros_like(p)
    # V is the victory matrix, each element of the matrix is the result of a
    # gameloop between two sequences, the for loop repeat everything for
    # different values of probability
    for n in tqdm.tqdm(range(len(p))):
        V = np.matrix([[0, gameloop(p[n - 1], "HHH", "HHT"), gameloop(p[n - 1], "HHH", "HTH"),
                        gameloop(p[n - 1], "HHH", "HTT"), gameloop(p[n - 1], "HHH", "THH"),
                        gameloop(p[n - 1], "HHH", "THT"), gameloop(p[n - 1], "HHH", "TTH"),
                        gameloop(p[n - 1], "HHH", "TTT")],
                       [gameloop(p[n - 1], "HHT", "HHH"), 0, gameloop(p[n - 1], "HHT", "HTH"),
                        gameloop(p[n - 1], "HHT", "HTT"), gameloop(p[n - 1], "HHT", "THH"),
                        gameloop(p[n - 1], "HHT", "THT"), gameloop(p[n - 1], "HHT", "TTH"),
                        gameloop(p[n - 1], "HHT", "TTT")],
                       [gameloop(p[n - 1], "HTH", "HHH"), gameloop(p[n - 1], "HTH", "HHT"), 0,
                        gameloop(p[n - 1], "HTH", "HTT"), gameloop(p[n - 1], "HTH", "THH"),
                        gameloop(p[n - 1], "HTH", "THT"), gameloop(p[n - 1], "HTH", "TTH"),
                        gameloop(p[n - 1], "HTH", "TTT")],
                       [gameloop(p[n - 1], "HTT", "HHH"), gameloop(p[n - 1], "HTT", "HHT"),
                        gameloop(p[n - 1], "HTT", "HTH"), 0, gameloop(p[n - 1], "HTT", "THH"),
                        gameloop(p[n - 1], "HTT", "THT"), gameloop(p[n - 1], "HTT", "TTH"),
                        gameloop(p[n - 1], "HTT", "TTT")],
                       [gameloop(p[n - 1], "THH", "HHH"), gameloop(p[n - 1], "THH", "HHT"),
                        gameloop(p[n - 1], "THH", "HTH"), gameloop(p[n - 1], "THH", "HTT"), 0,
                        gameloop(p[n - 1], "THH", "THT"), gameloop(p[n - 1], "THH", "TTH"),
                        gameloop(p[n - 1], "THH", "TTT")],
                       [gameloop(p[n - 1], "THT", "HHH"), gameloop(p[n - 1], "THT", "HHT"),
                        gameloop(p[n - 1], "THT", "HTH"), gameloop(p[n - 1], "THT", "HTT"),
                        gameloop(p[n - 1], "THT", "THH"), 0, gameloop(p[n - 1], "THT", "TTH"),
                        gameloop(p[n - 1], "THT", "TTT")],
                       [gameloop(p[n - 1], "TTH", "HHH"), gameloop(p[n - 1], "TTH", "HHT"),
                        gameloop(p[n - 1], "TTH", "HTH"), gameloop(p[n - 1], "TTH", "HTT"),
                        gameloop(p[n - 1], "TTH", "THH"), gameloop(p[n - 1], "TTH", "THT"), 0,
                        gameloop(p[n - 1], "TTH", "TTT")],
                       [gameloop(p[n - 1], "TTT", "HHH"), gameloop(p[n - 1], "TTT", "HHT"),
                        gameloop(p[n - 1], "TTT", "HTH"), gameloop(p[n - 1], "TTT", "HTT"),
                        gameloop(p[n - 1], "TTT", "THH"), gameloop(p[n - 1], "TTT", "THT"),
                        gameloop(p[n - 1], "TTT", "TTH"), 0]])
        # intransitiveness is a function of probability, and gives me the
        # unfairness of the game for each probability p to toss a T
        intransitiveness[n - 1] = np.min(np.max(V, axis=0)) - 1 / 2
        # printing values of probability that give transitiveness of the
        # game, using isclose method because of issues with equality
        # testing of no integers numbers
        if math.isclose(0, intransitiveness[n - 1], abs_tol=0.00001):
            print(p[n - 1])

    pickle.dump([p, intransitiveness], open("data.pkl", "wb"))
