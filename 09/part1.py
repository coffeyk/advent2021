#!/usr/bin/env python

import os
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterable, Iterator, NamedTuple


class DataPoint(NamedTuple):
    value: int
    row_id: int
    col_id: int


Grid = list[list[DataPoint]]


@dataclass
class DataType:
    data: Grid

    def local_minimums(self) -> Iterable[DataPoint]:
        for row in self.data:
            for point in row:
                for neighbor in self.neighbors(point):
                    if neighbor.value <= point.value:
                        break
                else:
                    yield point

    def neighbors(self, p: DataPoint) -> Iterable[DataPoint]:
        if p.col_id > 0:
            yield self.data[p.row_id][p.col_id - 1]

        if p.col_id + 1 < len(self.data[p.row_id]):
            yield self.data[p.row_id][p.col_id + 1]

        if p.row_id > 0:
            yield self.data[p.row_id - 1][p.col_id]

        if p.row_id + 1 < len(self.data):
            yield self.data[p.row_id + 1][p.col_id]


@contextmanager
def get_data(fname: str) -> Iterator[DataType]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fpath = os.path.join(dir_path, fname)
    with open(fpath) as raw_data:

        result = [
            [
                DataPoint(
                    value=int(c),
                    row_id=row_id,
                    col_id=col_id,
                )
                for col_id, c in enumerate(line.strip())
            ]
            for row_id, line in enumerate(raw_data)
        ]

        yield DataType(data=result)


def process_data(data: DataType) -> int:
    result = sum(p.value + 1 for p in data.local_minimums())
    return result


def render_result(result: int):
    print(result)


def main():
    fname = "input.txt"
    # fname = "sample.txt"
    # fname = "big_data.txt"
    with get_data(fname) as data:
        result = process_data(data)
        render_result(result)
    # sample -> 26
    # input -> 570


if __name__ == "__main__":
    main()
