#!/usr/bin/env python

import functools
import os
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator, NamedTuple


class Point(NamedTuple):
    row_id: int
    col_id: int

    def y_fold_helper(self, val: int) -> "Point":
        distance = self.row_id - val
        return self._replace(row_id=val - distance)

    def x_fold_helper(self, val: int) -> "Point":
        distance = self.col_id - val
        return self._replace(col_id=val - distance)


class Instruction(NamedTuple):
    axis: str
    value: int


def y_axis_check(val: int, point: Point) -> bool:
    return bool(point.row_id > val)


def x_axis_check(val: int, point: Point) -> bool:
    return bool(point.col_id > val)


@dataclass
class Paper:
    grid: set[Point]

    def add(self, p: Point) -> None:
        self.grid.add(p)

    def fold(self, instruction: Instruction) -> None:
        new_grid: set[Point] = set()

        if instruction.axis == "y":
            axis_check = functools.partial(
                y_axis_check,
                val=instruction.value,
            )
            fold_helper = functools.partial(
                Point.y_fold_helper,
                val=instruction.value,
            )
        else:
            axis_check = functools.partial(
                x_axis_check,
                val=instruction.value,
            )
            fold_helper = functools.partial(
                Point.x_fold_helper,
                val=instruction.value,
            )
        for point in self.grid:
            if not axis_check(point=point):
                new_grid.add(point)
            else:
                new_point = fold_helper(point)
                # print(f"{point}->{new_point}")
                new_grid.add(new_point)
        self.grid = new_grid

    def render(self):
        max_row = max(p.row_id for p in self.grid)
        max_col = max(p.col_id for p in self.grid)
        for r in range(max_row + 1):
            for c in range(max_col + 1):
                if Point(r, c) in self.grid:
                    print("#", end="")
                else:
                    print(".", end="")
            print()


DataType = tuple[Paper, list[Instruction]]
ResultType = int


@contextmanager
def get_data(fname: str) -> Iterator[DataType]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fpath = os.path.join(dir_path, fname)
    with open(fpath) as raw_data:
        paper = Paper(grid=set())
        # Points
        for line in raw_data:
            if not line.strip():
                break
            x, y = (int(v) for v in line.strip().split(","))
            paper.add(Point(y, x))

        # instructions
        instructions = [
            Instruction(line[11], int(line.split("=")[1])) for line in raw_data
        ]

        yield paper, instructions


def process_data(data: DataType) -> ResultType:
    paper, instructions = data
    # print(paper.grid)
    for i in instructions:
        paper.fold(i)

    # pprint(sorted(paper.grid))
    paper.render()
    return len(paper.grid)


def render_result(result: ResultType):
    print(result)


def main():
    fname = "input.txt"
    # fname = "sample.txt"
    # fname = "big_data.txt"
    with get_data(fname) as data:
        result = process_data(data)
        render_result(result)
    # sample -> O
    # input -> UFRZKAUZ


if __name__ == "__main__":
    main()
