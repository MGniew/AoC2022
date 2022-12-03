from string import ascii_letters

with open("input.txt") as f:
    data = f.read().splitlines()

priority = {l: i for i, l in enumerate(ascii_letters, 1)}
result = 0
for rucksack in data:
    comp_1 = set(rucksack[:len(rucksack)//2])
    comp_2 = set(rucksack[len(rucksack)//2:])
    result += sum(
        [priority[item] for item in comp_1 & comp_2]
    )

print("Star 1:", result)
    
result = 0
grp_i = iter(data)
for elf_1, elf_2, elf_3 in zip(grp_i, grp_i, grp_i):
    badge = set(elf_1) & set(elf_2) & set(elf_3)
    result += priority[badge.pop()]

print("Star 2:", result)
