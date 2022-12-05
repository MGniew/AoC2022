import copy


def prepare_stacks(stacks):
    new_stacks = []
    idxs = list(range(1, len(stacks[-1]), 4))
    for idx in idxs:
        new_stacks.append(list())

    for stack in stacks[:-1]:
        for stack_id, idx in enumerate(idxs):
            if stack[idx] != " ":
                new_stacks[stack_id].append(stack[idx])
    return new_stacks


def perform_op(stacks, op, reverse=True):
    to_move = op[0]
    source = op[1] - 1
    destination = op[2] - 1
    grabbed = list()
    for i in range(to_move):
        grabbed.append(stacks[source].pop(0))
    if reverse:
        grabbed.reverse()
    stacks[destination] = grabbed + stacks[destination]


def load_data(filename="input.txt"):
    with open("input.txt") as f:
        stacks = list()
        for line in f:
            if not line.strip():
                break
            stacks.append(list(line))
        stacks = prepare_stacks(stacks)

        ops = list()
        for line in f:
            ops.append(
                [int(el) for el in line.split()[1::2]]
            )

    return stacks, ops


def crate_mover_9000(stacks, ops):
    stacks = copy.deepcopy(stacks)
    for op in ops:
        perform_op(stacks, op, reverse=True)
    return "".join([s[0] for s in stacks])


def crate_mover_9001(stacks, ops):
    stacks = copy.deepcopy(stacks)
    for op in ops:
        perform_op(stacks, op, reverse=False)
    return "".join([s[0] for s in stacks])


stacks, ops = load_data()
print("Star1: ", crate_mover_9000(stacks, ops))
print("Star2: ", crate_mover_9001(stacks, ops))
