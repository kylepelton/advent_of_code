def count_occupied_neighbors(layout, adjacency_map, r, c):
    # Given the layout, a mapping of coordinates to their adjacent coordinates,
    # and a position, count how many neighboring coordinates are occupied.
    # By taking in an arbitrary adjacency map, this works for both parts.
    count = 0
    for radj, cadj in adjacency_map[(r,c)]:
         if layout[radj][cadj] == "#":
             count += 1
    return count

def part_one(layout):
    # Build a mapping of coordinates to adjacent seats. For this part of the
    # problem, adjacent seats will always be one seat away. Floor spaces are
    # included for completeness, but their entries are left empty.
    adjacency_map = {}
    for r in range(len(layout)):
        for c in range(len(layout[r])):
            adjacency_map[(r,c)] = []
            if layout[r][c] == "L":
                for rdelta, cdelta in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                    if ((0 <= r + rdelta <= len(layout) - 1) and \
                       (0 <= c + cdelta <= len(layout[r + rdelta]) - 1) and \
                       (layout[r + rdelta][c + cdelta] == "L")):
                       # Adjacent space is in range (i.e., not edge case) and
                       # corresponds to a seat, so include in the adjacency map
                       adjacency_map[(r,c)].append((r+rdelta,c+cdelta))
    # Simulate the game
    while True:
        # Construct the next layout
        next_layout = []
        # Keep track of whether any changes occur in this iteration
        num_changes = 0
        for r in range(len(layout)):
            next_layout.append([])
            for c in range(len(layout[r])):
                #num_occupied_neighbors = count_occupied_neighbors(layout, r, c)
                num_occupied_neighbors = count_occupied_neighbors(layout, adjacency_map, r, c)
                if (layout[r][c] == "L") and (num_occupied_neighbors == 0):
                    # Empty seat with no occupied adjacent seats is filled
                    next_layout[r].append("#")
                    num_changes += 1
                elif (layout[r][c] == "#") and (num_occupied_neighbors >= 4):
                    # Occupied seat with 4+ occupied adjacent seats is emptied
                    next_layout[r].append("L")
                    num_changes += 1
                else:
                    # In all other cases, seat state stays the same
                    next_layout[r].append(layout[r][c])
        if num_changes == 0:
            print("Part One:")
            print("Number of Occupied Seats:", sum([r.count("#") for r in layout]))
            return
        else:
            # Overwrite layout with results of this iteration
            layout = next_layout

def part_two(layout):
    # Build a mapping of coordinates to adjacent seats. For this part of the
    # problem, adjacent seats are the first non-floor seat in each direction.
    # Just like in part one, we list entries in the adjacency map for the floor
    # spaces for completeness, but their entries are left blank.
    adjacency_map = {}
    for r in range(len(layout)):
        for c in range(len(layout[r])):
            adjacency_map[(r,c)] = []
            if layout[r][c] == "L":
                for rdelta, cdelta in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                    # Go in this direction until you either find a seat or run
                    # out of room
                    rneighbor = r + rdelta
                    cneighbor = c + cdelta
                    while ((0 <= rneighbor <= len(layout) - 1) and \
                          (0 <= cneighbor <= len(layout[rneighbor]) - 1)):
                          if layout[rneighbor][cneighbor] == "L":
                              adjacency_map[(r,c)].append((rneighbor,cneighbor))
                              break
                          else:
                              rneighbor += rdelta
                              cneighbor += cdelta
    # Simulate the game
    while True:
        # Construct the next layout
        next_layout = []
        # Keep track of whether any changes occur in this iteration
        num_changes = 0
        for r in range(len(layout)):
            next_layout.append([])
            for c in range(len(layout[r])):
                num_occupied_neighbors = count_occupied_neighbors(layout, adjacency_map, r, c)
                if (layout[r][c] == "L") and (num_occupied_neighbors == 0):
                    # Empty seat with no occupied adjacent seats is filled
                    next_layout[r].append("#")
                    num_changes += 1
                elif (layout[r][c] == "#") and (num_occupied_neighbors >= 5):
                    # Occupied seat with 5+ occupied adjacent seats is emptied
                    next_layout[r].append("L")
                    num_changes += 1
                else:
                    # In all other cases, seat state stays the same
                    next_layout[r].append(layout[r][c])
        if num_changes == 0:
            print("Part Two:")
            print("Number of Occupied Seats:", sum([r.count("#") for r in layout]))
            return
        else:
            # Overwrite layout with results of this iteration
            layout = next_layout

def main():
    # 2D array storing each character in the seat layout table
    layout = []
    with open("input.txt") as f:
        for line in f:
            layout.append(list(line.strip()))
    part_one(layout)
    part_two(layout)

if __name__ == "__main__":
    main()
