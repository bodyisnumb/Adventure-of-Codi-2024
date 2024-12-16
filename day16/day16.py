import heapq

def read_maze(filename):
    with open(filename, 'r') as f:
        maze = [list(line.rstrip('\n')) for line in f]
    return maze

def find_positions(maze):
    start = None
    end = None
    for y, row in enumerate(maze):
        for x, c in enumerate(row):
            if c == 'S':
                start = (x, y)
            elif c == 'E':
                end = (x, y)
    return start, end

def solve_maze(maze):
    # Directions: 0=East, 1=South, 2=West, 3=North
    start, end = find_positions(maze)
    if start is None or end is None:
        raise ValueError("Maze must have S and E")

    # Movement offsets for directions
    dirs = [(1,0),(0,1),(-1,0),(0,-1)]

    def forward_pos(x, y, d):
        dx, dy = dirs[d]
        return x + dx, y + dy

    width = len(maze[0])
    height = len(maze)

    # Dijkstra
    # State: (cost, x, y, d)
    # Start facing East (d=0)
    start_state = (0, start[0], start[1], 0)
    visited = {(start[0], start[1], 0): 0}
    pq = []
    heapq.heappush(pq, start_state)

    while pq:
        cost, x, y, d = heapq.heappop(pq)
        if visited.get((x, y, d), float('inf')) < cost:
            continue
        if (x, y) == end:
            pass

        # Move forward
        fx, fy = forward_pos(x, y, d)
        if 0 <= fx < width and 0 <= fy < height and maze[fy][fx] != '#':
            fcost = cost + 1
            if fcost < visited.get((fx, fy, d), float('inf')):
                visited[(fx, fy, d)] = fcost
                heapq.heappush(pq, (fcost, fx, fy, d))

        # Turn left
        ld = (d - 1) % 4
        lcost = cost + 1000
        if lcost < visited.get((x, y, ld), float('inf')):
            visited[(x, y, ld)] = lcost
            heapq.heappush(pq, (lcost, x, y, ld))

        # Turn right
        rd = (d + 1) % 4
        rcost = cost + 1000
        if rcost < visited.get((x, y, rd), float('inf')):
            visited[(x, y, rd)] = rcost
            heapq.heappush(pq, (rcost, x, y, rd))

    # Find minimal cost to reach E in any orientation
    end_costs = [visited.get((end[0], end[1], d), float('inf')) for d in range(4)]
    min_end_cost = min(end_costs)
    if min_end_cost == float('inf'):
        # No path found
        return None, None



    # run a BFS
    queue = []
    visited_states_on_paths = set()
    # Add all end orientation states that achieve min_end_cost
    for d in range(4):
        c = visited.get((end[0], end[1], d), float('inf'))
        if c == min_end_cost:
            queue.append((end[0], end[1], d))
            visited_states_on_paths.add((end[0], end[1], d))

    while queue:
        cx, cy, cd = queue.pop()
        current_cost = visited[(cx, cy, cd)]

        # If we came forward then prev = (cx - dx, cy - dy, cd)
        dx, dy = dirs[cd]
        px, py = cx - dx, cy - dy
        if 0 <= px < width and 0 <= py < height and maze[py][px] != '#':
            pcost = visited.get((px, py, cd), float('inf'))
            if pcost + 1 == current_cost:
                if (px, py, cd) not in visited_states_on_paths:
                    visited_states_on_paths.add((px, py, cd))
                    queue.append((px, py, cd))

        # Check turn left predecessor (cx,cy,(cd+1)%4)
        ld = (cd + 1) % 4
        lcost = visited.get((cx, cy, ld), float('inf'))
        if lcost + 1000 == current_cost:
            if (cx, cy, ld) not in visited_states_on_paths:
                visited_states_on_paths.add((cx, cy, ld))
                queue.append((cx, cy, ld))

        # Check turn right predecessor (cx, cy, (cd-1)%4)
        rd = (cd - 1) % 4
        rcost = visited.get((cx, cy, rd), float('inf'))
        if rcost + 1000 == current_cost:
            if (cx, cy, rd) not in visited_states_on_paths:
                visited_states_on_paths.add((cx, cy, rd))
                queue.append((cx, cy, rd))

    path_tiles = set((x,y) for (x,y,d) in visited_states_on_paths)
    return min_end_cost, path_tiles

if __name__ == "__main__":
    maze = read_maze("data.txt")
    result, path_tiles = solve_maze(maze)
    if result is None:
        print("No path found.")
    else:
        print("Lowest score possible:", result)
        # Mark path tiles with O (except walls)
        if path_tiles is not None:
            count = 0
            for (x, y) in path_tiles:
                # Only mark if it's not a wall
                if maze[y][x] != '#':
                    maze[y][x] = 'O'
                    count += 1

            print("Number of tiles on best paths:", count)
            # Print the updated maze
            for row in maze:
                print("".join(row))