import itertools

def part_one(rules, my_ticket, nearby_tickets):
    # Check each field in each ticket to see if it satisfies at least one rule.
    # If not, add its value to the error rate, the sum of all fields which
    # satisfy NO rules.
    # Also, for part 2, build up a new array of nearby tickets that drops rows
    # which contain invalid fields
    error_rate = 0
    good_nearby_tickets = []
    for ticket in nearby_tickets:
        valid_ticket = True
        for field in ticket:
            valid_field = False
            for name, ranges in rules.items():
                if ranges[0][0] <= field <= ranges[0][1] or \
                   ranges[1][0] <= field <= ranges[1][1]:
                    valid_field = True
                    break
            if not valid_field:
                valid_ticket = False
                error_rate += field
        if valid_ticket:
            good_nearby_tickets.append(ticket)
    print("Part One:")
    print("Error Rate:", error_rate)
    return good_nearby_tickets

def part_two(rules, my_ticket, nearby_tickets):
    # Iterate over each column and determine the fields to which it could map.
    # This variable stores in each index i the ith column's potential fields
    all_possible_options = []
    for col in range(len(my_ticket)):
        # To start, it could be any of the fields
        possible_options = set([x for x in rules.keys()])
        # Check this column's entry in each valid nearby ticket
        for ticket in nearby_tickets:
            field = ticket[col]
            # Check if this entry satisfies each rule. If not, then this column
            # cannot correspond to this rule
            for rule_name, ranges in rules.items():
                if ranges[0][0] <= field <= ranges[0][1] or \
                   ranges[1][0] <= field <= ranges[1][1]:
                    continue
                elif rule_name in possible_options:
                    possible_options.remove(rule_name)
        all_possible_options.append(possible_options)
    # Not all columns yet map to a unique field. But there will be at least
    # one column that already does (or else we'd have multiple possible
    # solutions). So the idea is to find that column, figure out what field
    # it must be, then remove that field as a candidate from all other columns.
    # After we finish this, there should be another column which now maps to
    # a unique field. So we repeat the process, and we keep doing this until
    # all columns map to a unique field.
    # Use this to keep track of which columns we've "locked in"
    locked_columns = set()
    while len(locked_columns) < len(all_possible_options):
        for i in range(len(all_possible_options)):
            if len(all_possible_options[i]) == 1 and \
               i not in locked_columns:
                # Found the next column to "lock in". Remove it from all other
                # columns
                locked_columns.add(i)
                element_to_remove = tuple(all_possible_options[i])[0]
                for j in range(len(all_possible_options)):
                    if (j != i) and (element_to_remove in all_possible_options[j]):
                        all_possible_options[j].remove(element_to_remove)
                break
    # Finally, go back and multiply all the "departure" fields in my ticket
    product = 1
    for i, locked_option in enumerate(all_possible_options):
        if tuple(locked_option)[0].startswith("departure"):
            product *= my_ticket[i]
    print("Part Two:")
    print("Product:", product)

def main():
    lines = []
    with open("input.txt") as f:
        lines = [line for line in f]
    # The file has three sections: rules, my ticket, and nearby tickets.
    # Since the sections are separated by blank lines, split the list of lines
    # on that condition
    sections = [list(v) for k,v in itertools.groupby(lines, key=str.isspace) if not k]
    # Store the rules as a map with kv-pairs in the following format:
    #   name: ((range_1_low, range_1_high), (range_2_low, range_2_high))
    rules = {}
    for line in sections[0]:
        parts = line.strip().split(":")
        name = parts[0]
        parts = parts[1].strip().split(" ")
        range1 = tuple([int(x) for x in parts[0].split("-")])
        range2 = tuple([int(x) for x in parts[2].split("-")])
        rules[name] = (range1, range2)
    # Store my ticket as a list of its fields
    my_ticket = [int(x) for x in sections[1][1].strip().split(",")]
    # Store nearby tickets as a 2D array (rows = tickets, cols = fields)
    nearby_tickets = []
    sections[2].pop(0) # Remove the "nearby tickets:" line
    for r in sections[2]:
        nearby_tickets.append([int(x) for x in r.strip().split(",")])
    # Call the parts of the problem
    good_nearby_tickets = part_one(rules, my_ticket, nearby_tickets)
    part_two(rules, my_ticket, good_nearby_tickets)

if __name__ == "__main__":
    main()
