from collections import namedtuple


Elf = namedtuple("Elf", "start stop")


def is_overlap(elf_1, elf_2):
    if elf_1.stop < elf_2.start:
        return False
    if elf_2.stop < elf_1.start:
        return False
    return True


def is_fully_contains(elf_1, elf_2):
    if elf_1.start >= elf_2.start:
        if elf_1.stop <= elf_2.stop:
            return True
    if elf_2.start >= elf_1.start:
        if elf_2.stop <= elf_1.stop:
            return True
    return False


with open("input.txt") as f:
    data = [
        [
            Elf(
                *[int(job) for job in  elf.split("-")]
            ) 
            for elf in d.split(",")
        ] 
        for d in f.read().splitlines()
    ]

print("Star 1:", sum(is_fully_contains(a, b) for a, b in data))
print("Star 2:", sum(is_overlap(a, b) for a, b in data))
