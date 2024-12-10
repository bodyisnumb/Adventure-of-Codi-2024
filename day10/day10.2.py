def main():
    with open("data.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    grid = [list(map(int, list(row))) for row in lines] #integers

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Directions: up, down, left, right
    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    # Find all 0-cell
    zero_positions = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]

    # dp[r][c] will hold the number of distinct trails from (r,c) to any cell of height 9.
    dp = [[-1] * cols for _ in range(rows)]

    def count_paths(r, c):
        # If dp is already computed, return it
        if dp[r][c] != -1:
            return dp[r][c]

        current_height = grid[r][c]
        # If current cell is height 9 there is exactly one trail
        if current_height == 9:
            dp[r][c] = 1
            return 1

        total_paths = 0
        # Look for neighbors with height h+1
        next_height = current_height + 1
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == next_height:
                    total_paths += count_paths(nr, nc)

        dp[r][c] = total_paths
        return total_paths

    # Compute the sum of Ratings for all trailheads
    total_rating = 0
    for zr, zc in zero_positions:
        total_rating += count_paths(zr, zc)

    print(total_rating)

if __name__ == "__main__":
    main()