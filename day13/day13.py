import sys


def parse_input(filename):
    machines = []
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
        for i in range(0, len(lines), 3):  # Every 3 lines
            if i + 2 >= len(lines):
                print(f"Incomplete data for machine  {i + 1}")
                break
            # Parse Button A
            button_a_line = lines[i]
            button_a_values = button_a_line.split(': ')[1].split(', ')
            A_x_str, A_y_str = button_a_values
            A_x = int(A_x_str.replace('X+', '').replace('X-', ''))
            A_y = int(A_y_str.replace('Y+', '').replace('Y-', ''))
            if 'X-' in A_x_str:
                A_x = -A_x
            if 'Y-' in A_y_str:
                A_y = -A_y
            # Parse Button B
            button_b_line = lines[i + 1]
            button_b_values = button_b_line.split(': ')[1].split(', ')
            B_x_str, B_y_str = button_b_values
            B_x = int(B_x_str.replace('X+', '').replace('X-', ''))
            B_y = int(B_y_str.replace('Y+', '').replace('Y-', ''))
            if 'X-' in B_x_str:
                B_x = -B_x
            if 'Y-' in B_y_str:
                B_y = -B_y
            # Parse Prize
            prize_line = lines[i + 2]
            prize_values = prize_line.split(': ')[1].split(', ')
            X_str, Y_str = prize_values
            X = int(X_str.replace('X=', '').replace('X-', ''))
            Y = int(Y_str.replace('Y=', '').replace('Y-', ''))
            if 'X-' in X_str:
                X = -X
            if 'Y-' in Y_str:
                Y = -Y
            machines.append({
                "button_a": (A_x, A_y),
                "button_b": (B_x, B_y),
                "prize": (X, Y),
            })
    return machines


