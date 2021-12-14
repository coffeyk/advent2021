#!/usr/bin/env python

import os
from collections import deque
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterable, Iterator, Set


@dataclass()
class DataPoint:
    value: int
    row_id: int
    col_id: int

    def __hash__(self) -> int:
        return hash((self.row_id, self.col_id))


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

    def all_neighbors(self, p: DataPoint) -> Iterable[DataPoint]:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                row_id = p.row_id + i
                col_id = p.col_id + j
                if row_id < 0 or row_id >= len(self.data):
                    continue
                if col_id < 0 or col_id >= len(self.data):
                    continue
                yield self.data[row_id][col_id]

    def step(self) -> int:
        seen: set[DataPoint] = set()
        frontier: deque[DataPoint] = deque()
        for row in self.data:
            for seed in row:
                frontier.append(seed)
                while frontier:
                    point = frontier.pop()
                    point.value += 1
                    if point.value > 9 and point not in seen:
                        seen.add(point)
                        for neighbor in self.all_neighbors(point):
                            # if neighbor in seen:
                            #     continue
                            frontier.append(neighbor)

        for point in seen:
            point.value = 0

        return len(seen)

    def __str__(self) -> str:
        return "\n".join("".join(str(p.value) for p in row) for row in self.data)


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
    r = sum(data.step() for _ in range(100))
    # r = data.step()
    print(data)
    return r
    # region_sizes: list[int] = []

    # region_sizes = [data.region_size(local_min) for local_min in data.local_minimums()]

    # sorted_sizes = sorted(region_sizes)

    # top_3 = sorted_sizes[-3:]
    # print(top_3)
    # return reduce(operator.__mul__, top_3, 1)


def render_result(result: int):
    print(result)


def main():
    fname = "input.txt"
    # fname = "sample.txt"
    # fname = "big_data.txt"
    with get_data(fname) as data:
        result = process_data(data)
        render_result(result)
    # sample -> 1656
    # input ->


if __name__ == "__main__":
    main()
