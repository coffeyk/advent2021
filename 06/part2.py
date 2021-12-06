#!/usr/bin/env python

import os
from functools import cache
from typing import Iterable


def get_data(fname: str) -> Iterable[int]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fpath = os.path.join(dir_path, fname)
    with open(fpath) as raw_data:
        return (int(x) for x in raw_data.read().split(","))


def process_data(data: Iterable[int], steps: int = 256) -> list[int]:

    state = [0] * 9
    for d in data:
        state[d] += 1

    print(state)

    for s in range(steps):
        # Get the next step template for each timer and its current count
        template_counts = (
            (_step(timer), count) for timer, count in enumerate(state) if count
        )
        # Multiply the new timer template by the current count
        new_timers = (
            _scale(timer_template, count) for timer_template, count in template_counts
        )

        # Sum up the scaled timers into the final state
        state = _list_sum(*new_timers)
        print(f"{s=} {state=}")

    return list(state)


def _list_sum(*args: Iterable[int]) -> Iterable[int]:
    """_list_sum sums up the elements of each iterable"""
    return [sum(x) for x in zip(*args)]


def _scale(data: Iterable[int], scale: int) -> Iterable[int]:
    """_scale multiply each element of data by scape"""
    return (d * scale for d in data)


# This could have been a static dictionary lookup, but _lazy_
@cache
def _step(timer: int) -> list[int]:
    result = [0] * 9
    if timer == 0:
        result[6] = 1
        result[8] = 1
    else:
        result[timer - 1] = 1
    return result


def render_result(result: list[int]) -> None:
    print(result)
    print(sum(result))


def main():
    fname = "input.txt"
    fname = "sample.txt"
    data = get_data(fname)
    result = process_data(data)
    render_result(result)
    # sample -> 26984457539
    # input -> 1572358335990


if __name__ == "__main__":
    main()
