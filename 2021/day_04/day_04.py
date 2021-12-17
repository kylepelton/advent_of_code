class Board:
    def __init__(self, rows):
        self.grid = {}
        for row_idx, row in enumerate(rows):
            row = row.split()
            for col_idx, num in enumerate(row):
                self.grid[int(num)] = (row_idx, col_idx)

    def has_number(self, num):
        return num in self.grid

    def mark_number(self, num):
        pass

    def has_won(self):
        pass


def main():
    lines = []
    with open("input.txt") as file:
        lines = file.readlines()
    numbers = [int(num) for num in lines[0].strip().split(",")]
    boards = []

    rows = []
    for i in range(2, len(lines)):
        line = lines[i].strip()
        if len(line) == 0:
            boards.append(Board(rows))
            rows = []
            continue
        rows.append(line)



if __name__ == "__main__":
    main()
