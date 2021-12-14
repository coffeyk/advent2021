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
    "(",
    "[",
    "{",
    "<",
}

CLOSE = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}

SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def process_data(data: Iterable[DataType]) -> ResultType:
    result = sum(_process_line(d) for d in data)
    # for d in data:
    #     invalid_char = _process_line(d)
    #     if invalid_char is not None:

    return result


def _process_line(data: DataType) -> int:
    stack: deque[str] = deque()
    for c in data:
        if c in OPEN:
            stack.append(c)
        else:
            other = stack.pop()
            if other != CLOSE[c]:
                return SCORE[c]
    return 0


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
