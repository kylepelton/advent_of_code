def part_one(instructions):
    horizontal, depth = 0, 0
    for dir, amt in instructions:
        if dir == "forward":
            horizontal += amt
        elif dir == "up":
            depth -= amt
        elif dir == "down":
            depth += amt
        else:
            print("Something went wrong...")
            print("dir =", dir, ", amt =", amt)
    print("Part One:")
    print("Final Horizontal Position x Final Depth:", horizontal * depth)

def part_two(instructions):
    horizontal, depth, aim = 0, 0, 0
    for dir, amt in instructions:
        if dir == "forward":
            horizontal += amt
            depth += aim * amt
        elif dir == "up":
            aim -= amt
        elif dir == "down":
            aim += amt
        else:
            print("Something went wrong...")
            print("dir =", dir, ", amt =", amt)
    print("Part Two:")
    print("Final Horizontal Position x Final Depth:", horizontal * depth)

def main():
    instructions = []
    with open("input.txt", "r") as file:
        for line in file:
            dir, amt = line.strip().split(" ")
            amt = int(amt)
            instructions.append((dir, amt))
    part_one(instructions)
    part_two(instructions)

if __name__ == "__main__":
    main()
