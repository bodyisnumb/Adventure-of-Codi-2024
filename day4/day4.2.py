def load_grid(filename):
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        return [list(line) for line in lines]


def search_x_mas(grid):
    rows, cols = len(grid), len(grid[0])
    found_positions = []
    count = 0

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols

    def check_3x3(x, y):
        if not (is_valid(x, y) and is_valid(x + 2, y + 2)):
            return []

        subgrid = [
            [grid[x][y], grid[x][y + 1], grid[x][y + 2]],
            [grid[x + 1][y], grid[x + 1][y + 1], grid[x + 1][y + 2]],
            [grid[x + 2][y], grid[x + 2][y + 1], grid[x + 2][y + 2]],
        ]

        if subgrid[0][0] == "M" and subgrid[0][2] == "M" and subgrid[1][1] == "A" and subgrid[2][0] == "S" and \
                subgrid[2][2] == "S":
            return [(x, y), (x, y + 2), (x + 1, y + 1), (x + 2, y), (x + 2, y + 2)]  # M.M
        if subgrid[0][0] == "S" and subgrid[0][2] == "S" and subgrid[1][1] == "A" and subgrid[2][0] == "M" and \
                subgrid[2][2] == "M":
            return [(x, y), (x, y + 2), (x + 1, y + 1), (x + 2, y), (x + 2, y + 2)]  # S.S
        if subgrid[0][0] == "M" and subgrid[0][2] == "S" and subgrid[2][0] == "M" and subgrid[2][2] == "S" and \
                subgrid[1][1] == "A":
            return [(x, y), (x, y + 2), (x + 1, y + 1), (x + 2, y), (x + 2, y + 2)]  # M.S
        if subgrid[0][0] == "S" and subgrid[0][2] == "M" and subgrid[2][0] == "S" and subgrid[2][2] == "M" and \
                subgrid[1][1] == "A":
            return [(x, y), (x, y + 2), (x + 1, y + 1), (x + 2, y), (x + 2, y + 2)]  # S.M

        return []

    for row in range(rows - 2):
        for col in range(cols - 2):
            positions = check_3x3(row, col)
            if positions:
                found_positions.append(positions)
                count += 1

    return found_positions, count


def main():
    grid = load_grid("data.txt")

    results, count = search_x_mas(grid)

    if results:
        print(f"Found 'X-MAS' {count} time(s):")
        for positions in results:
            print(positions)
    else:
        print("'X-MAS' not found in the grid")


if __name__ == "__main__":
    main()