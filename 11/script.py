from functools import reduce
from copy import deepcopy

class Monkey():

    def __init__(self, items, operation, test, test_result):
        self.items = items
        self.operation = operation
        self.test = test
        self.test_result = test_result
        self.no_inspects = 0

    @classmethod
    def from_string(cls, mokey_str):
        monkey = monkey_str.split("\n")
        items = [int(a) for a in monkey[1][monkey[1].find(":")+1:].split(",")]
        operation = monkey[2].split(":")[1].split("=")[1]
        test = int(monkey[3].split("by")[1])
        test_result = [
            int(monkey[4].split("monkey")[1]),
            int(monkey[5].split("monkey")[1])
        ]
        return cls(items, operation, test, test_result)

    def __str__(self):
        return (
            f"Monkey(items: {self.items}, "
            f"opertation: {self.operation}, "
            f"test: {self.test})"
            f"test_result: {self.test_result})"
        )

    def take_turn(self, stress_divisor, super_divisor):
        targets = list()
        for old in self.items:
            self.no_inspects += 1
            new = eval(self.operation)
            if stress_divisor > 1:
                new = new // stress_divisor
            else:
                new = new % super_divisor
            target_m = self.test_result[new % self.test != 0]
            targets.append((target_m, new))
        self.items = []
        return targets

    def catch(self, item):
        self.items.append(item)


def solve(monkeys, iterations, stress_divisor):
    monkeys = deepcopy(monkeys)
    super_divisor = reduce(lambda a, b: a * b, [m.test for m in monkeys])
    for rnd in range(iterations):
        for i, m in enumerate(monkeys):
            targets = m.take_turn(stress_divisor, super_divisor)
            for target_m, new in targets:
                monkeys[target_m].catch(new)
    result = sorted([m.no_inspects for m in monkeys])
    return result[-1] * result[-2]


if __name__ == "__main__":

    filename = "input.txt"
    with open(filename) as f:
        data = f.read().split("\n\n")

    monkeys = list()
    for monkey_str in data:
        m = Monkey.from_string(monkey_str)
        monkeys.append(m)

    print("Star 1:", solve(monkeys, 20, 3))
    print("Star 2:", solve(monkeys, 10_000, 1))
