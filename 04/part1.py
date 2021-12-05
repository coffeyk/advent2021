import os

from typing import Iterable, NamedTuple
from dataclasses import dataclass

BOARD_SIZE = 5

Line = list[int]


def wincons(board: list[int]) -> Iterable[Line]:
    """Iterate over all the possible rows and columns for a given board.

    board is a 1d reperesentation of a BOARD_SIZE*BOARD_SIZE grid.
    """
    # Rows
    for i in range(BOARD_SIZE):
        yield board[i * 5 : (i * 5) + BOARD_SIZE]

    # Columns
    for i in range(BOARD_SIZE):
        yield board[i::BOARD_SIZE]


def _call_order(numbers: list[int]) -> list[int]:
    """Reverse lookup of number to index in the given list"""
    call_order = [len(numbers)] * 100
    for (i, number) in enumerate(numbers):
        call_order[number] = i

    return call_order


class BingoNumbers(NamedTuple):
    calls: list[int]
    calls_lookup: list[int]

    @classmethod
    def from_raw(cls, calls: list[int]) -> "BingoNumbers":
        return BingoNumbers(
            calls=calls,
            calls_lookup=_call_order(calls),
        )


@dataclass(order=True)
class BingoBoard:
    board: list[int]
    bingo_numbers: BingoNumbers

    _board_order: list[int] | None = None
    _win_turn: int | None = None
    _score: int | None = None

    @property
    def score(self) -> int:
        """The score of the board can now be calculated.
        Start by finding the sum of all unmarked numbers on that board;
        in this case, the sum is 188. Then, multiply that sum by the number
        that was just called when the board won, 24, to get the final score, 188 * 24 = 4512."""
        if self._score is None:
            total = sum(
                spot
                for spot, order in zip(self.board, self.board_order)
                if order > self.win_turn
            )
            winning_number = self.bingo_numbers.calls[self.win_turn]
            self._score = winning_number * total
        return self._score

    @property
    def board_order(self) -> list[int]:
        """The board transformed to where the spot falls in the call order."""
        if self._board_order is None:
            self._board_order = [self.bingo_numbers.calls_lookup[n] for n in self.board]

        return self._board_order

    @property
    def win_turn(self) -> int:
        """The turn the board would first have a filled line."""
        if self._win_turn is None:
            earliest_turn = len(self.bingo_numbers.calls_lookup)

            # Look at every row and column of the board to see which one is finished first
            for line in wincons(self.board_order):
                # A given line would win when the last spot is filled
                line_turn = max(line)
                # Keep the earliest winning turn
                earliest_turn = min(earliest_turn, line_turn)
            self._win_turn = earliest_turn

        return self._win_turn


def get_data(fname: str) -> list[BingoBoard]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fpath = os.path.join(dir_path, fname)
    with open(fpath) as raw_data:
        # trim trailing newline?
        # numbers, boards
        raw_numbers = raw_data.readline()
        numbers = [int(r) for r in raw_numbers.split(",")]
        bingo_numbers = BingoNumbers.from_raw(numbers)

        # Skip a line
        raw_data.readline()

        boards: list[BingoBoard] = list()
        # Boards are 5 lines of 5 numbers, with a blank in between boards
        data: list[int] = list()
        for line in raw_data:
            if line.strip():
                data.extend([int(x) for x in line.split()])
            else:
                boards.append(BingoBoard(data, bingo_numbers))
                # Reset data for next board
                data = list()
        if data:
            boards.append(BingoBoard(data, bingo_numbers))

        print(len(boards))
        return boards


def process_data(boards: list[BingoBoard]) -> BingoBoard:
    """process_data finds the board that wins on the earliest turn."""
    board_winturns = ((board.win_turn, board) for board in boards)
    _, best_board = min(board_winturns)

    return best_board


def render_result(board: BingoBoard) -> None:
    print("WINNER:")
    print(f"{board=}")
    print(f"{board.score=}")


def main():
    fname = "./input.txt"
    # fname = "sample.txt"
    boards = get_data(fname)
    winning_board = process_data(boards)
    render_result(winning_board)
    # board.score=2745


if __name__ == "__main__":
    main()