def find_min_tokens(A_x, A_y, B_x, B_y, X, Y, press_limit_a=None, press_limit_b=None):
    D = A_x * B_y - A_y * B_x

    if D == 0:
        if (A_x * Y != A_y * X) or (B_x * Y != B_y * X):
            return None  # Inconsistent no solution
        # Infinitely many solutions = find the one with minimal tokens
        min_tokens = None
        # Express a in terms of b: a = (X - B_x * b) / A_x
        if A_x == 0 and B_x == 0:
            # Both A_x and B_x are zero prize X must be zero
            if X != 0:
                return None
            # Any a and b such that a*A_y + b*B_y = Y
            # minimize 3a + b, prefer b
            if B_y == 0:
                if A_y == 0:
                    if Y == 0:
                        # Any a and b, choose a=0, b=0
                        return 0
                    else:
                        return None
                else:
                    if Y % A_y != 0:
                        return None
                    a = Y // A_y
                    if press_limit_a is not None and a > press_limit_a:
                        return None
                    tokens = 3 * a
                    return tokens
            else:
                # B_y !=0
                # To minimize 3a + b, maximize b
                b_max = Y // B_y
                for b in range(b_max, -1, -1):
                    remaining_Y = Y - B_y * b
                    if A_y == 0:
                        if remaining_Y != 0:
                            continue
                        a = 0
                    else:
                        if remaining_Y % A_y != 0:
                            continue
                        a = remaining_Y // A_y
                    if a < 0:
                        continue
                    if press_limit_a is not None and a > press_limit_a:
                        continue
                    tokens = 3 * a + b
                    if (min_tokens is None) or (tokens < min_tokens):
                        min_tokens = tokens
                return min_tokens

        # Since a = (X - B_x * b) / A_x
        if A_x != 0:
            # Find b such that (X - B_x * b) is divisible by A_x and a >=0
            # b_max = X // B_x if B_x >0 else 0
            if B_x > 0:
                b_max = X // B_x
            elif B_x < 0:
                b_max = 0  # Since b >=0, and B_x <0, b can only be 0
            else:
                # B_x ==0
                if X % A_x != 0:
                    return None
                a = X // A_x
                if a < 0:
                    return None
                if press_limit_a is not None and a > press_limit_a:
                    return None
                # check Y
                if A_y * a != Y:
                    return None
                tokens = 3 * a
                return tokens
            for b in range(b_max, -1, -1):
                remaining_X = X - B_x * b
                if A_x == 0:
                    if remaining_X != 0:
                        continue
                    a = 0
                else:
                    if remaining_X % A_x != 0:
                        continue
                    a = remaining_X // A_x
                if a < 0:
                    continue
                if press_limit_a is not None and a > press_limit_a:
                    continue
                # check Y
                if A_y * a + B_y * b != Y:
                    continue
                tokens = 3 * a + b
                if (min_tokens is None) or (tokens < min_tokens):
                    min_tokens = tokens
        else:
            # A_x ==0, handle similar to above
            if X != 0:
                return None
            # Now, B_x must also be zero (since D=0 and A_x=0)
            # So, solve for Y: A_y * a + B_y * b = Y
            # To minimize 3a + b, prefer larger b
            if B_y == 0:
                if A_y == 0:
                    if Y == 0:
                        # Any a and b, choose a=0, b=0
                        return 0
                    else:
                        return None
            # Iterate over b to maximize b
            if B_y > 0:
                b_max = Y // B_y
            elif B_y < 0:
                b_max = 0
            else:
                # B_y ==0
                if Y % A_y != 0:
                    return None
                a = Y // A_y
                if a < 0:
                    return None
                if press_limit_a is not None and a > press_limit_a:
                    return None
                tokens = 3 * a
                return tokens
            for b in range(b_max, -1, -1):
                remaining_Y = Y - B_y * b
                if A_y == 0:
                    if remaining_Y != 0:
                        continue
                    a = 0
                else:
                    if remaining_Y % A_y != 0:
                        continue
                    a = remaining_Y // A_y
                if a < 0:
                    continue
                if press_limit_a is not None and a > press_limit_a:
                    continue
                tokens = 3 * a + b
                if (min_tokens is None) or (tokens < min_tokens):
                    min_tokens = tokens
        return min_tokens

    else:
        numerator_a = X * B_y - Y * B_x
        numerator_b = A_x * Y - A_y * X

        if D < 0:
            numerator_a = -numerator_a
            numerator_b = -numerator_b
            D = -D

        if numerator_a % D != 0 or numerator_b % D != 0:
            return None  # No integer solution
        a = numerator_a // D
        b = numerator_b // D
        if a < 0 or b < 0:
            return None  # Negative presses not allowed
        if press_limit_a is not None and a > press_limit_a:
            return None
        if press_limit_b is not None and b > press_limit_b:
            return None
        if A_y * a + B_y * b != Y:
            return None
        tokens = 3 * a + b
        return tokens


def adjust_prize(prize, adjustment=10_000_000_000_000):
    return (prize[0] + adjustment, prize[1] + adjustment)


def process_machines(machines, part, adjustment=0):
    total_prizes = 0
    total_tokens = 0
    for idx, machine in enumerate(machines, 1):
        A_x, A_y = machine["button_a"]
        B_x, B_y = machine["button_b"]
        X, Y = machine["prize"]
        if adjustment != 0:
            X, Y = adjust_prize((X, Y), adjustment)
        if part == 1:
            tokens = find_min_tokens(A_x, A_y, B_x, B_y, X, Y, press_limit_a=100, press_limit_b=100)
        else:
            tokens = find_min_tokens(A_x, A_y, B_x, B_y, X, Y)
        if tokens is not None:
            total_prizes += 1
            total_tokens += tokens
    return total_prizes, total_tokens


def main():
    filename = 'data.txt'
    machines = parse_input(filename)

    # Part 1
    part1_prizes, part1_tokens = process_machines(machines, part=1, adjustment=0)
    print("=== Part 1 Results ===")
    print(f"Total prizes won in Part 1: {part1_prizes}")
    print(f"Minimum tokens required in Part 1: {part1_tokens}")

    # Part 2
    part2_prizes, part2_tokens = process_machines(machines, part=2, adjustment=10_000_000_000_000)
    print("\n=== Part 2 Results ===")
    print(f"Total prizes won in Part 2: {part2_prizes}")
    print(f"Minimum tokens required in Part 2: {part2_tokens}")


if __name__ == "__main__":
    main()