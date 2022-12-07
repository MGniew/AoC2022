from collections import namedtuple


Execution = namedtuple("Execution", ("cmd", "args", "stdout"))


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


fs = {"/": dict()}
pwd = "/"

executions = load_data()
for e in executions:
    
    if read_output:


    line = line[:2]
    if line == "ls":
        read_output = True





