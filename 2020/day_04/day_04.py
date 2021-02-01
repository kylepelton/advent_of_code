import string

def part_one(passports):
    required_fields = set(("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"))
    count = 0
    for passport in passports:
        if required_fields.issubset(passport):
            count += 1
    print("Part One:")
    print("Number of Valid Passports:", count)

def part_two(passports):
    count = 0
    for passport in passports:
        # Birth Year - 4 digit number, between 1920-2020
        if not 'byr' in passport or not passport['byr'].isdigit() or \
           not 1920 <= int(passport['byr']) <= 2002:
           continue
        # Birth Year - 4 digit number, between 2010-2020
        if not 'iyr' in passport or not passport['iyr'].isdigit() or \
           not 2010 <= int(passport['iyr']) <= 2020:
           continue
        # Expiration Year - 4 digit number, between 2020-2030
        if not 'eyr' in passport or not passport['eyr'].isdigit() or \
           not 2020 <= int(passport['eyr']) <= 2030:
           continue
        # Height - Number followed by either cm or in. If cm, number must be
        # between 150 and 193. If in, number must be between 59 and 76
        if not 'hgt' in passport or (len(passport['hgt']) < 3) or \
           ((passport['hgt'][-2:] != "cm") and (passport['hgt'][-2:] != "in")) or \
           not passport['hgt'][:-2].isdigit() or \
           ((passport['hgt'][-2:] == "cm") and not (150 <= int(passport['hgt'][:-2]) <= 193)) or \
           ((passport['hgt'][-2:] == "in") and not (59 <= int(passport['hgt'][:-2]) <= 76)):
           continue
        # Hair Color - #XXXXXX, where X is hexadecimal
        if not 'hcl' in passport or (len(passport['hcl']) != 7) or \
           (passport['hcl'][0] != "#") or \
           not set(passport['hcl'][1:]).issubset(string.hexdigits):
           continue
        # Eye Color - amb blu brn gry grn hzl oth
        if not 'ecl' in passport or \
           ((passport['ecl'] != "amb") and (passport['ecl'] != "blu") and \
           (passport['ecl'] != "brn") and (passport['ecl'] != "gry") and \
           (passport['ecl'] != "grn") and (passport['ecl'] != "hzl") and \
           (passport['ecl'] != "oth")):
           continue
        # Passport ID - 9 digit number, including leading zeros
        if not 'pid' in passport or (len(passport['pid']) != 9) or \
           not passport['pid'].isdigit():
           continue
        # If passes all the tests, then it's a valid passport
        count += 1
    print("Part Two:")
    print("Number of Valid Passports:", count)

def main():
    passports = []
    with open("input.txt") as f:
        # Passport entries take up multiple lines and can have multiple kv-pairs
        # on each line. So we take the following approach to parse them in:
        passport = {}
        for line in f:
            if line == "\n":
                passports.append(passport)
                passport = {}
            else:
                kv_pairs = line.rstrip().split()
                for kv_pair in kv_pairs:
                    k, v = kv_pair.split(":")
                    passport[k] = v
        # Add the last passport (since the file doesn't end with a newline)
        passports.append(passport)
    # Run the parts
    part_one(passports)
    part_two(passports)

if __name__ == "__main__":
    main()
