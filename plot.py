import json
import matplotlib.pyplot as plt
import math


p, intransitiveness = json.load(open("data.json", "r"))
# plotting the function intransitiveness(p)
plt.plot(p, intransitiveness)
plt.xlabel("Probability")
plt.ylabel("Intransitiveness")
plt.title("Penney's Game")
for n in range(len(p)):
    if math.isclose(0, intransitiveness[n], abs_tol=0.001):
        plt.plot(p[n], intransitiveness[n], 'ro')
plt.show()
