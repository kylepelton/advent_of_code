def part_one(groups):
    print("Part One:")
    print("Total Counts:", sum(len(set.union(*group)) for group in groups))

def part_two(groups):
    print("Part Two:")
    print("Total Counts:", sum(len(set.intersection(*group)) for group in groups))

def main():
    groups = []
    with open("input.txt") as f:
        group = []
        for i, line in enumerate(f):
            if line == "\n":
                groups.append(group)
                group = []
            else:
                group.append(set(c for c in line.strip()))
        if len(group) != 0:
            groups.append(group)
    part_one(groups)
    part_two(groups)

if __name__ == "__main__":
    main()
