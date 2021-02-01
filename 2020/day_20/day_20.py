from collections import defaultdict
import numpy as np
from scipy.ndimage import correlate

# Stores the eight different permutations for a tile's edges. The first
# two parameters are indices into the ndarray, while the third either
# iterates normally or flipped
edge_permutations = (
    # Top edge
    (0, ..., 1, "n"),   # Normal orientation
    (0, ..., -1, "n"),  # Flipped orientation
    # Bottom edge
    (-1, ..., 1, "s"),  # Normal orientation
    (-1, ..., -1, "s"), # Flipped orientation
    # Left edge
    (..., 0, 1, "w"),   # Normal orientation
    (..., 0, -1, "w"),  # Flipped orientation
    # Right edge
    (..., -1, 1, "e"),  # Normal orientation
    (..., -1, -1, "e"), # Flipped orientation
)

def print_image(image):
    # Prints the current image separated into tiles. Useful for debugging.
    for i, r in enumerate(image):
        if i % 8 == 0:
            print(109 * "=")
        for j, c in enumerate(r):
            if j % 8 == 0:
                print("|", sep="", end="")
            print(c, sep="", end="")
        print("|")
    print(109 * "=")

def part_one(tiles):
    # Maps edges to (tile, bordering side) pairs (e.g., {.#..##...# : (20, "w"), ...})
    edge_map = {}
    # Maps tile numbers to (tile, bordering side) pairs (e.g., {1 : {(2, "e"), (5, "s")}, ...})
    tiles_to_edges_map = defaultdict(set)
    # For each tile, iterate over its 8 possible edges
    for tile_num, tile in tiles.items():
        for x, y, f, dir in edge_permutations:
            edge = "".join(tile[x, y][::f])
            if edge in edge_map:
                # Found another tile which shares this edge. Associate these
                # tiles with one another in the tiles_to_edges_map
                other_tile_num, other_tile_dir = edge_map[edge]
                tiles_to_edges_map[tile_num].add((other_tile_num, dir))
                tiles_to_edges_map[other_tile_num].add((tile_num, other_tile_dir))
            else:
                # No other tile shares this edge (yet). Store in the edge map
                # for future reference
                edge_map[edge] = (tile_num, dir)
    # All tiles will either have 2, 3, or 4 shared edges. The ones with 2 shared
    # edges are corner pieces.
    corners = []
    product = 1
    for tile_num, bordering_tiles in tiles_to_edges_map.items():
        if (len(bordering_tiles) == 2):
            product *= tile_num
            corners.append(tile_num)
    print("Part One:")
    print("Product of Corner Pieces:", product)
    return corners, tiles_to_edges_map

