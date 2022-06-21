import numpy as np
import random
import math
import json
import tqdm


def check_sequence(s, sequence):
    """
    Check if s in sequence
    :param s: sequence chosen by p1 or p2
    :param sequence: sequence of coin tosses
    :return: True if s in sequence
    """
    return s in sequence[-3:]


def check_victory(s1, s2, sequence):
    """
    Check if someone won
    :param s1: sequence of p1
    :param s2: sequence of p2
    :param sequence: sequence of coin tosses
    :return: 0 if p1 won, 1 if p2 won, -1 if no one won
    """
    if check_sequence(s1, sequence):
        return 0
    if check_sequence(s2, sequence):
        return 1
    return -1


def gamemove(probability, s1, s2, sequence):
    """
    Appending a new toss to the sequence
    :param probability: probability to toss T
    :param s1: sequence of p1
    :param s2: sequence of p2
    :param sequence: sequence of coin tosses
    :return: sequence with a new toss and 0 if p1 won, 2 if p2 won, -1 if no one won
    """
    sequence += random.choices("HT", weights=[1 - probability, probability], k=1)[0]
    ret = check_victory(s1, s2, sequence)
    return sequence, ret


def gameloop(probability, s1, s2):
    """
    Playing a game multiple times
    :param probability: probability to toss T
    :param s1: sequence of p1
    :param s2: sequence of p2
    :return: p1 win ratio
    """
    # setting initial p1 wins to 0
    p1w = 0
    # number of tests can be increased for major statistical relevance
    tests = 10
    for number in range(tests):
        # setting initial sequence empty
        sequence = ""
        # while True cicle ensure that game won't stop until a player wins
        while True:
            sequence, ret = gamemove(probability, s1, s2, sequence)
            if ret == 0:
                p1w += 1
            if ret >= 0:
                break
    # p1w / tests represents a win ratio (probability to win)
    return p1w / tests


if __name__ == "__main__":
    """
    playing all possible games with different probabilities to toss T
    """
    # p represents probability to toss T, values under 0.1 and over 0.9 have being exluded because simulation would
    # have been too long and those results are not interesting
    p = np.arange(0.1, 0.9, 0.001)
    intransitiveness = np.zeros_like(p)
    # each iteration of the cycle is with a different probability to toss T
    for n in tqdm.tqdm(range(len(p))):
        # V represents the victory matrix with all possible games
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
        intransitiveness[n] = np.min(np.max(V, axis=0)) - 1 / 2
        # values of probability that give 0 intransitiveness are particularly interesting so I will print them
        if math.isclose(0, intransitiveness[n], abs_tol=0.01):
            print(p[n])

    json.dump([p.tolist(), intransitiveness.tolist()], open("data.json", "w"))
