from collections import Counter

def part_one():
    # All encountered ingredients
    all_ingredients = set()
    # Number of appearances for each ingredient
    ingredients_ctr = Counter()
    # Maps each allergen to its possible ingredients
    allergen_options = {}
    with open("input.txt") as f:
        for line in f:
            # Divide each line into its ingredients and known allergies
            line_ingredients, line_allergies = line.split("(")
            line_ingredients = line_ingredients.strip().split()
            line_allergies = line_allergies.strip().replace(")", "").replace(",", "").split()[1:]
            # Update our set of all encountered ingredients
            all_ingredients.update(line_ingredients)
            # Update the number of occurrences of each ingredient
            for ingredient in line_ingredients:
                ingredients_ctr[ingredient] += 1
            # For each allergen in this line, update its possible causing
            # ingredients. Basically, this means the first time we see an allergen,
            # we initialize a set of all that line's ingredients. For every
            # subsequent line containing that allergen, we take the intersection
            # of its running ingredients set and this line's ingredients. Since
            # an ingredient i can only possibly cause an allergen a if it appears
            # in all the same lines as a, this should give all possible causing
            # ingredients.
            for allergen in line_allergies:
                if allergen in allergen_options:
                    allergen_options[allergen].intersection_update(line_ingredients)
                else:
                    allergen_options[allergen] = set(line_ingredients)
        # The set of possible ingredients is the union of all allergens'
        # possible ingredients
        possible_ingredients = set.union(*allergen_options.values())
        # The set of impossible ingredients is just the difference between
        # the set of all ingredients and the set of possible ones.
        impossible_ingredients = all_ingredients - possible_ingredients
        print("Part One:")
        print("Number of Impossible Ingredients Appearances:", \
              sum(ingredients_ctr[x] for x in impossible_ingredients))
        # Return the mapping of allergen options for use in part 2
        return allergen_options

def part_two(allergen_options):
    # Maps allergens to their confirmed causing ingredient
    confirmed_options = {}
    # Build up this mapping. Basically, find an allergen that can only have
    # one causing ingredient and "confirm" it. Remove this ingredient from
    # the remaining allergens' options. Then keep looping through until all
    # the allergens have only one ingredient left
    while len(confirmed_options) < len(allergen_options):
        for allergen in allergen_options:
            if allergen not in confirmed_options:
                allergen_options[allergen].difference_update(confirmed_options.values())
                if len(allergen_options[allergen]) == 1:
                    confirmed_options[allergen] = allergen_options[allergen].pop()
    # Build up the "canonical dangerous ingredients list" by sorting the allergens
    # and joining their ingredients with commas.
    cdi_list = ",".join(confirmed_options[allergen] for allergen in sorted(confirmed_options))
    print("Part Two:")
    print("Canonical Dangerous Ingredients List:", cdi_list)

def main():
    allergen_options = part_one()
    part_two(allergen_options)

if __name__ == "__main__":
    main()
