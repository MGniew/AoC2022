def sliding_window(iterable, n=4):
    for i in range(len(iterable) - n + 1):
        yield iterable[i:i+n]


def find_marker(data, n):
    for i, window in enumerate(sliding_window(data, n=n)):
        window = set(window)
        if len(window) == n:
            return i + n


def main():
    with open("input.txt") as f:
        data = f.read()

    print("Star1: ", find_marker(data, n=4))
    print("Star2: ", find_marker(data, n=14))


if __name__ == "__main__":
    main()
