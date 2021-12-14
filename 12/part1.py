#!/usr/bin/env python

import os
from collections import defaultdict, deque
from contextlib import contextmanager
from copy import copy
from dataclasses import dataclass
from typing import Iterator

START = "start"
END = "end"


@dataclass
class Graph:
    data: dict[str, list[str]]

    def add_edge(self, edge: list[str]) -> None:
        n1, n2 = edge[:2]
        self.data[n1].append(n2)
        self.data[n2].append(n1)

    def walk(self) -> Iterator[list[str]]:

        frontier = deque([[START]])

        while frontier:
            path = frontier.popleft()
            node = path[-1]

            neighbors = self.data[node]

            for neighbor in neighbors:
                if neighbor == END:
                    yield path
                    continue
                if neighbor in path and neighbor.islower():
                    # Can't revisit a small cave
                    continue
                else:
                    new_path = copy(path)
                    new_path.append(neighbor)
                    frontier.append(new_path)


DataType = Graph
ResultType = int


@contextmanager
def get_data(fname: str) -> Iterator[DataType]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fpath = os.path.join(dir_path, fname)
    with open(fpath) as raw_data:
        graph = Graph(defaultdict(list))
        for raw in raw_data:
            path = raw.strip().split("-")
            graph.add_edge(path)
        yield graph


def process_data(data: DataType) -> ResultType:
    return len(list(data.walk()))


def render_result(result: ResultType):
    print(result)


def main():
    fname = "input.txt"
    # fname = "sample.txt"
    # fname = "big_data.txt"
    with get_data(fname) as data:
        result = process_data(data)
        render_result(result)
    # sample -> 10
    # input ->


if __name__ == "__main__":
    main()
