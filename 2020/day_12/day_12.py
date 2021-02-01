def part_one():
    with open("input.txt") as f:
        # Vertical and horizontal offsets (N, E positive; S, W negative)
        vertical, horizontal = (0, 0)
        # Orientation in degrees. Starts facing east
        orientation = 0
        # Parse each instruction from the file
        for line in f:
            opcode = line.strip()[0]
            units = int(line.strip()[1:])
            if opcode == "N":
                vertical += units
            elif opcode == "S":
                vertical -= units
            elif opcode == "E":
                horizontal += units
            elif opcode == "W":
                horizontal -= units
            elif opcode == "L":
                orientation += units
            elif opcode == "R":
                orientation -= units
            elif opcode == "F":
                # Determine which direction we're facing before moving
                direction = (orientation % 360)
                if direction == 0:     # East
                    horizontal += units
                elif direction == 90:  # North
                    # Moving north
                    vertical += units
                elif direction == 180: # West
                    horizontal -= units
                elif direction == 270: # South
                    vertical -= units
        print("Part One:")
        print("Manhattan Distance:", abs(vertical) + abs(horizontal))

def part_two():
    with open("input.txt") as f:
        # Ship's vertical and horizontal offsets (N, E positive; S, W negative)
        ship_vertical, ship_horizontal = (0, 0)
        # Waypoint's vertical and horizontal offsets (N, E positive; S, W negative)
        # Waypoint starts 10 units to the east and 1 unit to the north
        waypt_vertical, waypt_horizontal = (1, 10)
        # Parse each instruction from the file
        for line in f:
            opcode = line.strip()[0]
            units = int(line.strip()[1:])
            # For N/S/E/W, move the waypoint
            if opcode == "N":
                waypt_vertical += units
            elif opcode == "S":
                waypt_vertical -= units
            elif opcode == "E":
                waypt_horizontal += units
            elif opcode == "W":
                waypt_horizontal -= units
            elif opcode == "L":
                # Rotate waypoint about the ship counter-clockwise
                # Only need to rotate if the rotation is non-zero (mod 360)
                units %= 360
                if units == 90:
                    # Vertical/horizontal magnitudes flip, horizontal sign flips
                    waypt_vertical, waypt_horizontal = (waypt_horizontal, -waypt_vertical)
                elif units == 180:
                    # Vertical/horizontal magnitudes stay the same, just the signs flip
                    waypt_vertical, waypt_horizontal = (-waypt_vertical, -waypt_horizontal)
                elif units == 270:
                    # Vertical/horizontal magnitudes flip, vertical sign flips
                    waypt_vertical, waypt_horizontal = (-waypt_horizontal, waypt_vertical)
            elif opcode == "R":
                # Rotate waypoint about the ship clockwise
                # Only need to rotate if the rotation is non-zero (mod 360)
                units %= 360
                if units == 90:
                    # Vertical/horizontal magnitudes flip, vertical sign flips
                    waypt_vertical, waypt_horizontal = (-waypt_horizontal, waypt_vertical)
                elif units == 180:
                    # Vertical/horizontal magnitudes stay the same, just the signs flip
                    waypt_vertical, waypt_horizontal = (-waypt_vertical, -waypt_horizontal)
                elif units == 270:
                    # Vertical/horizontal magnitudes flip, horizontal sign flips
                    waypt_vertical, waypt_horizontal = (waypt_horizontal, -waypt_vertical)
            elif opcode == "F":
                # Move the ship "units" times relative to the waypoint
                ship_vertical += units * waypt_vertical
                ship_horizontal += units * waypt_horizontal
        print("Part Two:")
        print("Manhattan Distance:", abs(ship_vertical) + abs(ship_horizontal))

def main():
    part_one()
    part_two()

if __name__ == "__main__":
    main()
