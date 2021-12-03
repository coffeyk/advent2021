#!/usr/bin/env python

from itertools import islice, tee
from collections import deque
from contextlib import contextmanager
from typing import Iterable, Iterator, Tuple, TypeVar

# count the number of times a depth measurement increases from the previous measurement using a slding window of size 3

T = TypeVar("T")


def pairwise(data: Iterable[T]) -> Iterable[Tuple[T, T | None]]:
    a, b = tee(data, 2)
    # First pair has no previous
    yield (next(a), None)
    yield from zip(a, b)


@contextmanager
def get_data() -> Iterator[Iterable[int]]:
    fname = "input.txt"
    # fname = "sample.txt"
    with open(fname) as raw_data:
        data = (int(line) for line in raw_data)
        yield data


def sliding_sum(data: Iterable[int], size: int) -> Iterable[int]:
    assert size
    # boostrap the window with most values
    window = deque(islice(data, size - 1), maxlen=size)
    # Filler value for the first popleft
    window.appendleft(0)
    total = sum(window)
    for point in data:
        # Total sum is removing the oldest point and adding the new point
        total += point - window.popleft()
        window.append(point)
        yield total


def _compare_points(cur: int, prev: int | None) -> str:
    if prev is None:
        return "N/A"
    elif cur == prev:
        return "no change"
    elif cur < prev:
        return "decreased"
    return "increased"


def process_data(data: Iterable[int]) -> int:
    total = 0
    for cur, prev in pairwise(sliding_sum(data, size=3)):
        status = _compare_points(cur, prev)
        print(f"{cur} ({status})")

        if status == "increased":
            total += 1

    return total


def render_result(result: int) -> None:
    print(result)


def main():
    with get_data() as data:
        result = process_data(data)
    render_result(result)


if __name__ == "__main__":
    main()
