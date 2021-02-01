def part_one(public_keys):
    # Arbitrarily assign the public keys to the card and the door
    card_key, door_key = public_keys
    # First figure out the card loop size by transforming 7 loop_size times
    # until it equals the card's public key
    value = 1
    card_loop_size = 1
    while True:
        value *= 7
        value %= 20201227
        if value == card_key:
            break
        card_loop_size += 1
    # Transform door's public key according to the card's loop size. This
    # generates the encryption key
    value = 1
    for i in range(card_loop_size):
        value *= door_key
        value %= 20201227
    print("Part One:")
    print("Encryption Key:", value)

def main():
    # NOTE: There's only one part to this problem
    public_keys = [16616892, 14505727]
    part_one(public_keys)

if __name__ == "__main__":
    main()
