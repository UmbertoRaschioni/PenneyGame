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
    tests = 1000
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
    p = np.arange(0.1, 0.9, 0.001)
    intransitiveness = np.zeros_like(p)
    # V is the victory matrix, each element of the matrix is the result of a
    # gameloop between two sequences, the for loop repeat everything for
    # different values of probability
    for n in tqdm.tqdm(range(len(p))):
        V = np.matrix([[0, gameloop(p[n], "HHH", "HHT"), gameloop(p[n], "HHH", "HTH"),
                        gameloop(p[n], "HHH", "HTT"), gameloop(p[n], "HHH", "THH"),
                        gameloop(p[n], "HHH", "THT"), gameloop(p[n], "HHH", "TTH"),
                        gameloop(p[n], "HHH", "TTT")],
                       [gameloop(p[n], "HHT", "HHH"), 0, gameloop(p[n], "HHT", "HTH"),
                        gameloop(p[n], "HHT", "HTT"), gameloop(p[n], "HHT", "THH"),
                        gameloop(p[n], "HHT", "THT"), gameloop(p[n], "HHT", "TTH"),
                        gameloop(p[n], "HHT", "TTT")],
                       [gameloop(p[n], "HTH", "HHH"), gameloop(p[n], "HTH", "HHT"), 0,
                        gameloop(p[n], "HTH", "HTT"), gameloop(p[n], "HTH", "THH"),
                        gameloop(p[n], "HTH", "THT"), gameloop(p[n], "HTH", "TTH"),
                        gameloop(p[n], "HTH", "TTT")],
                       [gameloop(p[n], "HTT", "HHH"), gameloop(p[n], "HTT", "HHT"),
                        gameloop(p[n], "HTT", "HTH"), 0, gameloop(p[n], "HTT", "THH"),
                        gameloop(p[n], "HTT", "THT"), gameloop(p[n], "HTT", "TTH"),
                        gameloop(p[n], "HTT", "TTT")],
                       [gameloop(p[n], "THH", "HHH"), gameloop(p[n], "THH", "HHT"),
                        gameloop(p[n], "THH", "HTH"), gameloop(p[n], "THH", "HTT"), 0,
                        gameloop(p[n], "THH", "THT"), gameloop(p[n], "THH", "TTH"),
                        gameloop(p[n], "THH", "TTT")],
                       [gameloop(p[n], "THT", "HHH"), gameloop(p[n], "THT", "HHT"),
                        gameloop(p[n], "THT", "HTH"), gameloop(p[n], "THT", "HTT"),
                        gameloop(p[n], "THT", "THH"), 0, gameloop(p[n], "THT", "TTH"),
                        gameloop(p[n], "THT", "TTT")],
                       [gameloop(p[n], "TTH", "HHH"), gameloop(p[n], "TTH", "HHT"),
                        gameloop(p[n], "TTH", "HTH"), gameloop(p[n], "TTH", "HTT"),
                        gameloop(p[n], "TTH", "THH"), gameloop(p[n], "TTH", "THT"), 0,
                        gameloop(p[n], "TTH", "TTT")],
                       [gameloop(p[n], "TTT", "HHH"), gameloop(p[n], "TTT", "HHT"),
                        gameloop(p[n], "TTT", "HTH"), gameloop(p[n], "TTT", "HTT"),
                        gameloop(p[n], "TTT", "THH"), gameloop(p[n], "TTT", "THT"),
                        gameloop(p[n], "TTT", "TTH"), 0]])
        # intransitiveness is a function of probability, and gives me the
        # unfairness of the game for each probability p to toss a T
        intransitiveness[n] = np.min(np.max(V, axis=0)) - 1 / 2
        # printing values of probability that give transitiveness of the
        # game, using isclose method because of issues with equality
        # testing of no integers numbers
        if math.isclose(0, intransitiveness[n], abs_tol=0.00001):
            print(p[n])

    pickle.dump([p, intransitiveness], open("data.pkl", "wb"))
