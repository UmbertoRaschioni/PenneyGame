import numpy as np
import random
import math
import json
import tqdm
import configparser
from enum import Enum

config = configparser.ConfigParser()
config.read("config.txt")
i = config.getint('settings', 'n')
seed = config.getint('settings', 'seed')
tests = config.getint('settings', 'tests')
start = config.getfloat('settings', 'start')
end = config.getfloat('settings', 'end')
distance = config.getfloat('settings', 'range')


class Situation(Enum):
    p1_wins = 1
    p2_wins = 2
    nobody_won_yet = 3


def check_sequence(s, sequence, i):
    """
    Check if s in sequence
    :param s: sequence chosen by p1 or p2
    :param sequence: sequence of coin tosses
    :param i: lenght of players' sequences
    :return: True if s in sequence
    """
    return s in sequence[-i:]


def check_victory(s1, s2, sequence, i):
    """
    Check if someone won
    :param s1: sequence of p1
    :param s2: sequence of p2
    :param sequence: sequence of coin tosses
    :param i: lenght of players' sequences
    :return: 0 if p1 won, 1 if p2 won, -1 if no one won
    """
    if check_sequence(s1, sequence, i):
        return Situation.p1_wins
    if check_sequence(s2, sequence, i):
        return Situation.p2_wins
    return Situation.nobody_won_yet


def gamemove(probability, s1, s2, sequence, i):
    """
    Appending a new toss to the sequence
    :param probability: probability to toss T
    :param s1: sequence of p1
    :param s2: sequence of p2
    :param sequence: sequence of coin tosses
    :param i: lenght of players' sequences
    :return: sequence with a new toss and 0 if p1 won, 2 if p2 won, -1 if no one won
    """
    np.random.seed(seed)
    sequence += random.choices("HT", weights=[1 - probability, probability], k=1)[0]
    ret = check_victory(s1, s2, sequence, i)
    return sequence, ret


def gameloop(probability, s1, s2, i):
    """
    Playing a game multiple times
    :param probability: probability to toss T
    :param s1: sequence of p1
    :param s2: sequence of p2
    :param i: lenght of players' sequences
    :return: p1 win ratio
    """
    # setting initial p1 wins to 0
    p1w = 0
    # number of tests can be increased for major statistical relevance
    for number in range(tests):
        # setting initial sequence empty
        sequence = ""
        # while True cicle ensure that game won't stop until a player wins
        while True:
            sequence, ret = gamemove(probability, s1, s2, sequence, i)
            if ret == Situation.p1_wins:
                p1w += 1
            if ret == Situation.p2_wins:
                break
    # p1w / tests represents a win ratio (probability to win)
    return p1w / tests


def matrix():
    # v represents the victory matrix with all possible games
    v = np.matrix([[0, gameloop(p[n], "HHH", "HHT", i), gameloop(p[n], "HHH", "HTH", i),
                    gameloop(p[n], "HHH", "HTT", i), gameloop(p[n], "HHH", "THH", i),
                    gameloop(p[n], "HHH", "THT", i), gameloop(p[n], "HHH", "TTH", i),
                    gameloop(p[n], "HHH", "TTT", i)],
                   [gameloop(p[n], "HHT", "HHH", i), 0, gameloop(p[n], "HHT", "HTH", i),
                    gameloop(p[n], "HHT", "HTT", i), gameloop(p[n], "HHT", "THH", i),
                    gameloop(p[n], "HHT", "THT", i), gameloop(p[n], "HHT", "TTH", i),
                    gameloop(p[n], "HHT", "TTT", i)],
                   [gameloop(p[n], "HTH", "HHH", i), gameloop(p[n], "HTH", "HHT", i), 0,
                    gameloop(p[n], "HTH", "HTT", i), gameloop(p[n], "HTH", "THH", i),
                    gameloop(p[n], "HTH", "THT", i), gameloop(p[n], "HTH", "TTH", i),
                    gameloop(p[n], "HTH", "TTT", i)],
                   [gameloop(p[n], "HTT", "HHH", i), gameloop(p[n], "HTT", "HHT", i),
                    gameloop(p[n], "HTT", "HTH", i), 0, gameloop(p[n], "HTT", "THH", i),
                    gameloop(p[n], "HTT", "THT", i), gameloop(p[n], "HTT", "TTH", i),
                    gameloop(p[n], "HTT", "TTT", i)],
                   [gameloop(p[n], "THH", "HHH", i), gameloop(p[n], "THH", "HHT", i),
                    gameloop(p[n], "THH", "HTH", i), gameloop(p[n], "THH", "HTT", i), 0,
                    gameloop(p[n], "THH", "THT", i), gameloop(p[n], "THH", "TTH", i),
                    gameloop(p[n], "THH", "TTT", i)],
                   [gameloop(p[n], "THT", "HHH", i), gameloop(p[n], "THT", "HHT", i),
                    gameloop(p[n], "THT", "HTH", i), gameloop(p[n], "THT", "HTT", i),
                    gameloop(p[n], "THT", "THH", i), 0, gameloop(p[n], "THT", "TTH", i),
                    gameloop(p[n], "THT", "TTT", i)],
                   [gameloop(p[n], "TTH", "HHH", i), gameloop(p[n], "TTH", "HHT", i),
                    gameloop(p[n], "TTH", "HTH", i), gameloop(p[n], "TTH", "HTT", i),
                    gameloop(p[n], "TTH", "THH", i), gameloop(p[n], "TTH", "THT", i), 0,
                    gameloop(p[n], "TTH", "TTT", i)],
                   [gameloop(p[n], "TTT", "HHH", i), gameloop(p[n], "TTT", "HHT", i),
                    gameloop(p[n], "TTT", "HTH", i), gameloop(p[n], "TTT", "HTT", i),
                    gameloop(p[n], "TTT", "THH", i), gameloop(p[n], "TTT", "THT", i),
                    gameloop(p[n], "TTT", "TTH", i), 0]])
    intransitiveness[n] = np.min(np.max(v, axis=0)) - 1 / 2
    # values of probability that give 0 intransitiveness are particularly interesting so I will print them
    if math.isclose(0, intransitiveness[n], abs_tol=0.01):
        print(p[n])


if __name__ == "__main__":
    """
    playing all possible games with different probabilities to toss T
    """
    # p represents probability to toss T, values under 0.1 and over 0.9 have being exluded because simulation would
    # have been too long and those results are not interesting
    p = np.arange(start, end, distance)
    intransitiveness = np.zeros_like(p)
    # each iteration of the cycle is with a different probability to toss T
    for n in tqdm.tqdm(range(len(p))):
        matrix()

    json.dump([p.tolist(), intransitiveness.tolist()], open("data.json", "w"))
