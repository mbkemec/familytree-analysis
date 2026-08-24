from collections import Counter

ind_file = "../reference/aadr/v66.p1_compatibility_HO.aadr.patch.PUB.ind"

groups = Counter()

with open(ind_file) as f:
    for line in f:
        parts = line.split()

        sample = parts[0]
        group = parts[2]

        if sample.endswith(".HO"):
            groups[group] += 1

print("Human Origins populations")
print()

for group, count in groups.most_common():
    print(group, count)
