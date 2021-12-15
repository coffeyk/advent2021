#!/usr/bin/env python

import os
from contextlib import contextmanager
from dataclasses import dataclass
from util import PriorityQueue

from typing import Iterable, Iterator, NamedTuple


class DataPoint(NamedTuple):
    value: int
    row_id: int
    col_id: int


Grid = list[list[DataPoint]]


@dataclass
class DataType:
    data: Grid

    def neighbors(self, p: DataPoint) -> Iterable[DataPoint]:
        if p.col_id > 0:
            yield self.data[p.row_id][p.col_id - 1]

        if p.col_id + 1 < len(self.data[p.row_id]):
            yield self.data[p.row_id][p.col_id + 1]

        if p.row_id > 0:
            yield self.data[p.row_id - 1][p.col_id]

        if p.row_id + 1 < len(self.data):
            yield self.data[p.row_id + 1][p.col_id]

    def walk(self) -> int:
        initial_node = self.data[0][0]
        visited: set[DataPoint] = set()
        distance: dict[DataPoint, int] = {initial_node: 0}
        pq = PriorityQueue[DataPoint]()
        pq.add_task(initial_node, distance[initial_node])

        while True:
            current_node = pq.pop_task()
            print(current_node)
            current_distance = distance[current_node]

            if current_node.row_id == current_node.col_id == len(self.data) - 1:
                return current_distance

            for neighbor in self.neighbors(current_node):
                if neighbor not in visited:
                    try:
                        if distance[neighbor] < current_distance + neighbor.value:
                            continue
                    except KeyError:
                        # neighbor never visited
                        pass

                    # current_path is closer or first visit
                    try:
                        pq.remove_task(neighbor)
                    except KeyError:
                        # neighbor not in queue yet
                        pass
                    new_distance = current_distance + neighbor.value
                    distance[neighbor] = new_distance
                    pq.add_task(neighbor, new_distance)

            visited.add(current_node)

    def __str__(self) -> str:
        return "\n".join("".join(str(p.value) for p in row) for row in self.data)


ResultType = int


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


def process_data(data: DataType) -> ResultType:
    return data.walk()


def render_result(result: ResultType):
    print(result)


def main():
    fname = "input.txt"
    # fname = "sample.txt"
    # fname = "big_data.txt"
    with get_data(fname) as data:
        result = process_data(data)
        render_result(result)
    # sample -> 40
    # input -> 595


if __name__ == "__main__":
    main()
