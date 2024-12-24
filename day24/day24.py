from collections import deque, defaultdict

def parse_input(filename):
    wires = {}
    gates = []
    with open(filename) as f:
        lines = [l.rstrip('\n') for l in f]
    idx = 0
    while idx < len(lines) and lines[idx].strip():
        name, val = lines[idx].split(':')
        wires[name.strip()] = int(val.strip())
        idx += 1
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    while idx < len(lines):
        parts = lines[idx].split()
        if '->' in parts:
            a, op, b, _, out = parts
            gates.append((a, op, b, out))
        idx += 1
    return wires, gates

def solve(filename):
    wires, gates = parse_input(filename)
    dep = defaultdict(list)
    in_count = {}
    info = {}
    for a, op, b, out in gates:
        in_count[out] = 2
        info[out] = (a, op, b)
        dep[a].append(out)
        dep[b].append(out)
    q = deque()
    for w in wires:
        for nxt in dep[w]:
            if nxt not in in_count:
                in_count[nxt] = 2
    for w in wires:
        q.append(w)
    while q:
        w = q.popleft()
        if w not in dep:
            continue
        for nxt in dep[w]:
            if nxt not in wires:
                a, op, b = info[nxt]
                in_count[nxt] -= 1
                if in_count[nxt] == 0:
                    va = wires[a] if a in wires else 0
                    vb = wires[b] if b in wires else 0
                    if op == 'AND':
                        wires[nxt] = 1 if (va == 1 and vb == 1) else 0
                    elif op == 'OR':
                        wires[nxt] = 1 if (va == 1 or vb == 1) else 0
                    else:
                        wires[nxt] = 1 if (va != vb) else 0
                    q.append(nxt)
    z_wires = []
    for k in wires:
        if k.startswith('z'):
            z_wires.append(k)
    def num_index(k):
        return int(k[1:])
    z_wires.sort(key=num_index)
    bin_str = ''.join(str(wires[w]) for w in reversed(z_wires))
    return int(bin_str, 2) if bin_str else 0

def part1(filename):
    return solve(filename)

def part2(filename):
    return None

if __name__ == "__main__":
    print(part1("data.txt"))