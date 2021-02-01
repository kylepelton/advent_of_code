def part_one(lines):
    # Only need to keep track of which tiles are currently black
    black_tiles = set()
    # For each instruction/line:
    for line in lines:
        # Represent each hexagon as an (x, y) pair, starting at the origin (0, 0).
        # Moving directly east or west changes x by +1 or -1, respectively.
        # Moving northeast or northwest moves y by +1, but moves x by +0.5/-0.5.
        # Likewise, moving southeast or southwest moves y by -1 and x by +0.5/-0.5.
        # This works due to the geometry of our regular hexagon -- moving in a
        # diagonal is equivalent to moving half a hexagon away.
        x, y = (0, 0)
        tokens = iter(line)
        for char in tokens:
            # Iterate through the valid directions: E, SE, SW, W, NW, NE
            if char == "e":
                x += 1
            elif char == "s":
                y -= 1
                next_char = next(tokens)
                if next_char == "e":
                    x += 0.5
                else:
                    x -= 0.5
            elif char == "w":
                x -= 1
            elif char == "n":
                y += 1
                next_char = next(tokens)
                if next_char == "w":
                    x -= 0.5
                else:
                    x += 0.5
        # Flip this resulting tile's color
        if (x, y) in black_tiles:
            black_tiles.remove((x, y))
        else:
            black_tiles.add((x, y))
    # Print number of black tiles and return the black tiles for usage in Part 2
    print("Part One:")
    print("Number of Black Tiles:", len(black_tiles))
    return black_tiles

def part_two(black_tiles):
    # Offsets to (x, y) coordinates to find the 6 hexagonal neighbors
    neighbor_deltas = ((1,0), (0.5,-1), (-0.5,-1), (-1,0), (-0.5,1), (0.5,1))
    def is_black_next_round(tile, curr_black_tiles):
        # Helper function to check whether a tile should be black next round.
        # This depends on how many neighboring tiles are black this round.
        black_neighbor_count = 0
        for dx, dy in neighbor_deltas:
            if (tile[0] + dx, tile[1] + dy) in curr_black_tiles:
                black_neighbor_count += 1
        if tile in curr_black_tiles:
            return black_neighbor_count == 1 or black_neighbor_count == 2
        else:
            return black_neighbor_count == 2
    # Run through the 100 iterations of this game
    for i in range(100):
        # Keep track of which tiles we've already determined for the next round.
        # This helps speed up cases where a lot of neighboring tiles are black.
        checked_tiles = set()
        # Store all the tiles that will be black next round
        new_black_tiles = set()
        # The only tiles that could be black next round are current black tiles
        # and their neighbors
        for bt in black_tiles:
            if bt not in checked_tiles:
                if is_black_next_round(bt, black_tiles):
                    new_black_tiles.add(bt)
                checked_tiles.add(bt)
            for dx, dy in neighbor_deltas:
                nt = (bt[0] + dx, bt[1] + dy)
                if nt not in checked_tiles:
                    if is_black_next_round(nt, black_tiles):
                        new_black_tiles.add(nt)
                    checked_tiles.add(nt)
        # Update the black tiles for the next round
        black_tiles = new_black_tiles
    print("Part Two:")
    print("Number of Black Tiles:", len(black_tiles))

def main():
    lines = []
    with open("input.txt") as f:
        lines = [line.strip() for line in f]
    black_tiles = part_one(lines)
    part_two(black_tiles)

if __name__ == "__main__":
    main()
