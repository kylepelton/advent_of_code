def initialize_game():
    # Construct the initial decks for each player
    p1, p2 = [], []
    with open("input.txt") as f:
        player = p1
        for line in f:
            if line.isspace():
                continue
            elif line.startswith("Player"):
                if line.strip() == "Player 2:":
                    player = p2
            else:
                player.append(int(line.strip()))
    return (p1, p2)

def part_one():
    # Play until one player has all the cards
    p1, p2 = initialize_game()
    while p1 and p2:
        # Draw the top card in each player's deck
        p1_card = p1.pop(0)
        p2_card = p2.pop(0)
        # The winner of the round is the player with the higher card. The winner
        # puts both cards at the bottom of their deck (winning card first)
        if p1_card > p2_card:
            p1.append(p1_card)
            p1.append(p2_card)
        else:
            p2.append(p2_card)
            p2.append(p1_card)
    # The winning score is calculated by multiplying 1 * bottom card +
    # 2 * penultimate card + ... + N * top card
    winner = p1 if p1 else p2
    print("Part One:")
    print("Winning Score:", sum((len(winner) - i) * card for i, card in enumerate(winner)))

def part_two():
    def play_game(p1, p2):
        # Plays a recursive combat game given an initial p1 and p2. Returns
        # the winning number and its corresponding deck at the end of the game/
        # The winning number is used in recursive calls, while the winning
        # deck is used at the end to calculate the winning score.
        prev_rounds = set()
        while p1 and p2:
            # Check if this partitioning/arrangement of cards has been seen
            # before in this game. If so, then Player 1 wins. We store each
            # round as "[..., ..., ...] vs [..., ..., ...]" strings so they
            # are uniquely identifiable.
            round = str(p1) + " vs " + str(p2)
            if round in prev_rounds:
                return (1, p1)
            prev_rounds.add(round)
            # Otherwise we play the game. Each player draws their top card.
            p1_card = p1.pop(0)
            p2_card = p2.pop(0)
            winnum = None
            winner = None
            if len(p1) >= p1_card and len(p2) >= p2_card:
                # If each player has enough cards to play a recursive game,
                # the winner is the winner of the recursive game.
                winnum, winner = play_game(p1[:p1_card], p2[:p2_card])
            else:
                # Othewise, the winner is the player with the higher card
                winnum, winner = (1, p1) if (p1_card > p2_card) else (2, p2)
            # Update the winner's deck
            if winnum == 1:
                p1.append(p1_card)
                p1.append(p2_card)
            else:
                p2.append(p2_card)
                p2.append(p1_card)
        # Once one player has no cards left, the other player wins
        return (1, p1) if p1 else (2, p2)

    # Play the game and return the winner
    p1, p2 = initialize_game()
    winnum, winner = play_game(p1, p2)
    print("Part Two:")
    print("Winning Score:", sum((len(winner) - i) * card for i, card in enumerate(winner)))

def main():
    part_one()
    part_two()

if __name__ == "__main__":
    main()
