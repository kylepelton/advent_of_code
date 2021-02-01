def part_one(adapters):
    # We have to use all adapters, so the easiest way to do this is to sort
    # the adapters, look at the differences between them, and count all the
    # 1 and 3 jolt differences
    adapters.sort()
    # Add fake adapters for charging outlet (0 jolts) and device's built-in
    # adapter (3 jolts higher than the highest adapter)
    adapters.insert(0, 0)
    adapters.append(adapters[-1] + 3)
    one_jolt_count = 0
    three_jolt_count = 0
    for i in range(len(adapters) - 1):
        diff = adapters[i + 1] - adapters[i]
        if diff == 1:
            one_jolt_count += 1
        elif diff == 3:
            three_jolt_count += 1
    print("Part One:")
    print("Result:", one_jolt_count * three_jolt_count)

def part_two(adapters):
    # Start by sorting the list of adapters. The fake adapters (the charging
    # outlet and the device's built-in adapter) can be omitted because there
    # is only one way to get to them (only one way to get to 0 and only one
    # way to get to max + 3)
    adapters.sort()
    # Use dynamic programming/memoization to store intermediate results.
    # Specifically, some some adapter jolt value j, the number of ways
    # to get to it is:
    #   Number of Ways[j] = Number of Ways[j-1] + Number of Ways[j-2] + Number of Ways[j-3]
    # So if we start at the lowest values of j and work our way up, we can
    # calculate the max number of combinations without getting into recursion
    # bloat. In this case, counts[i] will refer to the number of ways to get
    # to i jolts. Technically there's one way to get to 0 jolts, but it's
    # unused in this implementation (in fact, it's only there to make the
    # indexing easier). Our table has enough elements to store the max adapter's
    # number of ways.
    counts = [0 for i in range(max(adapters) + 1)]
    for i in range(1, len(adapters)):
        # This also has to handle the edge cases
        if adapters[i] == 1:
            counts[1] = 1
        elif adapters[i] == 2:
            counts[2] = 1 + counts[1]
        elif adapters[i] == 3:
            counts[3] = 1 + counts[1] + counts[2]
        else:
            counts[adapters[i]] = counts[adapters[i] - 1] + \
                                  counts[adapters[i] - 2] + \
                                  counts[adapters[i] - 3]
    print("Part Two:")
    print("Number of Ways:", counts[adapters[-1]])

def main():
    adapters = []
    with open("input.txt") as f:
        adapters = [int(line.strip()) for line in f]
    part_one(adapters)
    part_two(adapters)

if __name__ == "__main__":
    main()
