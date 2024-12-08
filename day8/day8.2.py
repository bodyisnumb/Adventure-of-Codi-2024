from math import gcd


def read_grid(file_path):
    with open(file_path, 'r') as file:
        return [list(line.strip()) for line in file.readlines()]


def get_antenna_positions(grid):
    antennas = {}
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell not in ('.', '#'):
                if cell not in antennas:
                    antennas[cell] = []
                antennas[cell].append((x, y, cell))
    return antennas


def is_within_bounds(pos, grid):
    x, y = pos
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def line_direction(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    dx = x2 - x1
    dy = y2 - y1
    g = gcd(dx, dy)
    if g == 0:
        return None  # Same point or invalid line
    return (dx // g, dy // g)


def sort_antennas_along_line(antennas_line, dx, dy):
    ref = antennas_line[0]
    x0, y0, _ = ref
    # Sort by scalar projection along (dx, dy)
    antennas_line.sort(key=lambda p: (p[0] - x0) * dx + (p[1] - y0) * dy)
    return antennas_line


def generate_full_line_antinodes(antennas_line, grid):
    if len(antennas_line) < 2:
        # Only one antenna on this line no line-based pattern
        return set([(antennas_line[0][0], antennas_line[0][1])])

    antinodes = set()
    # Add antennas themselves as antinodes
    for ax, ay, _ in antennas_line:
        if is_within_bounds((ax, ay), grid):
            antinodes.add((ax, ay))

    # Determine direction and spacing
    x1, y1, _ = antennas_line[0]
    x2, y2, _ = antennas_line[1]
    dx = x2 - x1
    dy = y2 - y1
    g = gcd(dx, dy)
    dx //= g
    dy //= g

    x0, y0, _ = antennas_line[0]

    def param(x, y):
        return (x - x0) * dx + (y - y0) * dy  # scalar projection along direction

    params = [param(ax, ay) for ax, ay, _ in antennas_line]
    min_p = min(params)
    max_p = max(params)

    # Fill antinodes between the min and max
    for t in range(min_p, max_p + 1):
        X = x0 + t * dx
        Y = y0 + t * dy
        if is_within_bounds((X, Y), grid):
            antinodes.add((X, Y))

    # Extend beyond the min and max until we hit grid
    # Go lower
    t = min_p - 1
    while True:
        X = x0 + t * dx
        Y = y0 + t * dy
        if not is_within_bounds((X, Y), grid):
            break
        antinodes.add((X, Y))
        t -= 1

    # Go higher
    t = max_p + 1
    while True:
        X = x0 + t * dx
        Y = y0 + t * dy
        if not is_within_bounds((X, Y), grid):
            break
        antinodes.add((X, Y))
        t += 1

    return antinodes


def mark_antinodes(grid, antennas):
    antinodes = set()

    # Group antennas by symbol then find lines formed by pairs of antennas with the same symbol
    for symbol, positions in antennas.items():

        lines = {}

        n = len(positions)
        if n == 1:
            # Single antenna counts as an antinode
            x, y, _ = positions[0]
            if is_within_bounds((x, y), grid):
                antinodes.add((x, y))
            continue

        # For each pair, determine the line direction and a unique line identifier
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1, _ = positions[i]
                x2, y2, _ = positions[j]
                dx = x2 - x1
                dy = y2 - y1
                g = gcd(dx, dy)
                if g == 0:
                    continue
                dx //= g
                dy //= g
                # normalize so dx>0 or if dx=0, dy>0
                # This avoids duplicates with reversed directions
                if dx < 0 or (dx == 0 and dy < 0):
                    dx = -dx
                    dy = -dy

                # Find line offset:
                c = dy * x1 - dx * y1

                if (dx, dy, c) not in lines:
                    lines[(dx, dy, c)] = []
                # Add both points
                lines[(dx, dy, c)].append(positions[i])
                lines[(dx, dy, c)].append(positions[j])

        # process each line
        for (dx, dy, c), line_positions in lines.items():
            # Deduplicate antennas on this line
            unique_line_positions = list({(p[0], p[1], p[2]) for p in line_positions})
            if len(unique_line_positions) == 0:
                continue

            sorted_line = sort_antennas_along_line(unique_line_positions, dx, dy)
            line_antinodes = generate_full_line_antinodes(sorted_line, grid)
            antinodes.update(line_antinodes)

    for x, y in antinodes:
        if grid[y][x] == '.':
            grid[y][x] = '#'
    return len(antinodes)


def main():
    input_file = 'data.txt'

    grid = read_grid(input_file)
    antennas = get_antenna_positions(grid)
    num_antinodes = mark_antinodes(grid, antennas)

    print(f"Total distinct antinodes: {num_antinodes}")


if __name__ == "__main__":
    main()