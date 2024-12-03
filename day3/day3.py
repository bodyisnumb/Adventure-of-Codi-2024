import re


pattern = re.compile(r"mul\(\s*(\d+),\s*(\d+)\s*\)")
results = []


with open("data.txt", "r") as file:
    for line in file:
        matches = pattern.findall(line)
        for x, y in matches:
            results.append(int(x) * int(y))

total_sum = sum(results)

print(f"Individual Results: {results}")
print(f"Total Sum: {total_sum}")