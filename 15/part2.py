#!/usr/bin/env python

import os
from collections import deque
from contextlib import contextmanager
from dataclasses import dataclass
from util import PriorityQueue

# from io import TextIOWrapper
from typing import Iterable, Iterator, NamedTuple, Set


class DataPoint(NamedTuple):
    value: int
    row_id: int
    col_id: int

    # def __hash__(self) -> int:
    #     return hash((self.row_id, self.col_id))


Grid = list[list[DataPoint]]


@dataclass
class DataType:
    data: Grid

    @property
    def size(self) -> int:
        return len(self.data) * 5

    def __getitem__(self, row_col: tuple[int, int]) -> DataPoint:
        # Fake the giant grid by scaling up on lookups
        row_id, col_id = row_col
        scaled_row = row_id % len(self.data)
        scaled_col = col_id % len(self.data)
        base_point = self.data[scaled_row][scaled_col]

        scale = (row_id // len(self.data)) + (col_id // len(self.data))

        if not scale:
            return base_point

        new_value = base_point.value + scale
        if new_value > 9:
            new_value = new_value - 9

        return DataPoint(new_value, row_id, col_id)

    def neighbors(self, p: DataPoint) -> Iterable[DataPoint]:
        if p.col_id > 0:
            yield self[p.row_id, p.col_id - 1]

        if p.col_id + 1 < self.size:
            yield self[p.row_id, p.col_id + 1]

        if p.row_id > 0:
            yield self[p.row_id - 1, p.col_id]

        if p.row_id + 1 < self.size:
            yield self[p.row_id + 1, p.col_id]

    def walk(self) -> int:
        """Dijkstra's algorithm"""
        initial_node = self[0, 0]
        # Track the DataPoints we've already processed
        visited: set[DataPoint] = set()
        # Track the shortest distances from the initial_node to a DataPoint
        distance: dict[DataPoint, int] = {initial_node: 0}
        # Track the DataPoints with the shortest distance
        pq = PriorityQueue[DataPoint]()
        # Bootstrap the queue with our initial_node
        pq.add_task(initial_node, distance[initial_node])

        while True:
            current_node = pq.pop_task()
            # print(current_node)
            current_distance = distance[current_node]

            if current_node.row_id == current_node.col_id == self.size - 1:
                return current_distance

            for neighbor in self.neighbors(current_node):
                if neighbor not in visited:
                    try:
                        if distance[neighbor] < current_distance + neighbor.value:
                            # New path to neighbor is longer than the existing path
                            continue
                    except KeyError:
                        # neighbor never visited
                        pass

                    # current_node is closer or first visit
                    # Upsert the neighbor distance in the priority queue
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
    # sample -> 315
    # input -> 2914


if __name__ == "__main__":
    main()
