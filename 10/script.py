class CRT():

    def __init__(self, width=40, height=6, sprite_width=3):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.sprite_width = sprite_width
        self.image = [
            ["." for i in range(width)] for h in range(height)
        ]

    def draw(self, x):
        if x - 1 + self.sprite_width > self.x >= x - 1:
            self.image[self.y][self.x] = "#" 
        self.x += 1
        if self.x == self.width:
            self.y += 1
            self.x = 0

    def __str__(self):
        return "\n".join(["".join(row) for row in self.image])


def addx(*args):
    global x
    x += int(args[0])


def noop(*args):
    pass


with open("input.txt") as f:
    data = f.read().splitlines()
    data = [d.split() for d in data]
    data = [(d[0], tuple(d[1:])) for d in data]

x = 1
cycle = 1
exec_time = {
    "addx": 2,
    "noop": 1
}

cpu_states = list()
crt = CRT()
for line in data:
    cmd = line[0]
    args = line[1]
    start_cycle = cycle

    while cycle < start_cycle + exec_time[cmd]:
        cpu_states.append([cycle, x])
        crt.draw(x)
        cycle += 1

    locals()[cmd](*args)
cpu_states.append([cycle, x])
crt.draw(x)

result = ([
    cycle  * x for cycle, x in cpu_states
    if (cycle + 40) % 40 == 20
])
print("Star 1:", sum(result))
print("Star 2:", crt, sep="\n")
