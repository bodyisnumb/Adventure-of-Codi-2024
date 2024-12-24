def parse_input(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f]
    patterns_line = lines[0]
    patterns = [p.strip() for p in patterns_line.split(',') if p.strip()]
    designs = []
    i = 1
    while i < len(lines) and lines[i] == '':
        i += 1
    while i < len(lines):
        if lines[i]:
            designs.append(lines[i])
        i += 1
    return patterns, designs


def can_display(design, patterns):
    n = len(design)
    dp = [False] * (n + 1)
    dp[0] = True  # empty design is trivially coverable

    for i in range(1, n + 1):
        for pat in patterns:
            plen = len(pat)
            if i - plen >= 0 and dp[i - plen]:
                if design[i - plen:i] == pat:
                    dp[i] = True
                    break
    return dp[n]


def part1(filename):
    patterns, designs = parse_input(filename)
    count = 0
    for d in designs:
        if can_display(d, patterns):
            count += 1
    return count


def part2(filename):
    return None


if __name__ == "__main__":
    print(part1("data.txt"))