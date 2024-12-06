import pathlib

def load_map(file_path: str) -> list[list[str]]:
    with open(file_path, 'r') as file:
        return [list(line.rstrip('\n')) for line in file]

def find_guard_start(map_data: list[list[str]]) -> tuple[int, int]:
    for yy, row in enumerate(map_data):
        for xx, cell in enumerate(row):
            if cell == '^':
                return yy, xx
    raise ValueError("No guard on map")

def turn_right(direction: tuple[int, int]) -> tuple[int, int]:
    return {
        (-1, 0): (0, 1),   # Up -> Right
        (0, 1): (1, 0),    # Right -> Down
        (1, 0): (0, -1),   # Down -> Left
        (0, -1): (-1, 0)   # Left -> Up
    }[direction]

def is_within_bounds(map_data: list[list[str]], y: int, x: int) -> bool:
    return 0 <= y < len(map_data) and 0 <= x < len(map_data[0])

def simulate_guard_route(map_data):
    start_y, start_x = find_guard_start(map_data)
    direction = (-1, 0)  # up
    y, x = start_y, start_x
    visited_positions = []
    visited_states = set()

    while True:
        if (y, x, direction) in visited_states:
            break
        visited_states.add((y, x, direction))
        visited_positions.append((y, x))

        next_y, next_x = y + direction[0], x + direction[1]
        if not is_within_bounds(map_data, next_y, next_x):
            # Guard leaves map
            break

        if map_data[next_y][next_x] == '#':
            direction = turn_right(direction)
        else:
            # Move forward
            y, x = next_y, next_x

    return visited_positions

def simulate_with_obstacle(map_data):
    start_y, start_x = find_guard_start(map_data)
    direction = (-1, 0)  # up
    y, x = start_y, start_x
    visited_states = set()

    while True:
        if (y, x, direction) in visited_states:
            # Loop detected
            return True
        visited_states.add((y, x, direction))

        next_y, next_x = y + direction[0], x + direction[1]
        if not is_within_bounds(map_data, next_y, next_x):
            # Leaves the map
            return False

        if map_data[next_y][next_x] == '#':
            direction = turn_right(direction)
        else:
            y, x = next_y, next_x

def main():
    file_path = "data.txt"
    if not pathlib.Path(file_path).exists():
        print(f"File '{file_path}' not found.")
        return

    map_data = load_map(file_path)

    route = simulate_guard_route(map_data)

    # Consider only distinct '.' cells visited by guard
    # skip cells that are starting position '^' or obstacles
    # Focus on '.'
    candidate_positions = set()
    for (yy, xx) in route:
        if map_data[yy][xx] == '.':
            candidate_positions.add((yy, xx))

    count = 0
    for (oy, ox) in candidate_positions:
        # Place obstacle at (oy, ox)
        modified_map = [row[:] for row in map_data]
        modified_map[oy][ox] = '#'

        # Check if loop occurs with this one obstacle added
        if simulate_with_obstacle(modified_map):
            count += 1

    print(f"Total number of obstacles that can make the guard loop: {count}")

if __name__ == "__main__":
    main()