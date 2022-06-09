import pickle
import matplotlib.pyplot as plt


p,intransitiveness = pickle.load(open("data.pkl", "rb"))
print(intransitiveness.shape)
print(p.shape)
# plotting the function intransitiveness(p)
plt.plot(p, intransitiveness)
plt.xlabel("probability")
plt.ylabel("intransitiveness")
plt.show()