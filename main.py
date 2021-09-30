from random import choice

BOARD_SIZE = 4


class Game:
    def __init__(self, board_size):
        self.size = board_size if board_size > 2 else 4
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self._add_new_num(2)

        self.score = 0
        self.moves = 0

    # Main Method
    def run(self):
        while not self._game_over():
            print("\n\n")
            self.print_board()
            print(f"\nSCORE: {self.score}\tMOVES:{self.moves}")
            print("\nW for UP\nS for DOWN\nA for LEFT\nD for RIGHT\nQ to QUIT\n")
            move = input("> ")[0].lower()
            if move == "w":
                self._up()
            elif move == "s":
                self._down()
            elif move == "a":
                self._left()
            elif move == "d":
                self._right()
            elif move == "q":
                break
            else:
                print("Invalid move!")
                continue

            self.moves += 1
            self._add_new_num()

        print("GAME OVER!")
        print("\nFINAL BOARD\n")
        self.print_board()
        print(f"\nSCORE: {self.score}\tMOVES:{self.moves}")

    # Add new num
    def _add_new_num(self, nums: int = 1):
        for _ in range(nums):
            row, col = choice(self.empty_coords)
            self.board[row][col] = choice([2, 2, 2, 2, 2, 2, 2, 2, 4, 4])

    # Game over check

    # - Get all neighbours of a given coord
    def _get_neighbours(self, row: int, col: int):
        # Top row cases
        coords = []

        if row == 0:
            # Top left corner
            if col == 0:
                coords = [(row + 1, col), (row, col + 1)]

            # Top right corner
            elif col == self.size - 1:
                coords = [(row + 1, col), (row, col - 1)]

            # Top edge
            elif self.size - 1 > col > 0:
                coords = [(row, col - 1), (row - 1, col), (row, col + 1)]

        # Bottom row cases
        elif row == self.size - 1:
            # Bottom left corner
            if col == 0:
                coords = [(row - 1, col), (row, col + 1)]

            # Bottom right corner
            elif col == self.size - 1:
                coords = [(row - 1, col), (row, col - 1)]

            # Bottom edge
            elif self.size - 1 > col > 0:
                coords = [(row, col - 1), (row + 1, col), (row, col + 1)]

        # Middle cases
        elif self.size - 1 > col > 0 and self.size - 1 > row > 0:
            coords = [(row, col - 1), (col, row + 1), (col, row - 1), (row, col + 1)]

        return [self.board[row][col] for row, col in coords]

    # - Decide wether game over
    def _game_over(self) -> bool:
        if len(self.empty_coords) != 0:
            return False

        for row_i, row in enumerate(self.board):
            for col_i, col in enumerate(row):
                if col not in self._get_neighbours(row_i, col_i):
                    return True

        return False

    # Movements
    def _left(self):  # sourcery skip: remove-redundant-if
        for row in self.board:

            # Move nums
            for i, e in enumerate(row):
                while e != 0:
                    if i == 0:
                        break

                    if row[i - 1] == 0:
                        row[i - 1] = e
                        row[i] = 0

                    i -= 1

            # Add all the consecutives
            for i, e in enumerate(row):
                if e == 0:
                    continue

                if i < self.size - 1 and row[i + 1] == e:
                    row[i] = e + e
                    row[i + 1] = 0
                    self.score += e + e

            # Move all nums again for cleanup
            for i, e in enumerate(row):
                while e != 0:
                    if i == 0:
                        break

                    if row[i - 1] == 0:
                        row[i - 1] = e
                        row[i] = 0

                    i -= 1

    def _right(self):
        self._rotate(2)
        self._left()
        self._rotate(2)

    def _up(self):
        self._rotate(3)
        self._left()
        self._rotate()

    def _down(self):
        self._rotate()
        self._left()
        self._rotate(3)

    # Get empty/[0] coords
    @property
    def empty_coords(self) -> list[tuple[int, int]]:
        coords = []
        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                if col == 0:
                    coords.append((i, j))

        return coords

    # Rotate the board clockwise
    def _rotate(self, rot: int = 1):
        for _ in range(rot):
            temp_board = [[] for _ in range(self.size)]
            for row in self.board:
                for j, e in enumerate(row):
                    temp_board[j].append(e)

            for row in temp_board:
                row.reverse()

            self.board = temp_board

    # Print Board
    def print_board(self):
        for row in self.board:
            for num in row:
                if num == 0:
                    num = "_"
                print(f"{num}\t", end="")

            print("\n")


def main():
    game = Game(4)
    game.run()


if __name__ == "__main__":
    main()
