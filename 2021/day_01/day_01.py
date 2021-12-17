def part_one(measurements):
    count = 0
    prev_measurement = measurements[0]
    for i in range(1, len(measurements)):
        curr_measurement = measurements[i]
        if curr_measurement > prev_measurement:
            count += 1
        prev_measurement = curr_measurement
    print("Part One:")
    print("Number of Measurements Larger Than Previous:", count)

def part_two(measurements):
    count = 0
    prev_sum = measurements[0] + measurements[1] + measurements[2]
    for i in range(1, len(measurements) - 2):
        curr_sum = measurements[i] + measurements[i + 1] + measurements[i + 2]
        if curr_sum > prev_sum:
            count += 1
        prev_sum = curr_sum
    print("Part Two:")
    print("Number of Sliding Windows Larger Than Previous:", count)

def main():
    measurements = []
    with open("input.txt", "r") as file:
        for line in file:
            measurements.append(int(line))
    part_one(measurements)
    part_two(measurements)

if __name__ == "__main__":
    main()
