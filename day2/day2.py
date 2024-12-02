def is_safe_report(report):
    ascending = all(report[i] <= report[i + 1] for i in range(len(report) - 1))
    descending = all(report[i] >= report[i + 1] for i in range(len(report) - 1))
    within_distance = all(1 <= abs(report[i] - report[i + 1]) <= 3 for i in range(len(report) - 1))
    return (ascending or descending) and within_distance


def is_dampened_safe_report(report):
    if len(report) < 3:
        return False
    for i in range(len(report)):
        modified_report = report[:i] + report[i + 1:]
        if is_safe_report(modified_report):
            return True
    return False


with open("data.txt", "r") as file:
    reports = [[int(num) for num in line.split()] for line in file]


safe_count = sum(is_safe_report(report) for report in reports)
dampened_safe_count = sum(is_dampened_safe_report(report) for report in reports)


print(f"Number of safe reports: {safe_count}")
print(f"Number of dampened safe reports: {dampened_safe_count}")