from copy import deepcopy
from itertools import pairwise
from typing import List, Tuple, Set, Iterable


def read_garden(file_name: str = "data.txt") -> List[List[str]]:
    with open(file_name, "r", encoding="utf-8") as f:
        return [list(line.strip()) for line in f if line.strip()]


def iter_neighbours(value: str, pos: Tuple[int, int], garden: List[List[str]], height: int, width: int):
    for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        nr, nc = pos[0] + dr, pos[1] + dc
        if 0 <= nr < height and 0 <= nc < width and garden[nr][nc] == value:
            yield nr, nc


def get_region_params(pos: Tuple[int, int], garden: List[List[str]], original_garden: List[List[str]], height: int, width: int) -> Tuple[int, int]:
    value = garden[pos[0]][pos[1]]
    if value == "":
        return 0, 0
    area, perimeter = 1, 4
    garden[pos[0]][pos[1]] = ""
    for neighbor in iter_neighbours(value, pos, original_garden, height, width):
        perimeter -= 1
        add_area, add_perimeter = get_region_params(neighbor, garden, original_garden, height, width)
        area += add_area
        perimeter += add_perimeter
    return area, perimeter


def get_region(pos: Tuple[int, int], garden: List[List[str]], original_garden: List[List[str]], height: int, width: int) -> Set[Tuple[int, int]]:
    value = garden[pos[0]][pos[1]]
    region = set()
    if value == "":
        return region
    region.add(pos)
    garden[pos[0]][pos[1]] = ""
    for neighbor in iter_neighbours(value, pos, original_garden, height, width):
        region.update(get_region(neighbor, garden, original_garden, height, width))
    return region


def get_region_sides(region: Iterable[Tuple[int, int]]) -> int:
    region = sorted(region, key=lambda pos: (pos[0], pos[1]))
    sides = 0
    prev_rights, prev_lefts, rights, lefts = set(), set(), set(), {region[0][1]}
    for position, next_position in pairwise(region + [(region[-1][0] + 1, -1)]):
        if next_position[0] == position[0]:
            if next_position[1] - position[1] > 1:
                rights.add(position[1])
                lefts.add(next_position[1])
        else:
            rights.add(position[1])
            sides += 2 * sum(1 for left in lefts if left not in prev_lefts)
            sides += 2 * sum(1 for right in rights if right not in prev_rights)
            prev_rights, prev_lefts = rights, lefts
            rights, lefts = set(), {next_position[1]}
    return sides


def calculate_prices(file_name: str):
    garden = read_garden(file_name)
    original_garden = deepcopy(garden)
    height, width = len(garden), len(garden[0])

    part1, part2 = 0, 0
    for i in range(height):
        for j in range(width):
            area, perimeter = get_region_params((i, j), garden, original_garden, height, width)
            part1 += area * perimeter

    garden = read_garden(file_name)
    original_garden = deepcopy(garden)
    for i in range(height):
        for j in range(width):
            region = get_region((i, j), garden, original_garden, height, width)
            if region:
                part2 += len(region) * get_region_sides(region)

    return part1, part2


if __name__ == "__main__":
    part1, part2 = calculate_prices("data.txt")
    print(f"Total Price Original (Part 1): {part1}")
    print(f"Total Price Discounted (Part 2): {part2}")