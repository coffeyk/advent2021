#!/usr/bin/env python

import os
from collections import deque
from contextlib import contextmanager
from typing import Iterable, Iterator

DataType = str
ResultType = int


@contextmanager
def get_data(fname: str) -> Iterator[Iterable[DataType]]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fpath = os.path.join(dir_path, fname)
    with open(fpath) as raw_data:
        yield (t.strip() for t in raw_data)


OPEN = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

CLOSE = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}

SCORE = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def process_data(data: Iterable[DataType]) -> ResultType:
    results = (_process_line(d) for d in data)
    results = [r for r in results if r]
    results = sorted(results)

    return results[len(results) // 2]


def _process_line(data: DataType) -> int:
    stack: deque[str] = deque()
    for c in data:
        if c in OPEN:
            stack.append(c)
        else:
            other = stack.pop()
            if other != CLOSE[c]:
                return 0

    result = 0
    while stack:
        c = stack.pop()
        needed = OPEN[c]
        result = (result * 5) + SCORE[needed]

    return result


def render_result(result: ResultType):
    print(result)


def main():
    fname = "input.txt"
    # fname = "sample.txt"
    # fname = "big_data.txt"
    with get_data(fname) as data:
        result = process_data(data)
        render_result(result)
    # sample ->
    # input ->


if __name__ == "__main__":
    main()
