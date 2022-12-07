from collections import namedtuple, defaultdict


Execution = namedtuple("Execution", ("cmd", "args", "stdout"))


def subpath_generator(path):
    spaths = path.split("/")
    result = ""
    for p in [s + "/" for s in spaths]:
        result = result + p 
        yield result


def load_data(filename="input.txt"):
    with open(filename) as f:
        data = f.read().strip().split("$")
        result = list()
        for line in [d for d in data if d]:
            line = line.strip().split("\n")
            cmd_args = line[0].split()
            cmd = cmd_args[0]
            args = cmd_args[1:]
            stdout = line[1:]
            result.append(
                Execution(cmd, args, stdout)
            )
    return result


def cd(cwd, arg):
    if arg == "/":
        cwd = arg
    elif arg == "..":
        cwd = "/".join(cwd.split("/")[:-1])
        if not cwd:
            cwd = "/"
    else:
        if cwd == "/":
            cwd = f"/{arg}"
        else:
            cwd = f"{cwd}/{arg}"
    return cwd


fs = {"/": dict()}
cwd = "/"
executions = load_data()
for e in executions:

    if e.cmd == "cd":
        cwd = cd(cwd, e.args[0])
        if cwd not in fs:
            fs[cwd] = dict()

    elif e.cmd == "ls":
        for f in e.stdout:
            if f.startswith("dir"):
                continue
            size, fn = f.split()
            size = int(size)
            fs[cwd][fn] = size
    

total = defaultdict(int)
for k, v in fs.items():
    partial = sum([fsize for fsize in v.values()])
    for parent in subpath_generator(k):
        total[parent] += partial

result = sum([v for v in total.values() if v <= 100_000])
print("Star 1:", result)


total_disk = 70_000_000
needed = 30_000_000
disk_space = total_disk - total["/"]
to_be_deleted = needed - disk_space
sorted_directories = sorted(list(total.items()), key=lambda x: x[1])
size = 0
while size < to_be_deleted:
    size = sorted_directories.pop(0)[1]

print("Star 2:", size)
