import re


mul_pattern = re.compile(r"mul\(\s*(\d+),\s*(\d+)\s*\)")
results = []
mul_enabled = True

with open("data.txt", "r") as file:
    for line in file:
        tokens = re.split(r"(mul\(\s*\d+,\s*\d+\s*\)|don't\(\)|do\(\))", line)
        for token in tokens:
            token = token.strip()
            if not token:
                continue
            if token == "don't()":
                mul_enabled = False
            elif token == "do()":
                mul_enabled = True
            elif mul_pattern.fullmatch(token) and mul_enabled:
                x, y = map(int, mul_pattern.match(token).groups())
                results.append(x * y)

total_sum = sum(results)

print(f"Individual Results: {results}")
print(f"Total Sum: {total_sum}")