def part_two(tiles, corners, tiles_to_edges_map):
    # Part A: Build the Image
    # =======================
    # Start by picking an arbitrary corner and fixing it as the top left corner
    # in the image. This involves rotating this piece until its neighbors are
    # on its south and east sides.
    top_left_tile_num = corners.pop()
    top_left_tile = tiles[top_left_tile_num]
    shared_sides = "".join(sorted(dir for neighbor, dir in tiles_to_edges_map[top_left_tile_num]))
    south_tile_num = 0
    east_tile_num = 0
    if shared_sides == "es":
        # Nothing to do
        south_tile_num = [neighbor for (neighbor, dir) in tiles_to_edges_map[top_left_tile_num] if dir == "s"][0]
        east_tile_num = [neighbor for (neighbor, dir) in tiles_to_edges_map[top_left_tile_num] if dir == "e"][0]
    elif shared_sides == "sw":
        # Rotate 270 degrees
        top_left_tile = np.rot90(top_left_tile, k=3, axes=(1, 0))
        south_tile_num = [neighbor for (neighbor, dir) in tiles_to_edges_map[top_left_tile_num] if dir == "w"][0]
        east_tile_num = [neighbor for (neighbor, dir) in tiles_to_edges_map[top_left_tile_num] if dir == "s"][0]
    elif shared_sides == "nw":
        # Rotate 180 degrees
        top_left_tile = np.rot90(top_left_tile, k=2, axes=(1, 0))
        south_tile_num = [neighbor for (neighbor, dir) in tiles_to_edges_map[top_left_tile_num] if dir == "n"][0]
        east_tile_num = [neighbor for (neighbor, dir) in tiles_to_edges_map[top_left_tile_num] if dir == "w"][0]
    elif shared_sides == "en":
        # Rotate 90 degrees
        top_left_tile = np.rot90(top_left_tile, k=1, axes=(1, 0))
        south_tile_num = [neighbor for (neighbor, dir) in tiles_to_edges_map[top_left_tile_num] if dir == "e"][0]
        east_tile_num = [neighbor for (neighbor, dir) in tiles_to_edges_map[top_left_tile_num] if dir == "n"][0]
    # Now that the top left corner is oriented correctly, we know its east
    # and south edges
    east_edge = "".join(top_left_tile[..., -1])
    south_edge = "".join(top_left_tile[-1, ...])
    # We'll store our image as a large ndarray with the tile edges stripped off
    trimmed_tile_dim = top_left_tile.shape[0] - 2
    image = np.zeros((int(len(tiles) ** 0.5) * trimmed_tile_dim, \
                     int(len(tiles) ** 0.5) * trimmed_tile_dim), "U1")
    # Place the top left corner in the image
    image[0:trimmed_tile_dim, 0:trimmed_tile_dim] = top_left_tile[1:-1, 1:-1]
    # Now comes the fun part -- we have to place all the other tiles in the
    # image. Fortunately, we already have all the information we need. For each
    # tile, we know from the tiles_to_edges_map its neighbors and on what sides
    # (in the given orientation) it matches to those neighbors. And we've locked
    # in the top left corner in the puzzle. So really, all we have to do is
    # build each row of the image from top to bottom. To build a row, we start
    # with the leftmost tile, find which tile borders it on its east side, query
    # that tile, orient it so its west side matches the east side of the leftmost
    # tile, place it in the image, find what tile borders on its east side, and
    # rinse and repeat until we've filled the whole row. Then to start the
    # next row, we look for the piece that borders on the leftmost tile's south
    # side.
    previous_tile_num = top_left_tile_num
    leftmost_tile = top_left_tile
    leftmost_tile_num = top_left_tile_num
    ypos = 0
    # Until we run out of rows
    while True:
        # Based on how we handle the loop, we actually start with the second left
        # tile. We'll handle the leftmost tile of the next row at the bottom of
        # this loop.
        xpos = trimmed_tile_dim
        # Keep finding the next east tile until we reach the end of the row
        while xpos < image.shape[1]:
            # Figure out how we have to rotate the tile to get it to align
            # with its west neighbor. Also keep track of the next tile (i.e.,
            # the one that will be directly east of this one) during these
            # rotations in the next_match_dir variable.
            matching_dir = [dir for (neighbor, dir) in tiles_to_edges_map[east_tile_num] if neighbor == previous_tile_num][0]
            next_match_dir = "e"
            num_turns = 0
            if matching_dir == "n":
                num_turns = 3
                next_match_dir = "s"
            elif matching_dir == "e":
                num_turns = 2
                next_match_dir = "w"
            elif matching_dir == "s":
                num_turns = 1
                next_match_dir = "n"
            rotated_tile = np.rot90(tiles[east_tile_num], k=num_turns, axes=(1,0))
            # The piece is now rotated correctly, but we may have to flip it
            # in order for it to match the previous tile's edge exactly
            if east_edge != "".join(rotated_tile[..., 0]):
                rotated_tile = np.flipud(rotated_tile)
            # Now that it's in the correct orientation, put the tile in the image
            image[ypos:ypos+trimmed_tile_dim, xpos:xpos+trimmed_tile_dim] = rotated_tile[1:-1, 1:-1]
            # Update the variables for the next iteration
            xpos += trimmed_tile_dim
            if xpos < image.shape[1]:
                east_edge = "".join(rotated_tile[..., -1])
                previous_tile_num = east_tile_num
                east_tile_num = [neighbor for (neighbor, dir) in tiles_to_edges_map[east_tile_num] if dir == next_match_dir][0]
        # Handle the leftmost tile of the next row (i.e., the tile directly south
        # of the leftmost tile of this row). The logic is largely the same as
        # above, except for we're looking for the south border this time, and
        # we also need to find this new tile's east border for the next iteration
        ypos += trimmed_tile_dim
        if ypos >= image.shape[0]:
            break
        matching_dir = [dir for (neighbor, dir) in tiles_to_edges_map[south_tile_num] if neighbor == leftmost_tile_num][0]
        next_match_dir_east = "e"
        next_match_dir_south = "s"
        num_turns = 0
        if matching_dir == "e":
            num_turns = 3
            next_match_dir_east = "s"
            next_match_dir_south = "w"
        elif matching_dir == "s":
            num_turns = 2
            next_match_dir_east = "w"
            next_match_dir_south = "n"
        elif matching_dir == "w":
            num_turns = 1
            next_match_dir_east = "n"
            next_match_dir_south = "e"
        rotated_tile = np.rot90(tiles[south_tile_num], k=num_turns, axes=(1,0))
        if south_edge != "".join(rotated_tile[0, ...]):
            rotated_tile = np.fliplr(rotated_tile)
            if next_match_dir_east == "w":
                next_match_dir_east = "e"
            elif next_match_dir_east == "n":
                next_match_dir_east = "s"
            elif next_match_dir_east == "e":
                next_match_dir_east = "w"
            elif next_match_dir_east == "s":
                next_match_dir_east = "n"
        image[ypos:ypos+trimmed_tile_dim, 0:trimmed_tile_dim] = rotated_tile[1:-1, 1:-1]
        south_edge = "".join(rotated_tile[-1, ...])
        east_edge = "".join(rotated_tile[..., -1])
        leftmost_tile_num = south_tile_num
        previous_tile_num = south_tile_num
        east_tile_num = [neighbor for (neighbor, dir) in tiles_to_edges_map[leftmost_tile_num] if dir == next_match_dir_east][0]
        if ypos + trimmed_tile_dim < image.shape[0]:
            south_tile_num = [neighbor for (neighbor, dir) in tiles_to_edges_map[leftmost_tile_num] if dir == next_match_dir_south][0]

    # Part B: Find the Monsters
    # =========================
    # Represent the monster in binary numbers so it can be used in correlation.
    # In hindsight, I think representing it in # vs . characters would have worked
    # as well.
    monster = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0], \
                        [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,1], \
                        [0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0]]).astype(int)
    # We need to know how many 1s/active pixels are in a monster
    monster_ones = monster.sum()
    # Convert the image into binary numbers as well. 0 = ., 1 = #
    image = (image == "#").astype(int)
    # To figure out how many monsters are in the image is the same as running
    # a correlation over the image with the monster as the kernel. We use scipy
    # to perform the correlation. We also have to iterate over the different
    # orientations of the monster to make sure we see it in the image.
    monster_count = 0
    for i in range(4):
        rot90 = np.rot90(monster, k=i)
        fliplr = np.fliplr(np.rot90(monster, k=i))
        monster_count += (correlate(image, rot90, mode="constant") == monster_ones).sum()
        monster_count += (correlate(image, fliplr, mode="constant") == monster_ones).sum()

    # Part C: Calculate the Water Roughness
    # =====================================
    # Water Roughness = Total Number of #s - Number of #s in Monsters
    print("Part Two:")
    print("Water Roughness:", image.sum() - monster_count * monster_ones)

def main():
    # Map tile number to ndarray representation
    tiles = {}
    with open("input.txt") as f:
        # Split file into raw tiles
        raw_tiles = f.read().rstrip().split("\n\n")
        for raw_tile in raw_tiles:
            raw_tile = raw_tile.split("\n")
            # Parse out the tile number
            tile_num = int(raw_tile[0].split()[1].replace(":", ""))
            # Convert the other rows into a 10x10 ndarray storing the tile
            tile = np.zeros((len(raw_tile) - 1, len(raw_tile[1])), "U1")
            tile.flat[:] = list("".join(raw_tile[1:]))
            tiles[tile_num] = tile
    corners, tiles_to_edges_map = part_one(tiles)
    part_two(tiles, corners, tiles_to_edges_map)

if __name__ == "__main__":
    main()
