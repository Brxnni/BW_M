from itertools import permutations
from collections import Counter
import matplotlib.pyplot as plt

spaces = list(range(1, 10))
distances = []
perms = list(permutations(spaces))

for perm in perms:
	distance = sum([abs(perm[i+1]-perm[i]) for i in range(len(perm)-1)])
	distance += perm[0] + perm[-1]

	distances.append((perm, distance))

# Alle möglichen Werte für d
# abysmal dogshit code, python ist nicht perfekt
print("d in:", ", ".join(list(map(str, sorted(set([ d[1] for d in distances ]))))))
# Alle Kombinationen für d=20
twenties = [ d for d in distances if d[1] == 20 ]
print("d=20 für:", ", ".join(map(str, twenties[0][0])))
# for t in twenties: print(t)

distance_distribution = Counter([ d[1] for d in distances ])

# d-#-Diagramm
plt.bar(distance_distribution.keys(), distance_distribution.values())
plt.xlabel("Gesamtstrecke")
plt.ylabel("# Permutationen")
plt.show()
