import csv
from collections import Counter

l1 = []
l2 = []
distance = []
with open("d01.txt", 'r') as fi:
    csv_reader = csv.reader(fi)
    for row in csv_reader:
        l1.append(int(row[0]))
        l2.append(int(row[-1]))

l1.sort()
l2.sort()

for i in range(len(l1)):
    if l1[i] < l2[i]:
        distance.append(l2[i] - l1[i])
    else:
        distance.append(l1[i] - l2[i])

print(sum(distance))

score = []
cnt = Counter(l2)
for i in l1:
    score.append(i * cnt[i])

print(sum(score))
