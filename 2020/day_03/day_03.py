def count_collisions(lines, num_right, num_down):
    count = 0
    index = 0
    # This loop takes advantage of the [start:stop:step] slicing syntax to
    # iterate over every num_down rows. It creates a copy, so it's not to be
    # used on large arrays. But it's fine for our purpose.
    for line in lines[::num_down]:
        if line[(index % len(line))] == "#":
            count += 1
        index += num_right
    return count

def part_one(lines):
    print("Part One:")
    print("Number of Trees:", count_collisions(lines, 3, 1))

def part_two(lines):
    print("Part Two:")
    print("Number of Trees:", \
          count_collisions(lines, 1, 1) * count_collisions(lines, 3, 1) * \
          count_collisions(lines, 5, 1) * count_collisions(lines, 7, 1) * \
          count_collisions(lines, 1, 2))

def main():
    lines = []
    with open("input.txt") as f:
        # The newline character at the end messes with the modulo math, so
        # remove it
        lines = [line.strip() for line in f]
    part_one(lines)
    part_two(lines)

if __name__ == "__main__":
    main()
