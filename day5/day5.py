def read_data(file_path):
    with open(file_path, "r") as f:
        lines = f.read().strip().split("\n")

    rules = []
    sets = []
    for line in lines:
        if "|" in line:
            rules.append(tuple(map(int, line.split("|"))))
        elif "," in line:
            sets.append(list(map(int, line.split(","))))

    return rules, sets


def validate_set(page_set, rules):
    for before, after in rules:
        if before in page_set and after in page_set:
            if page_set.index(before) > page_set.index(after):
                return False
    return True


def sort_to_make_good(page_set, rules):
    order_map = {page: [] for page in page_set}
    for before, after in rules:
        if before in page_set and after in page_set:
            order_map[after].append(before)

    sorted_pages = []
    while order_map:
        no_dependencies = [page for page, deps in order_map.items() if not deps]
        if not no_dependencies:
            raise ValueError("Circular dependency detected!")
        for page in sorted(no_dependencies):
            sorted_pages.append(page)
            del order_map[page]
        for deps in order_map.values():
            deps[:] = [d for d in deps if d not in no_dependencies]

    return sorted_pages


def sum_middle_pages(sets):
    total = 0
    for page_set in sets:
        mid_index = len(page_set) // 2
        total += page_set[mid_index]
    return total


def main(file_path):
    rules, sets = read_data(file_path)

    good_sets = [page_set for page_set in sets if validate_set(page_set, rules)]
    print("Good Sets:")
    for page_set in good_sets:
        print(page_set)

    middle_sum_good = sum_middle_pages(good_sets)
    print("\nSum of middle pages of good sets:", middle_sum_good)

    bad_sets = [page_set for page_set in sets if not validate_set(page_set, rules)]
    fixed_sets = [sort_to_make_good(page_set, rules) for page_set in bad_sets]

    print("\nFixed Sets (from bad sets):")
    for page_set in fixed_sets:
        print(page_set)

    middle_sum_fixed = sum_middle_pages(fixed_sets)
    print("\nSum of middle pages of fixed sets:", middle_sum_fixed)


if __name__ == "__main__":
    file_path = "data.txt"
    main(file_path)