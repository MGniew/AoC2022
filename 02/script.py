with open("input") as f:
    data = f.readlines()
data = [d.strip().split(" ") for d in data]
data = [(ord(a) - 64, ord(b) - 87) for a, b in data]

total = 0
for a, b in data:
    total += b
    if a == b:  # tie
        total += 3
    elif b == (a % 3) + 1: # win
        total += 6

print("Star1:", total)

total = 0
for a, b in data:
    if b == 1:
        total += ((a + 1) % 3) + 1
    elif b == 2:
        total += a + 3
    else:
        total += (a % 3) + 7

print("Star2:", total)
