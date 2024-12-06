import tkinter as tk
import pathlib
import time

CELL_SIZE = 5  # Size of each cell in pixels

def load_map(file_path: str) -> list[list[str]]:
    with open(file_path, 'r') as file:
        return [list(line.rstrip()) for line in file]

def find_guard_start(map_data: list[list[str]]) -> tuple[int, int]:
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == '^':
                return y, x
    raise ValueError("No guard in the map.")

def turn_right(direction: tuple[int, int]) -> tuple[int, int]:
    return {(-1, 0): (0, 1),  # Up -> Right
            (0, 1): (1, 0),   # Right -> Down
            (1, 0): (0, -1),  # Down -> Left
            (0, -1): (-1, 0)}[direction]  # Left -> Up

def is_within_bounds(map_data: list[list[str]], y: int, x: int) -> bool:
    return 0 <= y < len(map_data) and 0 <= x < len(map_data[0])

def draw_map(canvas, map_data, guard_pos, direction, cell_size):
    canvas.delete("all")  # Clear the canvas
    rows, cols = len(map_data), len(map_data[0])

    # Draw each cell
    for y in range(rows):
        for x in range(cols):
            color = "white" if map_data[y][x] == '.' else "black"
            if map_data[y][x] == '#':
                color = "gray"
            elif map_data[y][x] == '*':
                color = "yellow"
            elif map_data[y][x] == 'X':
                color = "red"
            canvas.create_rectangle(
                x * cell_size, y * cell_size,
                (x + 1) * cell_size, (y + 1) * cell_size,
                fill=color, outline="lightgray"
            )

    # Draw the guard
    guard_color = "blue"
    direction_symbol = {(-1, 0): '^', (0, 1): '>', (1, 0): 'v', (0, -1): '<'}[direction]
    gx, gy = guard_pos
    canvas.create_text(
        gx * cell_size + cell_size // 2,
        gy * cell_size + cell_size // 2,
        text=direction_symbol,
        fill=guard_color,
        font=("Helvetica", int(cell_size * 0.7), "bold")
    )

def center_view_on_guard(canvas, guard_pos, cell_size, canvas_width, canvas_height):
    x, y = guard_pos
    canvas.xview_moveto(max(0, x * cell_size - canvas_width // 2) / canvas.bbox("all")[2])
    canvas.yview_moveto(max(0, y * cell_size - canvas_height // 2) / canvas.bbox("all")[3])

def simulate_guard(map_data, canvas, canvas_width, canvas_height):
    y, x = find_guard_start(map_data)
    direction = (-1, 0)  # Initial direction (up)
    visited_cells = set()  # To track distinct cells visited by the guard
    visited_cells.add((y, x))  # Add the starting position

    while True:
        draw_map(canvas, map_data, (x, y), direction, CELL_SIZE)
        center_view_on_guard(canvas, (x, y), CELL_SIZE, canvas_width, canvas_height)
        canvas.update()
        time.sleep(0.0000001)  # Pause for visualization

        next_y, next_x = y + direction[0], x + direction[1]

        if not is_within_bounds(map_data, next_y, next_x):
            # Guard moves off the map
            print(f"The guard has left the map. Total distinct cells visited: {len(visited_cells)}.")
            break

        # If the guard is entering a new cell and it's not an obstacle
        if (next_y, next_x) not in visited_cells and map_data[next_y][next_x] != '#':
            # Add the new non-obstacle cell to the visited set
            visited_cells.add((next_y, next_x))

        if map_data[next_y][next_x] == '#':
            # If the guard encounters an obstacle turn right
            direction = turn_right(direction)
        elif map_data[next_y][next_x] == 'X' or map_data[next_y][next_x] == '#':
            # If guard encounters a counted obstacle it can still count this new cell
            direction = turn_right(direction)
        elif map_data[next_y][next_x] in ('.', '*'):  # Allow guard to move on trail or floor
            # Move to the next position or continue on the trail
            map_data[y][x] = '*'  # Leave a trail
            y, x = next_y, next_x

    print(f"The guard encountered {len(visited_cells)} distinct cells (excluding obstacles).")

def main():
    file_path = "data.txt"
    if not pathlib.Path(file_path).exists():
        print(f"File '{file_path}' not found.")
        return

    map_data = load_map(file_path)
    rows, cols = len(map_data), len(map_data[0])

    window = tk.Tk()
    window.title("Guard Simulation")

    canvas_width, canvas_height = 650, 650
    canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, scrollregion=(0, 0, cols * CELL_SIZE, rows * CELL_SIZE))

    h_scroll = tk.Scrollbar(window, orient=tk.HORIZONTAL, command=canvas.xview)
    v_scroll = tk.Scrollbar(window, orient=tk.VERTICAL, command=canvas.yview)
    canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    h_scroll.grid(row=1, column=0, sticky="ew")
    v_scroll.grid(row=0, column=1, sticky="ns")
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    simulate_guard(map_data, canvas, canvas_width, canvas_height)

    window.mainloop()

if __name__ == "__main__":
    main()