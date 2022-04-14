import numpy as np
import matplotlib.pyplot as plt
import random


def gameloop(p, s1, s2):
    #setting number of victories for player 1 (P1W) and player 2 (P2W) to zero
    P1W = 0
    P2W = 0
    #setting an empty initial sequence
    sequence = [""]
    #playing the game 1000 times
    for n in range(1000):
        i=0
        CoinSides = ["H", "T"]
        while True:
    #appending a toss to the sequence until one of the 2 sequences s1 or s2 appears
            sequence += random.choices(CoinSides, weights=[1 - p, p], k=1)
    #the conditional break starts when in the sequence there are at least three tosses
            if i > 1:
                if s1 in sequence[i - 1] + sequence[i] + sequence[i + 1]:
                    P1W += 1
                    break
                if s2 in sequence[i - 1] + sequence[i] + sequence[i + 1]:
                    P2W += 1
                    break
            i+=1
    #sequence returns empty after each game
        sequence = [""]
    return P1W / 1000.0

#p represents probability to toss T, it doesn't consider probabilities under 0.1 and over 0.9 because the simulation would be too much long, and the results are not interesting in those ranges
p = np.arange(0.1, 0.9, 0.001)
intransitiveness = [0] * 800
#V is the victory matrix, each element of the matrix is the result of a gameloop between two sequences, the for loop repeat everything for different values of probability
for n in range(1, 800):
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
    intransitiveness[n - 1] = np.min(np.max(V, axis=0)) - 1 / 2

plt.plot(p, intransitiveness)
plt.xlabel("probability")
plt.ylabel("intransitiveness")
plt.show()

