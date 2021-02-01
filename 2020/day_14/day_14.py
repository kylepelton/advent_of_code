import re

def part_one():
    with open("input.txt") as f:
        # Maps addresses to values. Since memory is default initialized to 0,
        # we only need to store the addresses which are explicitly written
        memory = {}
        # Maybe there's a way to do this with just one bit-toggling operation,
        # but the first way that came to mind is to apply the 0s and the 1s
        # in 2 separate masking operations:
        # - The 0s: convert Xs to 1s, then bitwise AND the mask with the value
        # - The 1s: convert Xs to 0s, then bitwise OR the mask with the value
        zeroes_mask = 0
        ones_mask = 0
        for line in f:
            if line.startswith("mask = "):
                # Change the masks
                raw_mask = line.strip().replace("mask = ", "")
                zeroes_mask = int(raw_mask.replace("X", "1"), 2)
                ones_mask = int(raw_mask.replace("X", "0"), 2)
            else:
                # Parse out the address and value
                mem_line = line.strip().split("=")
                address = re.findall(r"\d+", mem_line[0])[0]
                value = int(mem_line[1])
                # Apply the new 0s
                value &= zeroes_mask
                # Apply the new 1s
                value |= ones_mask
                # Write back to memory
                memory[address] = value
        print("Part One:")
        print("Sum:", sum(memory.values()))

def build_addresses(floating_address):
    # Recursively build all real addresses from the floating address by
    # removing each X from the left with a 0 and 1 option, recursing on those,
    # then concatenating the resulting lists
    x_idx = floating_address.find("X")
    if x_idx == -1:
        # Address has no more floating bits, so return as is
        return [int(floating_address, 2)]
    else:
        # Convert the leftmost floating bit into its 2 possible options, then
        # recurse to the next floating bit on both options
        zero_address = floating_address[:x_idx] + "0" + floating_address[x_idx + 1:]
        one_address = floating_address[:x_idx] + "1" + floating_address[x_idx + 1:]
        return build_addresses(zero_address) + build_addresses(one_address)

def part_two():
    with open("input.txt") as f:
        # Maps addresses to values. Since memory is default initialized to 0,
        # we only need to store the addresses which are explicitly written
        memory = {}
        # Stores the current floating mask
        # We use lists for this and the floating address instead of strings
        # to more easily toggle characters. Although I came to that realization
        # after implementing build_addresses(), hence why it uses string splices.
        floating_mask = []
        for line in f:
            if line.startswith("mask = "):
                # Update the floating mask
                floating_mask = list(line.strip().replace("mask = ", ""))
            else:
                # Parse out the original address (padded to 36 bits) and value
                mem_line = line.strip().split("=")
                floating_address = list(format(int(re.findall(r"\d+", mem_line[0])[0]), 'b').zfill(36))
                value = int(mem_line[1])
                # Convert the original address to a floating one according to
                # the rules. Essentially, if it's a 1 or X in the mask, then
                # copy to the floating address. If it's a 0 in the mask, leave
                # the address bit alone.
                floating_address = [floating_mask[i] if floating_mask[i] != "0" \
                                    else floating_address[i] for i in range(36)]
                # Convert the floating address into the real addresses
                addresses = build_addresses("".join(floating_address))
                # Write the value into all the real addresses
                for address in addresses:
                    memory[address] = value
        print("Part Two:")
        print("Sum:", sum(memory.values()))

def main():
    part_one()
    part_two()

if __name__ == "__main__":
    main()
