from functools import lru_cache

@lru_cache(None)
def transform_stone(stone_str: str) -> list[str]:
    #If stone is '0'
    if stone_str == '0':
        return ['1']

    length = len(stone_str)
    # Even number of digits split into two halves
    if length % 2 == 0:
        mid = length // 2
        left = str(int(stone_str[:mid]))   # Remove leading zeros
        right = str(int(stone_str[mid:]))
        return [left, right]
    else:
        # Odd number of digits multiply by 2024
        val = int(stone_str)
        new_val = val * 2024
        return [str(new_val)]

def main():
    # Read stones
    with open('data.txt', 'r') as f:
        line = f.readline().strip()

    # Create a dictionary {stone_str: count}
    stone_map = {}
    for s in line.split():
        stone_map[s] = stone_map.get(s, 0) + 1

    # Number of blinks (25 or 75)
    blinks = 75

    for i in range(blinks):
        new_stone_map = {}
        # Transform each unique stone once
        for stone_str, count in stone_map.items():
            transformed = transform_stone(stone_str)
            for t in transformed:
                new_stone_map[t] = new_stone_map.get(t, 0) + count

        stone_map = new_stone_map
        print(f"Completed blink {i+1}")

    # Count total stones
    total_stones = sum(stone_map.values())
    print(total_stones)

if __name__ == '__main__':
    main()