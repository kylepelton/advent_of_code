def part_one(numbers):
    # Count the number of 1s in each column
    counts = [0] * len(numbers[0])
    for i in range(len(numbers[0])):
        counts[i] = sum(1 for num in numbers if num[i] == "1")
    # Gamma rate corresponds to most common bit at each digit
    # Epsilon rate corresponds to least common bit at each digit
    gamma_rate, epsilon_rate = "", ""
    for c in counts:
        if c > len(numbers) / 2:
            gamma_rate += "1"
            epsilon_rate += "0"
        else:
            gamma_rate += "0"
            epsilon_rate += "1"
    gamma_rate = int(gamma_rate, 2)
    epsilon_rate = int(epsilon_rate, 2)
    print("Part One:")
    print("Power Consumption:", gamma_rate * epsilon_rate)

def part_two(numbers):
    def filter_by_bit_criteria(original_numbers, rating):
        """Common function for filtering the original list by a bit criteria"""
        filtered_numbers = original_numbers[:]
        for i in range(len(original_numbers[0])):
            # Count the number of 1s in the ith column of the current list
            count = sum(1 for num in filtered_numbers if num[i] == "1")
            if rating == "oxygen":
                # For the oxygen rating, keep numbers with the more common digit
                # If both digits are equally common, use 1
                filter_digit = "1" if count >= len(filtered_numbers) / 2 else "0"
            else:
                # For the CO2 rating, keep numbers with the less common digit
                # If both digits are equally common, use 0
                filter_digit = "0" if count >= len(filtered_numbers) / 2 else "1"
            filtered_numbers = [num for num in filtered_numbers if num[i] == filter_digit]
            if len(filtered_numbers) == 1:
                return int(filtered_numbers[0], 2)

    oxygen_rating = filter_by_bit_criteria(numbers, "oxygen")
    co2_rating = filter_by_bit_criteria(numbers, "co2")
    print("Part Two:")
    print("Life Support Rating:", oxygen_rating * co2_rating)

def main():
    numbers = []
    with open("input.txt", "r") as file:
        for line in file:
            numbers.append(line.strip())
    part_one(numbers)
    part_two(numbers)

if __name__ == "__main__":
    main()
