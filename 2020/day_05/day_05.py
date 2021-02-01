def part_one(lines):
    # Based on the way the seat IDs are created, it's effectively a binary number,
    # where F/L are 0s and B/R are 1s. So convert each string to binary and find
    # the max.
    print("Part One:")
    print("Highest ID:", max([int("".join("0" if c in "FL" else "1" for c in line), 2) for line in lines]))

def part_two(lines):
    # Since X-1 and X+1 will be present (but not X), sort the list and then check
    # for this condition.
    ids = [int("".join("0" if c in "FL" else "1" for c in line), 2) for line in lines]
    ids.sort()
    for i in range(len(ids) - 1):
        if ids[i] + 2 == ids[i + 1]:
            print("Part Two:")
            print("Your ID:", ids[i] + 1)
            break

def main():
    lines = []
    with open("input.txt") as f:
        lines = [line.strip() for line in f]
    part_one(lines)
    part_two(lines)

if __name__ == "__main__":
    main()
