from PIL import Image
import os

def read_input(filename):
    robots = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            # Format: p=x,y v=dx,dy
            p_part = parts[0][2:]  # remove 'p='
            v_part = parts[1][2:]  # remove 'v='

            x_str, y_str = p_part.split(',')
            dx_str, dy_str = v_part.split(',')
            x, y = int(x_str), int(y_str)
            dx, dy = int(dx_str), int(dy_str)

            robots.append((x, y, dx, dy))
    return robots

def solve_part1(robots):
    width = 101
    height = 103
    mid_x = 50
    mid_y = 51
    time_to_simulate = 100

    # Simulate 100 seconds with wrapping
    final_positions = []
    for (x, y, dx, dy) in robots:
        new_x = (x + dx * time_to_simulate) % width
        new_y = (y + dy * time_to_simulate) % height
        final_positions.append((new_x, new_y))

    # Count how many end up in each quadrant
    q1 = q2 = q3 = q4 = 0
    for (x, y) in final_positions:
        # Exclude if on the middle lines
        if x == mid_x or y == mid_y:
            continue

        if x < mid_x and y < mid_y:
            q1 += 1
        elif x > mid_x and y < mid_y:
            q2 += 1
        elif x < mid_x and y > mid_y:
            q3 += 1
        elif x > mid_x and y > mid_y:
            q4 += 1

    safety_factor = q1 * q2 * q3 * q4
    print("Part 1 Safety Factor:", safety_factor)


def save_positions_as_image(positions, width, height, t):
    img = Image.new("L", (width, height), 255)  # white background
    pixels = img.load()

    # Count how many robots per tile
    grid_counts = [[0 for _ in range(width)] for _ in range(height)]
    for (x, y) in positions:
        grid_counts[y][x] += 1

    for y in range(height):
        for x in range(width):
            c = grid_counts[y][x]
            if c > 0:
                # If at least one robot is here, make it black
                pixels[x, y] = 0  # black
            # else remains white (255)

    # Save the image
    if not os.path.exists("frames"):
        os.makedirs("frames")
    img.save(f"frames/frame_{t:04d}.png")


def solve_part2(robots):
    width = 101
    height = 103
    positions = [(x, y) for (x, y, dx, dy) in robots]
    velocities = [(dx, dy) for (x, y, dx, dy) in robots]

    max_time = 7000  # Adjust as needed

    for t in range(max_time):
        # Save the current state as an image
        save_positions_as_image(positions, width, height, t)

        # Move robots one step with wrapping
        positions = [((p[0] + v[0]) % width, (p[1] + v[1]) % height)
                     for p, v in zip(positions, velocities)]

def main():
    robots = read_input("data.txt")
    solve_part1(robots)
    solve_part2(robots)

if __name__ == "__main__":
    main()