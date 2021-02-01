def part_one(earliest_time, buses):
    # Remove all the x's -- we only want the numeric entries for this part
    buses = [int(i) for i in filter(lambda e: e != "x", buses)]
    # We want the first bus we can get on after earliest_time. To do that,
    # we basically want to calculate which bus has the smallest
    # internal - (earliest_time % interval) -- this corresponds to the
    # amount of time we'll have to wait after earliest_time to get on each
    # bus.
    min_bus = buses[0]
    min_delta = earliest_time + 1
    for bus in buses:
        this_delta = bus - (earliest_time % bus)
        if this_delta < min_delta:
            min_bus = bus
            min_delta = this_delta
    print("Part One:")
    print("Result:", min_delta * min_bus)

def part_two(buses):
    # Map the running buses to (bus_id, remainder) pairs
    buses = [(int(buses[remainder]), remainder) for remainder in range(len(buses)) if buses[remainder] != "x"]
    timestamp = 0
    # The algorithm takes the following approach:
    # Let's say our input (buses, remaining time until leaving) are something like:
    #    (a1, 0), (a2, t2), (a3, t3), (a4, t4), ...
    # We brute force to find the lowest time t that satisfies a1 and a2. The
    # next time t' which satisfies a1 and a2 will be t + lcm(a1, a2). Since a1
    # and a2 are coprime, the lcm will be a1 * a2. So to find the lowest t''
    # that satisfies a1, a2, and a3 will happen at a t + c * a1 * a2 for some c.
    # Since all of our a's are relatively coprime (they're all prime), we can extend
    # this approach. Namely, search over the multiples of a1 until we find a
    # timestamp that satisfies a1 and a2, then start adding multiples of
    # a1 * a2 to that timestamp find a new timestamp that satisfies a1, a2, and a3.
    # Then add multiples of a1 * a2 * a3 to our running timestamp to find a
    # new timestamp that satisfies a1, a2, a3, and a4, etc. For our inputs, this
    # is more than sufficiently efficient.
    lcm = buses[0][0]
    for i in range(1, len(buses)):
        bus_id, remainder = buses[i]
        while (timestamp + remainder) % bus_id != 0:
            timestamp += lcm
        lcm *= bus_id
    print("Part Two:")
    print("Earliest Timestamp:", timestamp)

def main():
    earliest_time = 0
    buses = []
    with open("input.txt") as f:
        lines = [line.strip() for line in f]
        earliest_time = int(lines[0])
        buses = lines[1].split(",")
    part_one(earliest_time, buses)
    part_two(buses)

if __name__ == "__main__":
    main()
