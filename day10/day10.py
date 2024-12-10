def main():
    with open('data.txt', 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    grid = [list(map(int, list(row))) for row in lines] #integers

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Directions: up, down, left, right
    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    # Find all 0-cell
    zero_positions = [(r,c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]

    def neighbors(r, c):
        for dr, dc in directions:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols:
                yield nr, nc

    total_score = 0

    for zr, zc in zero_positions:
        visited = set()
        endpoints = set()

        #(row, col, height)
        stack = [(zr, zc, 0)]
        visited.add((zr, zc, 0))

        while stack:
            r, c, h = stack.pop()

            if h == 9:
                # reached a cell of height 9
                endpoints.add((r, c))
                continue

            # Look for neighbors with height h+1
            for nr, nc in neighbors(r, c):
                if grid[nr][nc] == h + 1:
                    state = (nr, nc, h+1)
                    if state not in visited:
                        visited.add(state)
                        stack.append(state)

        # Add the number of distinct 9 endpoints for this trailhead to total score
        total_score += len(endpoints)

    print(total_score)

if __name__ == '__main__':
    main()