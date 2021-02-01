def part_one(numbers):
    preamble = 25
    # Loop over all numbers after the preamble
    for i in range(preamble, len(numbers)):
        curr = numbers[i]
        seen_set = set()
        found = False
        # For the current number, check the previous preamble numbers
        for j in range(i - 25, i):
            # Keep track of the numbers we see in this preamble in a set for
            # O(1) search time. If this target is in the set, then we've found
            # 2 numbers in the preamble that sum to curr.
            target = curr - numbers[j]
            if target in seen_set:
                found = True
                break
            seen_set.add(numbers[j])
        if not found:
            print("Part One:")
            print("First Number:", curr)
            return curr

def part_two(numbers, invalid_number):
    # Brute-force approach that fixes the leftmost point of the contiguous
    # range and grows the rightmost point until it finds a sum that matches
    # the invalid number of runs out of elements. If it runs out of elements,
    # it moves the leftmost point to the right one and repeats the process.
    for i in range(len(numbers)):
        sum = numbers[i]
        for j in range(i+1, len(numbers)):
            sum += numbers[j]
            if sum == invalid_number:
                print("Part Two:")
                print("Sum of Min and Max In Range:", min(numbers[i:j+1]) + max(numbers[i:j+1]))
                return
            if sum > invalid_number:
                # There are no negative numbers in our input data, so if our
                # contiguous sum exceeds the invalid number, we can drop out
                # early
                break

def main():
    numbers = []
    with open("input.txt") as f:
        numbers = [int(line.strip()) for line in f]
    invalid_number = part_one(numbers)
    part_two(numbers, invalid_number)

if __name__ == "__main__":
    main()
