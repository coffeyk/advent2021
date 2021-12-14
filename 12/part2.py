#!/usr/bin/env python

import os
from collections import defaultdict, deque
from contextlib import contextmanager
from copy import copy
from dataclasses import dataclass
from typing import Iterator, NamedTuple

START = "start"
END = "end"


class CavePath(NamedTuple):
    nodes: list[str]
    spare_cave: bool = True


@dataclass
class Graph:
    data: dict[str, list[str]]

    def add_edge(self, edge: list[str]) -> None:
        n1, n2 = edge[:2]
        self.data[n1].append(n2)
        self.data[n2].append(n1)

    def walk(self) -> Iterator[list[str]]:

        frontier = deque([CavePath([START])])

        while frontier:
            path = frontier.popleft()
            node = path.nodes[-1]

            neighbors = self.data[node]

            for neighbor in neighbors:
                if neighbor == START:
                    # Can't go back to start
                    continue

                if neighbor == END:
                    yield path.nodes
                    continue

                if neighbor in path.nodes and neighbor.islower():
                    if not path.spare_cave:
                        # Can't revisit a small cave
                        continue

                    # Could revisit the smaller cave, so keep going
                    new_nodes = copy(path.nodes)
                    new_nodes.append(neighbor)

                    new_path = path._replace(nodes=new_nodes, spare_cave=False)
                    frontier.append(new_path)

                else:
                    # Not a node in the path or is a big cave
                    new_nodes = copy(path.nodes)
                    new_nodes.append(neighbor)

                    new_path = path._replace(nodes=new_nodes)
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
    paths = list(data.walk())
    # paths = set(tuple(nodes) for nodes in data.walk())
    # print(paths)
    return len(paths)


def render_result(result: ResultType):
    print(result)


def main():
    fname = "input.txt"
    # fname = "sample.txt"
    # fname = "big_data.txt"
    with get_data(fname) as data:
        result = process_data(data)
        render_result(result)
    # sample -> 36
    # input -> 84870


if __name__ == "__main__":
    main()
