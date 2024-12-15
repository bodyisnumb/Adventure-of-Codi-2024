def read_input(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]

    map_lines = []
    move_lines = []
    map_mode = True

    for line in lines:
        if map_mode:
            if line and all(ch in '#.@O' or ch == '.' for ch in line):
                map_lines.append(line)
            else:
                map_mode = False
                if line.strip():
                    move_lines.append(line)
        else:
            if line.strip():
                move_lines.append(line)

    return map_lines, move_lines

def parse_moves(move_lines):
    moves_str = "".join(move_lines)
    moves_str = moves_str.replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "")
    return [ch for ch in moves_str if ch in '^v<>']

def parse_map_part1(map_lines):
    grid = [list(row) for row in map_lines]
    height = len(grid)
    width = len(grid[0])
    robot_pos = None
    for y in range(height):
        for x in range(width):
            if grid[y][x] == '@':
                robot_pos = (x, y)
                break
        if robot_pos is not None:
            break
    return grid, robot_pos, width, height

def scale_map_part2(map_lines):
    char_map = {
        '#': '##',
        'O': '[]',
        '.': '..',
        '@': '@.'
    }

    original_grid = [list(row) for row in map_lines]
    height = len(original_grid)
    width = len(original_grid[0])

    scaled_grid = []
    robot_pos = None
    for y in range(height):
        new_line = []
        for x in range(width):
            tile = original_grid[y][x]
            doubled = char_map[tile]
            new_line.extend(list(doubled))
        scaled_grid.append(new_line)

    for y in range(height):
        for x in range(width):
            if scaled_grid[y][2*x] == '@' and scaled_grid[y][2*x+1] == '.':
                robot_pos = (x, y)
                break
        if robot_pos is not None:
            break

    return scaled_grid, robot_pos, width, height

def move_robot_part1(grid, robot_pos, move, width, height):
    dir_map = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}
    (rx, ry) = robot_pos
    dx, dy = dir_map[move]
    nx, ny = rx+dx, ry+dy

    if grid[ny][nx] == '#':
        return grid, (rx, ry)
    if grid[ny][nx] == '.':
        grid[ry][rx] = '.'
        grid[ny][nx] = '@'
        return grid, (nx, ny)
    if grid[ny][nx] == 'O':
        box_positions = []
        cx, cy = nx, ny
        while True:
            if grid[cy][cx] == 'O':
                box_positions.append((cx, cy))
                cx += dx
                cy += dy
            else:
                break
        if grid[cy][cx] == '.':
            for bx, by in reversed(box_positions):
                grid[by][bx] = '.'
                grid[by+dy][bx+dx] = 'O'
            grid[ry][rx] = '.'
            grid[ry+dy][rx+dx] = '@'
            return grid, (rx+dx, ry+dy)
        else:
            return grid, (rx, ry)
    return grid, (rx, ry)

def move_robot_part2(grid, robot_pos, move, width, height):
    dir_map = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}
    (rx, ry) = robot_pos
    dx, dy = dir_map[move]
    nx, ny = rx+dx, ry+dy

    def tile_is_wall(x, y):
        return grid[y][2*x] == '#' and grid[y][2*x+1] == '#'
    def tile_is_empty(x, y):
        return grid[y][2*x] == '.' and grid[y][2*x+1] == '.'
    def tile_is_box(x, y):
        return grid[y][2*x] == '[' and grid[y][2*x+1] == ']'
    def tile_is_robot(x, y):
        return grid[y][2*x] == '@' and grid[y][2*x+1] == '.'

    if tile_is_wall(nx, ny) or tile_is_robot(nx, ny):
        return grid, (rx, ry)
    if tile_is_empty(nx, ny):
        grid[ry][2*rx] = '.'
        grid[ry][2*rx+1] = '.'
        grid[ny][2*nx] = '@'
        grid[ny][2*nx+1] = '.'
        return grid, (nx, ny)
    if tile_is_box(nx, ny):
        box_positions = []
        cx, cy = nx, ny
        while True:
            if tile_is_box(cx, cy):
                box_positions.append((cx, cy))
                cx += dx
                cy += dy
            else:
                break
        if tile_is_empty(cx, cy):
            for (bx, by) in reversed(box_positions):
                grid[by][2*bx] = '.'
                grid[by][2*bx+1] = '.'
                grid[by+dy][2*(bx+dx)] = '['
                grid[by+dy][2*(bx+dx)+1] = ']'
            grid[ry][2*rx] = '.'
            grid[ry][2*rx+1] = '.'
            grid[ny][2*nx] = '@'
            grid[ny][2*nx+1] = '.'
            return grid, (nx, ny)
        else:
            return grid, (rx, ry)
    return grid, (rx, ry)

def compute_gps_sum_part1(grid, width, height):
    total = 0
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 'O':
                total += 100*y + x
    return total

def compute_gps_sum_part2(grid, width, height):
    total = 0
    for y in range(height):
        line_str = ''.join(grid[y])
        start = 0
        while True:
            idx = line_str.find('[', start)
            if idx == -1:
                break
            total += 100*y + idx
            start = idx+1
    return total

def main():
    map_lines, move_lines = read_input("data.txt")
    moves = parse_moves(move_lines)

    grid1, robot_pos1, w1, h1 = parse_map_part1(map_lines)
    for move in moves:
        grid1, robot_pos1 = move_robot_part1(grid1, robot_pos1, move, w1, h1)
    part1_result = compute_gps_sum_part1(grid1, w1, h1)

    grid2, robot_pos2, w2, h2 = scale_map_part2(map_lines)
    for move in moves:
        grid2, robot_pos2 = move_robot_part2(grid2, robot_pos2, move, w2, h2)
    part2_result = compute_gps_sum_part2(grid2, w2, h2)

    print("Part 1 Result:", part1_result)
    print("Part 2 Result:", part2_result)

if __name__ == "__main__":
    main()