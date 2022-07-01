import json
import matplotlib.pyplot as plt
import math
import configparser


configu = configparser.ConfigParser()
configu.read("config.txt")
title = configu.get('settings', 'title')
p, intransitiveness = json.load(open("data.json", "r"))
# plotting the function intransitiveness(p)
plt.plot(p, intransitiveness)
plt.xlabel("Probability")
plt.ylabel("Intransitiveness")
plt.title(title)
for n in range(len(p)):
    if math.isclose(0, intransitiveness[n], abs_tol=0.001):
        plt.plot(p[n], intransitiveness[n], 'ro')
plt.savefig('./images/intransitiveness.png')
plt.show()

