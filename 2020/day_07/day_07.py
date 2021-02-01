def part_one(bags):
    # The bags which contain shiny gold bags (directly or indirectly)
    answer_bags = set()
    # The queue of bags to check
    # These bags are "reachable" from the shiny gold bag
    discovered_bags = ["shiny gold"]
    # Basically perform a breadth-first search on the graph of bags
    # Start with the shiny gold bag. Determine what bags it can be in, then
    # check what bags those bags can be in, etc. Keep going until you run
    # out of bags. While normally you would also want to keep a visited set
    # to prevent running into cycles, this problem is intuitively a directed
    # acyclic graph, so that check won't be necessary
    while len(discovered_bags) != 0:
        # Pick the next bag from the queue
        curr = discovered_bags.pop(0)
        # See which bags contain this bag
        for bag in bags:
            if bag in answer_bags:
                # Avoid double counting
                continue
            elif curr in bags[bag]:
                # The bag from the queue is in this bag, which means that this
                # bag must be reachable from the shiny gold bag in the graph,
                # which means that this bag holds shiny gold bags. Add it to
                # our answer set and also to the discovered queue
                discovered_bags.append(bag)
                answer_bags.add(bag)
    print("Part One:")
    print("Number of Bags that Contain Shiny Gold Bags:", len(answer_bags))

def part_two(bags):
    # Helper to recursively count the number of bags in a given bag
    def counter(bag):
        # To make the multiplication math nicer, count the bag itself
        count = 1
        # For each bag in our bag, multiply its multiplicity by the number of bags
        # it contains
        for k, v in bags[bag].items():
            if v != 0:
                count += v * counter(k)
        return count
    # Take off one at the end because our algorithm counts the shiny gold bag
    print("Part Two:")
    print("Number of Bags that Shiny Gold Bags Contain:", counter("shiny gold") - 1)

def main():
    # Dictionary of bag names => {contained bag names: counts}
    bags = {}
    with open("input.txt") as f:
        for line in f:
            bag = {}
            description, contents = line.split("contain")
            bag_name = " ".join(description.strip().split(" ")[:2])
            contents = contents.split(",")
            for c in contents:
                words = c.strip().split(" ")
                count = 0 if words[0] == "no" else int(words[0])
                name = " ".join(words[1:3])
                bag[name] = count
            bags[bag_name] = bag
    part_one(bags)
    part_two(bags)

if __name__ == "__main__":
    main()
