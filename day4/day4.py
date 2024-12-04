def load_grid(filename):
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        max_len = max(len(line) for line in lines)
        return [list(line.ljust(max_len)) for line in lines]


def search_word(grid, word):
    directions = [
        (-1, 0), (1, 0),  # Vertical (up, down)
        (0, -1), (0, 1),  # Horizontal (left, right)
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonals
    ]
    word_length = len(word)
    rows, cols = len(grid), len(grid[0])
    found_positions = []
    count = 0

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols

    def check_word(start_x, start_y, dx, dy, reverse=False):
        positions = []
        for i in range(word_length):
            x = start_x + dx * i
            y = start_y + dy * i
            if not is_valid(x, y):
                return []
            target_char = word[::-1][i] if reverse else word[i]
            if grid[x][y] != target_char:
                return []
            positions.append((x, y))
        return positions

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == word[0]:
                for dx, dy in directions:

                    positions = check_word(row, col, dx, dy)
                    if positions:
                        found_positions.append(positions)
                        count += 1

                    positions_reverse = check_word(row, col, dx, dy, reverse=True)
                    if positions_reverse:
                        found_positions.append(positions_reverse)
                        count += 1

    return found_positions, count


def main():
    grid = load_grid("data.txt")
    word = "XMAS"
    results, count = search_word(grid, word)

    if results:
        print(f"Found '{word}' {count} time(s):")
        for positions in results:
            print(positions)
    else:
        print(f"'{word}' not found in the grid.")


if __name__ == "__main__":
    main()