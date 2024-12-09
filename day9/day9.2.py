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

def find_files(blocks: list[str]) -> list[tuple[int, int, int]]:
    files = []
    n = len(blocks)
    i = 0
    while i < n:
        if blocks[i] != '.':
            file_id = int(blocks[i])
            start = i
            while i < n and blocks[i] == str(file_id):
                i += 1
            end = i - 1
            files.append((file_id, start, end))
        else:
            i += 1
    return files

def find_leftmost_fit(blocks: list[str], file_len: int, file_start: int) -> int:
    count = 0
    start_run = -1
    for i in range(file_start):
        if blocks[i] == '.':
            if count == 0:
                start_run = i
            count += 1
            if count >= file_len:
                return start_run
        else:
            count = 0
            start_run = -1
    return -1

def move_file(blocks: list[str], file_id: int, start: int, end: int) -> None:
    file_len = (end - start + 1)
    free_start = find_leftmost_fit(blocks, file_len, start)
    if free_start == -1:
        return

    for i in range(file_len):
        blocks[free_start + i] = str(file_id)

    for i in range(start, end + 1):
        blocks[i] = '.'

def compact_disk(blocks: list[str]) -> list[str]:
    files = find_files(blocks)
    files.sort(key=lambda x: x[0], reverse=True)

    # Attempt to move each file once
    for file_id, start, end in files:
        move_file(blocks, file_id, start, end)

    return blocks

def calculate_checksum(blocks: list[str]) -> int:
    checksum = 0
    for i, b in enumerate(blocks):
        if b != '.':
            fid = int(b)
            checksum += i * fid
    return checksum

def main():
    with open('data.txt', 'r') as f:
        line = f.readline().strip()

    # Parse the input into blocks
    blocks = parse_disk_map(line)

    # Compact the disk using the new method
    compacted = compact_disk(blocks)

    # Calculate the checksum
    csum = calculate_checksum(compacted)

    print(csum)

if __name__ == "__main__":
    main()