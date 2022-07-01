import json
import matplotlib.pyplot as plt
import math
import configparser


configu = configparser.ConfigParser()
configu.read("config.txt")
title = configu.get('settings', 'title')
title2 = configu.get('settings', 'title2')
p, intransitiveness = json.load(open("data.json", "r"))
# plotting the function intransitiveness(p)
plt.plot(p, intransitiveness)
plt.xlabel("Probability")
plt.ylabel("Intransitiveness")
plt.title(title)
for n in range(len(p)):
    if math.isclose(0, intransitiveness[n], abs_tol=0.01):
        plt.plot(p[n], intransitiveness[n], 'ro')
plt.savefig('./images/intransitiveness.png')
plt.show()

p, intransitiveness2 = json.load(open("data2.json", "r"))
plt.plot(p, intransitiveness2)
plt.xlabel("Probability")
plt.ylabel("Intransitiveness")
plt.title(title2)
for n in range(len(p)):
    if math.isclose(0, intransitiveness2[n], abs_tol=0.01):
        plt.plot(p[n], intransitiveness2[n], 'ro')
plt.savefig('./images/intransitiveness2.png')
plt.show()
