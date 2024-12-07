from itertools import product


def parse_data(file_path):
    equations = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            result, parts = line.split(":")
            result = int(result.strip())
            parts = list(map(int, parts.strip().split()))
            equations.append((result, parts))
    return equations


def evaluate_left_to_right(parts, operators):
    total = parts[0]
    for op, part in zip(operators, parts[1:]):
        if op == "+":
            total += part
        elif op == "*":
            total *= part
    return total


def is_valid_equation(result, parts):
    operators = ['+', '*']
    for ops in product(operators, repeat=len(parts) - 1):
        if evaluate_left_to_right(parts, ops) == result:
            return True
    return False


def process_file(file_path):
    equations = parse_data(file_path)
    total_sum = 0

    for result, parts in equations:
        if is_valid_equation(result, parts):
            print(f"Valid is {result}: {parts}")
            total_sum += result

    return total_sum


if __name__ == "__main__":
    file_path = "data.txt"
    total_sum = process_file(file_path)
    print(f"The sum of valid is: {total_sum}")