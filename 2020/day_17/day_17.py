from collections import defaultdict
import itertools

def simulate_pocket_dimension(num_dimensions, num_cycles):
    # In each cycle, this keeps track of the coordinates that are active
    active_set = set()
    # Add the initial active coordinates to the active_set
    with open("input.txt") as f:
        for i, line in enumerate(f):
            for j, c in enumerate(line):
                if c == "#":
                    # Only the first two dimensions are populated in the initial
                    # state. This pads the remaining dimensions with 0s to form
                    # an n-dimensional tuple coordinate
                    active_set.add((i, j) + (num_dimensions - 2) * (0,))
    # Stores the deltas which when added to any coordinate give it its n-
    # dimensional neighbors. Remove (0, 0, ...) from this list because that
    # would give the original coordinate instead of a neighbor
    neighbor_deltas = set(itertools.product([-1, 0, 1], repeat=num_dimensions))
    neighbor_deltas.remove(num_dimensions * (0,))
    # Run each cycle of the simulation
    for i in range(num_cycles):
        # Maps coordinates to their number of active neighbors this cycle.
        # For every active coordinate, add 1 to their neighbors' tallies
        neighbor_counts = defaultdict(int)
        for coord in active_set:
            for deltas in neighbor_deltas:
                neighbor_counts[tuple([coord + delta for coord, delta in zip(coord, deltas)])] += 1
        # Then determine the next round's active coordinates
        new_active_set = set()
        for coord, count in neighbor_counts.items():
            if count == 3 or (count == 2 and coord in active_set):
                new_active_set.add(coord)
        active_set = new_active_set
    return len(active_set)

def part_one():
    print("Part One:")
    print("Number of Active Cubes:", simulate_pocket_dimension(3, 6))

def part_two():
    print("Part Two:")
    print("Number of Active Cubes:", simulate_pocket_dimension(4, 6))

def main():
    part_one()
    part_two()

if __name__ == "__main__":
    main()
