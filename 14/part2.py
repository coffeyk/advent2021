#!/usr/bin/env python

import os
from collections import defaultdict
from contextlib import contextmanager
from pprint import pprint
from typing import Counter, Iterator, TypeVar

from util import pairwise

T = TypeVar("T")

GenericTable = dict[tuple[str | None, str], T]
TableType = GenericTable[str]
PairCounts = GenericTable[int]
DataType = tuple[str, TableType]
ResultType = int


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


def step(pattern: PairCounts, table: TableType) -> PairCounts:
    """step performs one round of substitution on the pattern using the table

    Args:
        pattern (PairCounts): The initial counts of each character pair
        table (TableType): The mapping table of character pair to new value

    Returns:
        PairCounts: The final counts of each character pair
    """
    result: PairCounts = defaultdict(int)
    for pair, count in pattern.items():
        try:
            # E.g (X, Y) -> (X, Z) and (Z, Y)
            new_value = table[pair]
            prev, cur = pair
            result[(prev, new_value)] += count
            result[(new_value, cur)] += count
        except KeyError:
            # E.g (X, Y) -> (X, Y)
            result[pair] += count
    return result


def process_data(data: DataType) -> ResultType:
    """process_data computes the score after 40 rounds of replacement

    Args:
        data (DataType): The pattern and replacement table

    Returns:
        ResultType: The final score
    """
    pattern, table = data

    # Build up the initial pair counts from the given pattern
    result = _pair_counts(pattern)

    for _ in range(40):
        result = step(result, table)
        # pprint(result)

    final_score = score(result)

    return final_score


def _pair_counts(pattern: str) -> PairCounts:
    """_pair_counts converts a string into a PairCounts map

    Args:
        pattern (str): The string to count pairs from

    Returns:
        PairCounts: The map of character pairs to their counts
    """
    result: PairCounts = defaultdict(int)
    for cur, prev in pairwise(pattern):
        # Flip the order to match up with the expected format of the replacement table
        result[(prev, cur)] += 1
    return result


def render_result(result: ResultType):
    print(result)


def score(result: PairCounts) -> int:
    """score is the quantity of the most common element minus the quantity of the least common element.

    Args:
        result (PairCounts): The map of character pairs to their counts
        first_character (str): The first character from the original pattern

    Returns:
        int: The score of the result
    """
    counts: dict[str, int] = Counter()

    # Only look at one character of the pair, otherwise we'll double count
    # e.g. ABC -> "AB", "BC" the B is counted twice.
    # We use the second character because the first character of the original input is parsed as the pair (None, C)
    for (_, c2), count in result.items():
        counts[c2] += count

    pprint(counts)
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
