#!/usr/bin/env python

import os
from collections import defaultdict
from contextlib import contextmanager
from enum import auto
from typing import Iterable, Iterator, NamedTuple

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


@contextmanager
def get_data(fname: str) -> Iterator[Iterable[Line]]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fpath = os.path.join(dir_path, fname)
    with open(fpath) as raw_data:
        transformed_data = (_line_to_point(d) for d in raw_data)
        yield transformed_data


def _line_to_point(line: str) -> Line:
    # _line_to_point("0,9 -> 5,9") == Line(Point(0,9), Point(5,9))
    raw_points = line.split(" -> ", maxsplit=1)
    raw_point_values = (rp.split(",") for rp in raw_points)
    points = [Point(int(x), int(y)) for (x, y) in raw_point_values]
    return Line(points[0], points[1])


def process_data(data: Iterable[Line]) -> int:
    line_filter = (LineType.HORIZONTAL, LineType.VERTICAL)
    valid_lines = (l for l in data if l.category() in line_filter)

    grid: dict[Point, int] = defaultdict(int)
    for l in valid_lines:
        for p in l.walk():
            grid[p] += 1

    result = 0
    for count in grid.values():
        if count > 1:
            result += 1

    return result


def render_result(result: int):
    print(result)


def main():
    fname = "input.txt"
    # fname = "sample.txt"
    with get_data(fname) as data:
        result = process_data(data)
        render_result(result)


if __name__ == "__main__":
    main()
