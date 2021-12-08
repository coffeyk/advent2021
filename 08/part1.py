#!/usr/bin/env python

import os
from collections import defaultdict
from contextlib import contextmanager
from enum import auto
from typing import Iterable, Iterator, NamedTuple
import itertools
from util import StrEnum


class LineType(StrEnum):
    POINT = auto()
    HORIZONTAL = auto()
    VERTICAL = auto()
    OTHER = auto()


class Point(NamedTuple):
    x: int
    y: int


class Line(NamedTuple):
    p1: Point
    p2: Point

    def category(self) -> LineType:
        p1 = self.p1
        p2 = self.p2
        if p1 == p2:
            return LineType.POINT
        elif p1.x == p2.x:
            return LineType.HORIZONTAL
        elif p1.y == p2.y:
            return LineType.VERTICAL
        else:
            return LineType.OTHER

    def walk(self) -> Iterable[Point]:
        p1 = self.p1
        p2 = self.p2
        x_distance = p2.x - p1.x
        y_distance = p2.y - p1.y
        max_distance = max(abs(x_distance), abs(y_distance))

        x_step = int(x_distance / max_distance)
        y_step = int(y_distance / max_distance)

        for s in range(max_distance + 1):
            yield Point(
                x=p1.x + (x_step * s),
                y=p1.y + (y_step * s),
            )


DataType = tuple[list[str], list[str]]


@contextmanager
def get_data(fname: str) -> Iterator[Iterable[DataType]]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fpath = os.path.join(dir_path, fname)
    with open(fpath) as raw_data:
        transformed_data = (_split_line(d) for d in raw_data)
        yield transformed_data


def _split_line(line: str) -> DataType:
    # _line_to_point("0,9 -> 5,9") == Line(Point(0,9), Point(5,9))
    left, right = line.split(" | ", 2)
    return left.split(), right.split()


def process_data(data: Iterable[DataType]) -> int:
    result = sum(
        1
        for (_, values) in data
        for segments in values
        if len(segments) in (2, 3, 4, 7)
    )
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
    # input ->


if __name__ == "__main__":
    main()
