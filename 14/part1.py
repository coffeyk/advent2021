#!/usr/bin/env python

import os
from contextlib import contextmanager
from typing import Counter, Iterable, Iterator
from util import pairwise

TableType = dict[tuple[str, str], str]
DataType = tuple[str, TableType]
ResultType = str


@contextmanager
def get_data(fname: str) -> Iterator[DataType]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fpath = os.path.join(dir_path, fname)
    with open(fpath) as raw_data:
        pattern = raw_data.readline().strip()
        table: TableType = dict()
        for raw_mapping in raw_data:

            raw_left, _, raw_right = raw_mapping.strip().partition(" -> ")
            if raw_left:
                key = (raw_left[0], raw_left[1])
                table[key] = raw_right
        yield pattern, table


def _step(pattern: str, table: TableType) -> Iterable[str]:
    for cur, prev in pairwise(pattern):
        if prev is not None:
            try:
                yield table[(prev, cur)]
            except KeyError:
                pass
        yield cur


def step(pattern: str, table: TableType) -> str:
    return "".join(_step(pattern, table))


def process_data(data: DataType) -> ResultType:
    pattern, table = data
    result = pattern
    for _ in range(10):
        result = step(result, table)
    return result


def render_result(result: ResultType):
    print(score(result))
    # print(result)


def score(result: str) -> int:
    counts = Counter(result)
    first, *_, last = counts.most_common()

    return first[1] - last[1]


def main():
    # fname = "sample.txt"
    # fname = "small_sample.txt"
    fname = "input.txt"
    # fname = "big_data.txt"
    with get_data(fname) as data:
        result = process_data(data)
        render_result(result)
    # sample -> 1588
    # small_sample -> 517
    # input -> 2657


if __name__ == "__main__":
    main()
