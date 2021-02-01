def run_program(instructions):
    index = 0
    accumulator = 0
    while index < len(instructions):
        if instructions[index][2] > 0:
            # This instruction has been executed more than once, meaning we've
            # entered an infinite loop
            return (False, accumulator)
        instructions[index][2] += 1
        if instructions[index][0] == "acc":
            accumulator += instructions[index][1]
            index += 1
        elif instructions[index][0] == "jmp":
            index += instructions[index][1]
        elif instructions[index][0] == "nop":
            index += 1
    # Program finished successfully
    return (True, accumulator)

def part_one(instructions):
    print("Part One:")
    print("Accumulator:", run_program(instructions)[1])

def part_two(instructions):
    for i in range(len(instructions)):
        if instructions[i][0] == "jmp" or instructions[i][0] == "nop":
            # Flip the jmp/nop instruction, then simulate the program
            instructions[i][0] = "jmp" if instructions[i][0] == "nop" else "nop"
            success, accumulator = run_program(instructions)
            if success:
                print("Part Two:")
                print("Accumulator:", accumulator)
                return
            else:
                # Reset the instructions for the next run
                instructions[i][0] = "jmp" if instructions[i][0] == "nop" else "nop"
                for instruction in instructions:
                    instruction[2] = 0

def main():
    # Instructions stored in the form [opcode, value, # times run]
    instructions = []
    with open("input.txt") as f:
        for line in f:
            opcode, value = line.strip().split(" ")
            instructions.append([opcode, int(value), 0])
    part_one(instructions)
    part_two(instructions)

if __name__ == "__main__":
    main()
