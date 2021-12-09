#!/usr/bin/env python

import operator
import os
from collections import deque
from contextlib import contextmanager
from dataclasses import dataclass
from functools import reduce
from typing import Iterable, Iterator, NamedTuple, Set


class DataPoint(NamedTuple):
    value: int
    row_id: int
    col_id: int


Grid = list[list[DataPoint]]


@dataclass
class DataType:
    data: Grid

    def region_size(self, seed: DataPoint) -> int:
        seen: Set[DataPoint] = set([seed])
        frontier = deque(seen)
        while frontier:
            point = frontier.pop()
            for neighbor in self.neighbors(point):
                if neighbor in seen:
                    continue
                if neighbor.value == 9:
                    continue
                if neighbor.value > point.value:
                    seen.add(neighbor)
                    frontier.append(neighbor)
        return len(seen)

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
    region_sizes: list[int] = []

    region_sizes = [data.region_size(local_min) for local_min in data.local_minimums()]

    sorted_sizes = sorted(region_sizes)

    top_3 = sorted_sizes[-3:]
    print(top_3)
    return reduce(operator.__mul__, top_3, 1)


def render_result(result: int):
    print(result)


def main():
    fname = "input.txt"
    # fname = "sample.txt"
    # fname = "big_data.txt"
    with get_data(fname) as data:
        result = process_data(data)
        render_result(result)
    # sample -> 1134
    # input -> 899392


if __name__ == "__main__":
    main()
