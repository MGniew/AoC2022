with open("input") as f:
    data = f.read()

elfs = [
    sum([int(f) for f in e.split("\n")]) 
    for e in data.strip().split("\n\n")
]

print("Star1:", max(elfs))
print("Star2:", sum(sorted(elfs)[-3:]))
