from collections import deque, defaultdict

def parse_input(filename):
    lines = []
    with open(filename) as f:
        for line in f:
            line_str = line.rstrip('\n')
            if line_str:
                lines.append(line_str)
    grid = [list(row) for row in lines]
    h, w = len(grid), len(grid[0])

    start = None
    end = None

    for r in range(h):
        for c in range(w):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'E':
                end = (r, c)
    return grid, h, w, start, end

def bfs_normal(grid, h, w, start):
    """
    Standard BFS that respects walls (#).
    Returns an array dist[] of the same size as grid,
    where dist[r][c] = the fewest steps from start to (r,c).
    If (r,c) is unreachable, dist[r][c] = None.
    """
    dist = [[None]*w for _ in range(h)]
    (sr, sc) = start
    dist[sr][sc] = 0
    queue = deque([ (sr, sc) ])

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            rr, cc = r+dr, c+dc
            if 0 <= rr < h and 0 <= cc < w:
                if grid[rr][cc] != '#' and dist[rr][cc] is None:
                    dist[rr][cc] = dist[r][c] + 1
                    queue.append((rr, cc))
    return dist

def neighbors_up_to_2_ignoring_walls(grid, h, w, r, c):
    result = []
    visited = [[False]*w for _ in range(h)]
    # BFS in a small local sense (up to 2 steps)
    # (row, col, distSoFar)
    queue = deque([(r, c, 0)])
    visited[r][c] = True

    while queue:
        rr, cc, d = queue.popleft()
        if d > 0 and grid[rr][cc] != '#':
            # We have moved at least 1 step and this cell is track => valid "end" of cheat
            result.append(((rr, cc), d))
        if d < 2:
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = rr + dr, cc + dc
                if 0 <= nr < h and 0 <= nc < w:
                    # We can pass through walls ignoring collisions
                    if not visited[nr][nc]:
                        visited[nr][nc] = True
                        queue.append((nr, nc, d+1))
    return result

def part1(filename):
    grid, h, w, start, end = parse_input(filename)

    # 2) BFS from S
    distS = bfs_normal(grid, h, w, start)
    # 3) BFS from E
    distE = bfs_normal(grid, h, w, end)

    # If E was unreachable normally, saving is never > 0
    if distS[end[0]][end[1]] is None:
        return 0

    normalDist = distS[end[0]][end[1]]

    count_cheats_ge_100 = 0

    # keep a "visitedCheat" set to avoid counting duplicates
    visitedCheats = set()

    for r in range(h):
        for c in range(w):
            if distS[r][c] is None:
                continue
            # c1 is (r,c)
            # If c1 is on the normal path, find c2 thats up to 2 ignoring walls
            possible_ends = neighbors_up_to_2_ignoring_walls(grid, h, w, r, c)
            dist_to_c1 = distS[r][c]
            for (c2, cost_ignore) in possible_ends:
                # c2 is a track cell
                r2, c2_ = c2
                if distE[r2][c2_] is None:
                    continue
                # total cheated distance
                cheatedDist = dist_to_c1 + cost_ignore + distE[r2][c2_]
                saving = normalDist - cheatedDist
                if saving >= 100:
                    # Check if we counted this cheat before
                    # (we treat it as an ordered tuple of (startCheatCell, endCheatCell, cost_ignore))
                    cheat_key = ((r,c),(r2,c2_), cost_ignore)
                    if cheat_key not in visitedCheats:
                        visitedCheats.add(cheat_key)
                        count_cheats_ge_100 += 1

    return count_cheats_ge_100

def part2(filename):
    return None

if __name__ == "__main__":
    print(part1("data.txt"))