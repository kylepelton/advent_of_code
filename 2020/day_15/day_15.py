def nth_spoken(starting_numbers, n):
    # Maps numbers to last iteration they were read
    history = {}
    # Fill in the 1...n-1 starting iterations. We start at round 1 (not 0)!
    for i in range(1, len(starting_numbers)):
        history[starting_numbers[i - 1]] = i
    # The last starting number will be the last spoken during the first "real"
    # round
    last_spoken = starting_numbers[-1]
    # Run the real rounds
    for i in range(len(starting_numbers) + 1, n + 1):
        # If the last spoken was spoken previously, then the next spoken is
        # the difference between the last round (i-1) and the last round in
        # which it was spoken (history[last_spoken]). If the last spoken has
        # not previously been said, then the next spoken is 0.
        next_spoken = 0
        if last_spoken in history:
            next_spoken = (i-1) - history[last_spoken]
        # Make sure to update the history with the results from round i-1.
        # We wait until round i to do this so we can keep track of when (if at
        # all) the last spoken was last said.
        history[last_spoken] = i-1
        last_spoken = next_spoken
    # Return the nth spoken number
    return last_spoken

def part_one(input):
    print("Part One:")
    print("2020th Spoken:", nth_spoken(input, 2020))

def part_two(input):
    print("Part Two:")
    print("30000000th Spoken:", nth_spoken(input, 30000000))

def main():
    part_one([6, 4, 12, 1, 20, 0, 16])
    part_two([6, 4, 12, 1, 20, 0, 16])

if __name__ == "__main__":
    main()
