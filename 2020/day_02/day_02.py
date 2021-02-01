def part_one(lines):
    count = 0
    for line in lines:
        # Split each line into its corresponding fields
        # [min-max] [character:] [password]
        fields = line.split()
        # Parse out the min and max number of occurrences of the character
        low, high = map(int, fields[0].split("-"))
        # Remove the colon at the end of the character
        fields[1] = fields[1].replace(":", "")
        # Then just check that the number of occurrences is in the range
        if fields[2].count(fields[1]) in range(low, high + 1):
            count += 1
    print("Part One:")
    print("Number of Valid Passwords =", count)

def part_two(lines):
    count = 0
    for line in lines:
        # Split each line into its corresponding fields
        # [low_index-high_index] [character:] [password]
        fields = line.split()
        # Parse out the first and second indexes
        # Since they are 1-based indexes, convert to 0-based
        low, high = [(x - 1) for x in map(int, fields[0].split("-"))]
        # Remove the colon at the end of the character
        fields[1] = fields[1].replace(":", "")
        # Character must be in either the low or high position, but not both
        if (fields[2][low] == fields[1]) ^ (fields[2][high] == fields[1]):
            count += 1
    print("Part Two:")
    print("Number of Valid Passwords =", count)

def main():
    lines = []
    with open("input.txt") as f:
        lines = [line for line in f]
    part_one(lines)
    part_two(lines)

if __name__ == "__main__":
    main()
