import pickle
import matplotlib.pyplot as plt
import math


p, intransitiveness = pickle.load(open("data.pkl", "rb"))
# plotting the function intransitiveness(p)
plt.plot(p, intransitiveness)
plt.xlabel("Probability")
plt.ylabel("Intransitiveness")
plt.title("Penney's Game")
for n in range(len(p)):
    if math.isclose(0, intransitiveness[n], abs_tol=0.001):
        plt.plot(p[n], intransitiveness[n], 'ro')
plt.show()
