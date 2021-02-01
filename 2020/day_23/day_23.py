def play_game(start, table, num_rounds):
    # Simulate each round of the game
    curr = start
    num_cups = len(table) - 1
    for i in range(num_rounds):
        # Pick the three adjacent cups (clockwise) to the current cup
        picked_cups = [table[curr], table[table[curr]], table[table[table[curr]]]]
        # These three cups will be moved somewhere else, so the "next" current
        # will be 4 cups away
        next_curr = table[table[table[table[curr]]]]
        # Determine the destination cup. This is the first cup less than current
        # (mod num_cups) that isn't in the picked cups. Cup 0 is invalid, so
        # special care has to be taken to handle that case
        destination = (curr - 1) % num_cups
        if destination == 0:
            destination = num_cups
        while destination in picked_cups:
            destination = (destination - 1) % num_cups
            if destination == 0:
                destination = num_cups
        # Moved the picked cups. In the table, that's simulated through the
        # following moves. Assume the list is (3) 8  9  1  2  5  4  6  7:
        # - The last picked cup's next becomes destination's next
        # - Destination's next becomes the first picked up cup
        # - Current's next becomes the next current (4 away from current before
        #   moving the picked cups)
        # These moves will result in 3 (2) 8 9 1 5 4 6 7
        table[picked_cups[-1]] = table[destination]
        table[destination] = picked_cups[0]
        table[curr] = next_curr
        curr = next_curr

def part_one():
    input = "739862541"
    num_cups = len(input)
    # Construct a table that maps cup i to its next clockwise cup
    # Basically simulates a circular linked list without having to create node, etc objects
    # Have num_cups + 1 entries in the table to make indexing cups 1-N easier
    table = [0 for i in range(num_cups + 1)]
    for i in range(len(input)):
        table[int(input[i])] = int(input[(i + 1) % num_cups])
    # The first "current" cup is the first digit in the input string
    curr = int(input[0])
    # Play the game for 100 rounds. Table will be modified in-place by the
    # function, so no need to return anything
    play_game(curr, table, 100)
    # The solution string is all the cups clockwise starting with the one
    # after 1 (and not including 1)
    soln = ""
    curr = table[1]
    while True:
        soln += str(curr)
        curr = table[curr]
        if curr == 1:
            break
    print("Part One:")
    print("Solution String:", soln)

def part_two():
    input = "739862541"
    # There are 1 million cups total
    num_cups = 1000000
    # Construct a table that maps cup i to its next clockwise cup
    # Basically simulates a circular linked list without having to create node, etc objects
    # Have num_cups + 1 entries in the table to make indexing cups 1-N easier
    table = [0 for i in range(num_cups + 1)]
    # For the first N-1 input elements, this maps to the next input element
    for i in range(len(input) - 1):
        table[int(input[i])] = int(input[(i + 1) % num_cups])
    # For the last input element, it maps to max input element + 1 (10). Then
    # 10 maps to 11, 11 maps to 12, and so on until 1000000, which maps back to
    # the first input element (7)
    table[int(input[-1])] = len(input) + 1
    for i in range(len(input) + 1, num_cups):
        table[i] = i + 1
    table[num_cups] = int(input[0])
    # The first "current" cup is the first digit in the input string
    curr = int(input[0])
    # Play the game for 10,000,000 rounds. Table will be modified in-place by the
    # function, so no need to return anything
    play_game(curr, table, 10000000)
    print("Part Two:")
    print("Product of Next Two Cups to 1:", table[1] * table[table[1]])

def main():
    part_one()
    part_two()

if __name__ == "__main__":
    main()
