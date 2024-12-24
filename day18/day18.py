from collections import deque

def parse_input(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f]
    coords = []
    for line in lines:
        if not line:
            continue
        x_str, y_str = line.split(',')
        coords.append((int(x_str), int(y_str)))
    return coords

def build_grid(coords):
    # Memory space is 71 x 71 (indices 0..70)
    grid = [[False]*71 for _ in range(71)]
    for x, y in coords:
        grid[y][x] = True
    return grid

def bfs_min_steps(grid):
    # BFS from (0,0) to (70,70). Return min steps or None if impossible.
    # grid[r][c] == True => corrupted
    # grid[r][c] == False => safe
    n = 71  # 0..70
    start, end = (0, 0), (70, 70)
    if grid[start[0]][start[1]] or grid[end[0]][end[1]]:
        return None

    visited = [[False]*n for _ in range(n)]
    visited[start[0]][start[1]] = True
    queue = deque([(start[0], start[1], 0)])  # (row, col, dist)

    while queue:
        r, c, dist = queue.popleft()
        if (r, c) == end:
            return dist
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            rr, cc = r+dr, c+dc
            if 0 <= rr < n and 0 <= cc < n:
                if not grid[rr][cc] and not visited[rr][cc]:
                    visited[rr][cc] = True
                    queue.append((rr, cc, dist+1))
    return None

def part1(filename):
    # Read the first 1024 lines
    coords = parse_input(filename)[:1024]
    # Build a 71x71 grid, mark corrupted
    grid = build_grid(coords)
    # Find the minimum number of steps
    result = bfs_min_steps(grid)
    return result

def part2(filename):
    return None

if __name__ == "__main__":
    print(part1("data.txt"))