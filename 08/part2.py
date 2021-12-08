#!/usr/bin/env python

from functools import reduce
import os
from collections import defaultdict
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


DigitValues = tuple[list[str], list[str]]


@contextmanager
def get_data(fname: str) -> Iterator[Iterable[DigitValues]]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fpath = os.path.join(dir_path, fname)
    with open(fpath) as raw_data:
        transformed_data = (_split_line(d) for d in raw_data)
        yield transformed_data


def _split_line(line: str) -> DigitValues:
    left, right = line.split(" | ", 2)
    return left.split(), right.split()


def process_data(data: Iterable[DigitValues]) -> int:
    total = 0
    for (examples, values) in data:
        segment_map = _process_examples_logically(examples)
        result = _evaluate(segment_map, values)
        total += result
    return total


SegmentMap = dict[str, Segments]


def _process_examples_logically(examples: list[str]) -> SegmentMap:
    partial_segment_map: dict[str, Segments] = {}

    example_map: dict[int, list[set[str]]] = defaultdict(list)
    for e in examples:
        example_map[len(e)].append(set(e))

    # Find the A segment
    # One is CF
    cf_pair = example_map[2][0]
    # Seven is ACF
    afc_triple = example_map[3][0]
    # So A is seven - one
    a_segment = (afc_triple - cf_pair).pop()
    partial_segment_map[a_segment] = Segments.A

    # Four is BCDF
    bcdf_set = example_map[4][0]

    # We know One is CF, so four - one is BD
    bd_pair = bcdf_set - cf_pair

    # Now we'll use the 5 segment numbers to resolve B, D, and G

    # All 5 segment numbers have A D G in common
    five_segment_sets = example_map[5]
    adg_triple = five_segment_sets[0].intersection(*five_segment_sets[1:])

    # A is known, so reduce to the DG pair
    dg_pair = adg_triple - {a_segment}

    # we now have to pairs BD and DG, so their intersection is D which resolves the other two
    d_segment = (bd_pair & dg_pair).pop()
    partial_segment_map[d_segment] = Segments.D

    b_segment = (bd_pair - {d_segment}).pop()
    partial_segment_map[b_segment] = Segments.B

    g_segment = (dg_pair - {d_segment}).pop()
    partial_segment_map[g_segment] = Segments.G

    # Knowing B, we can identify the 5 (ABDFG)
    abdfg_set = next((s for s in five_segment_sets if s.intersection(b_segment)))
    # And solve for F because we know the other four segments
    f_segment = (abdfg_set - set((a_segment, b_segment, d_segment, g_segment))).pop()
    partial_segment_map[f_segment] = Segments.F

    # Knowing F, we can finally resolve the CF pair
    c_segment = (cf_pair - {f_segment}).pop()
    partial_segment_map[c_segment] = Segments.C

    # Finally, E is the final outstanding segment
    e_segment = (set("abcdefg") - partial_segment_map.keys()).pop()
    partial_segment_map[e_segment] = Segments.E

    return partial_segment_map


def _evaluate(segment_map: SegmentMap, values: list[str]) -> int:
    result = 0
    for value in values:
        value_segments = Segments.combine(segment_map[c] for c in value)
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
