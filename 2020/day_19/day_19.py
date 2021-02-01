def match_msg(msg, rules, rule, idx):
    # This is a recursive function to find all the matching indices in the
    # message for the given rule. By matching index, we mean an index i such
    # that msg[idx:i] (idx to i-1, inclusive) matches rule. This recursive
    # approach works because none of the rules in Part 1 or Part 2 are left
    # recursive
    if idx >= len(msg):
        # Past the end of the message, so there are no possible next indices
        return set()
    if type(rule) is str:
        # This rule is a terminal ("a" or "b"). Check if our index matches the
        # terminal. If so, consume this terminal and return index + 1 as the
        # valid next index to check. If not, we've reached an invalid state
        # and need to backtrack, so return an empty set
        if msg[idx] == rule:
            return {idx + 1}
        else:
            return set()
    # Otherwise, our rule is comprised of nonterminal characters. E.g.:
    #   N: A
    #   N: A B
    #   N: A B | C D E
    # For each option in our rule (each |-separated sub-rule), we need to
    # check whether our message matches. If it does, then we store the indices
    # it matches at. The set we then return is the union of all the options'
    # matching indices.
    match_indices = set()
    for option in rule:
        # Keep track of the matching indices for this option. The initial
        # matching index is the starting index we were provided as input
        option_match_indices = {idx}
        # For each nonterminal in this option (e.g., in N: A B, this would be
        # A then B)
        for nt in option:
            # For each successive nonterminal, we need to find all its matching
            # indices, starting at any of its starting indices, and then we
            # set the next nonterminal's starting indices to this one's matching
            # indices.
            # This is clearer with an example. Say the sub-rule is N: A B, and
            # our starting index is 0. We recursively call this function on A
            # starting at 0 to find all the matching indices for A. Let's say
            # A's matching indices are 2 and 5. That means that indices 2 and 5
            # are the only valid places B can start. So we then recursively call
            # B on starting index 2 AND also recursively call B on starting
            # index 5. Let's say B's matching indices are 3, 4, and 6. At that
            # point, we've reached the end of the sub-rule, so that means that
            # starting at index 0, N: A B can be satisfied by substrings:
            # [0, 2], [0, 3], and [0, 5].
            next_match_indices = set()
            for start_idx in option_match_indices:
                next_match_indices.update(match_msg(msg, rules, rules[nt], start_idx))
            option_match_indices = next_match_indices
        match_indices.update(option_match_indices)
    return match_indices

def part_one(messages, rules):
    count = 0
    for msg in messages:
        # If len(msg) is in the set of matching indices for this message starting
        # at rule 0, then the whole string (0 - N-1) matches rule 0
        if len(msg) in match_msg(msg, rules, rules[0], 0):
            count += 1
    print("Part One:")
    print("Number of Valid Rules:", count)

def part_two(messages, rules):
    count = 0
    for msg in messages:
        # If len(msg) is in the set of matching indices for this message starting
        # at rule 0, then the whole string (0 - N-1) matches rule 0
        if len(msg) in match_msg(msg, rules, rules[0], 0):
            count += 1
    print("Part Two:")
    print("Number of Valid Rules:", count)

def main():
    rules = {}
    messages = []
    with open("input.txt") as f:
        for line in f:
            if line.isspace():
                continue
            line = line.rstrip()
            if line[0].isdigit():
                # This line is a rule
                rule_num, options = line.split(":")
                if "\"" in options:
                    # One of the terminal rules: N: "a" or N: "b"
                    # Parse out the terminal
                    options = options.strip().replace("\"", "")
                else:
                    # One of the nonterminal rules: N: A or N: A B or N: A B | C
                    # Parse into a list of tuples (e.g., [(A, B), (C)])
                    options = options.split("|")
                    for idx, option in enumerate(options):
                        option = tuple(int(nt) for nt in option.strip().split())
                        options[idx] = option
                rules[int(rule_num)] = options
            else:
                # This line is a message
                messages.append(line)
    part_one(messages, rules)
    # For Part 2, update the following rules of the grammar:
    #    8: 42 | 42 8
    #   11: 42 31 | 42 11 31
    rules[8] = [(42,), (42, 8)]
    rules[11] = [(42, 31), (42, 11, 31)]
    part_two(messages, rules)


if __name__ == "__main__":
    main()
