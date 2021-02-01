def part_one(entries):
    # Finding the entries that sum to 2020 is best found by putting all the
    # entries into a set, iterating over the entries once, and checking if
    # 2020 - entry is in the set. This is O(n) instead of O(n^2).
    unique_entries = set(entries)
    for entry in unique_entries:
        if (2020 - entry) in unique_entries:
            print("Part One:")
            print(entry, " + ", (2020 - entry), " = 2020")
            print(entry, " * ", (2020 - entry), " = ", (entry * (2020 - entry)))
            return

def part_two(entries):
    # Similar to Part 1, but this time we loop twice instead of thrice.
    unique_entries = set(entries)
    for entry1 in unique_entries:
        for entry2 in unique_entries:
            if (2020 - entry1 - entry2) in unique_entries:
                print("Part Two:")
                print(entry1, " + ", entry2, " + ", \
                      (2020 - entry1 - entry2), " = 2020")
                print(entry1, " * ", entry2, " * ", (2020 - entry1 - entry2), \
                      " = ", (entry1 * entry2 * (2020 - entry1 - entry2)))
                return

def main():
    entries = []
    with open("input.txt") as f:
        for line in f:
            entries.append(int(line))
    entries.sort()
    part_one(entries)
    part_two(entries)

if __name__ == "__main__":
    main()
