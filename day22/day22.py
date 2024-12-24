def parse_input(filename):
    return [int(line.strip()) for line in open(filename) if line.strip()]

def next_secret(x):
    x ^= (x * 64)
    x %= 16777216
    x ^= (x // 32)
    x %= 16777216
    x ^= (x * 2048)
    x %= 16777216
    return x

def get_2000th_secret(initial):
    x = initial
    for _ in range(2000):
        x = next_secret(x)
    return x

def part1(filename):
    buyers = parse_input(filename)
    return sum(get_2000th_secret(b) for b in buyers)

def part2(filename):
    return None

if __name__ == "__main__":
    print(part1("data.txt"))