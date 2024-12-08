def read_grid(file_path):
    with open(file_path, 'r') as file:
        return [list(line.strip()) for line in file.readlines()]

def get_antenna_positions(grid):
    antennas = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != '.' and cell != '#':
                antennas.append((x, y, cell))
    return antennas

def calculate_antinode(pos1, pos2):
    x1, y1, _ = pos1
    x2, y2, _ = pos2
    return (x1 + (x1 - x2), y1 + (y1 - y2))

def is_within_bounds(pos, grid):
    x, y = pos
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])

def mark_antinodes(grid, antennas):
    antinodes = set()

    for i in range(len(antennas)):
        for j in range(i + 1, len(antennas)):
            pos1, pos2 = antennas[i], antennas[j]
            if pos1[2] == pos2[2]:  # Only antinodes of antennas the same symbol
                antinode = calculate_antinode(pos1, pos2)
                if is_within_bounds(antinode, grid):
                    antinodes.add(antinode)

                antinode = calculate_antinode(pos2, pos1)
                if is_within_bounds(antinode, grid):
                    antinodes.add(antinode)

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
