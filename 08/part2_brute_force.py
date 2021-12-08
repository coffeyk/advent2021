#!/usr/bin/env python

from functools import reduce
import itertools
import os
from contextlib import contextmanager
from enum import IntFlag, auto
from typing import Iterable, Iterator
import operator


#   aaaa
#  b    c
#  b    c
#   dddd
#  e    f
#  e    f
#   gggg


class Segments(IntFlag):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()
    G = auto()

    @staticmethod
    def combine(segments: Iterable["Segments"]) -> "Segments":
        return reduce(operator.or_, segments)


ALL_SEGMENTS = [
    Segments.A,
    Segments.B,
    Segments.C,
    Segments.D,
    Segments.E,
    Segments.F,
    Segments.G,
]

NUMBER_SEGMENTS = {
    1: Segments.C | Segments.F,
    2: Segments.A | Segments.C | Segments.D | Segments.E | Segments.G,
    3: Segments.A | Segments.C | Segments.D | Segments.F | Segments.G,
    4: Segments.B | Segments.C | Segments.D | Segments.F,
    5: Segments.A | Segments.B | Segments.D | Segments.F | Segments.G,
    6: Segments.A | Segments.B | Segments.D | Segments.E | Segments.F | Segments.G,
    7: Segments.A | Segments.C | Segments.F,
    8: (
        Segments.A
        | Segments.B
        | Segments.C
        | Segments.D
        | Segments.E
        | Segments.F
        | Segments.G
    ),
    9: Segments.A | Segments.B | Segments.C | Segments.D | Segments.F | Segments.G,
    0: Segments.A | Segments.B | Segments.C | Segments.E | Segments.F | Segments.G,
}

SEGMENT_NUMBERS = {v: k for k, v in NUMBER_SEGMENTS.items()}

VALID_SEGMENT_COMBINATIONS = set(NUMBER_SEGMENTS.values())

DataType = tuple[list[str], list[str]]


@contextmanager
def get_data(fname: str) -> Iterator[Iterable[DataType]]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fpath = os.path.join(dir_path, fname)
    with open(fpath) as raw_data:
        transformed_data = (_split_line(d) for d in raw_data)
        yield transformed_data


def _split_line(line: str) -> DataType:
    left, right = line.split(" | ", 2)
    return left.split(), right.split()


def process_data(data: Iterable[DataType]) -> int:
    total = 0
    for (examples, values) in data:
        example_result = _process_examples_brute_force(examples)
        result = _evaluate(example_result, values)
        total += result
    return total


SegmentMap = dict[str, Segments]


def _process_examples_brute_force(examples: list[str]) -> SegmentMap:
    for possible in itertools.permutations(ALL_SEGMENTS):
        segment_map = {l: s for (l, s) in zip("abcdefg", possible)}
        if _check_permutation(examples, segment_map):
            return segment_map
    raise Exception()


def _check_permutation(examples: list[str], segment_map: SegmentMap) -> bool:
    for example in examples:
        example_segments = Segments.combine(segment_map[c] for c in example)
        if example_segments not in VALID_SEGMENT_COMBINATIONS:
            return False
    return True


def _evaluate(example_result: SegmentMap, values: list[str]) -> int:
    result = 0
    for value in values:
        value_segments = Segments.combine(example_result[c] for c in value)
        value_number = SEGMENT_NUMBERS[value_segments]
        result *= 10
        result += value_number
    return result


def render_result(result: int):
    print(result)


def main():
    fname = "input.txt"
    # fname = "sample.txt"
    # fname = "simple_sample.txt"
    # fname = "big_data.txt"
    with get_data(fname) as data:
        result = process_data(data)
        render_result(result)
    # sample -> 5353
    # input -> 1027483


if __name__ == "__main__":
    main()
