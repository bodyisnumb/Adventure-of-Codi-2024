def parse_disk_map(line: str) -> list[str]:
    blocks = []
    file_id = 0
    for i, ch in enumerate(line):
        length = int(ch)
        if i % 2 == 0:
            blocks.extend([str(file_id)] * length)
            file_id += 1
        else:
            blocks.extend(['.'] * length)
    return blocks

def compact_disk(blocks: list[str]) -> list[str]:
    while True:
        last_file_idx = None
        for i in reversed(range(len(blocks))):
            if blocks[i] != '.':
                last_file_idx = i
                break

        if last_file_idx is None:
            break

        leftmost_dot = None
        for i in range(last_file_idx):
            if blocks[i] == '.':
                leftmost_dot = i
                break

        if leftmost_dot is None:
            # No gaps
            break

        rightmost_file_idx = None
        for i in reversed(range(len(blocks))):
            if blocks[i] != '.':
                rightmost_file_idx = i
                break

        blocks[leftmost_dot], blocks[rightmost_file_idx] = blocks[rightmost_file_idx], '.'

    return blocks

def calculate_checksum(blocks: list[str]) -> int:
    checksum = 0
    for i, b in enumerate(blocks):
        if b != '.':
            file_id = int(b)
            checksum += i * file_id
    return checksum

def main():
    with open('data.txt', 'r') as f:
        line = f.readline().strip()

    # Parse the input into blocks
    blocks = parse_disk_map(line)

    # Compact the disk
    compacted = compact_disk(blocks)

    # Calculate the checksum
    csum = calculate_checksum(compacted)

    print(csum)

if __name__ == "__main__":
    main()