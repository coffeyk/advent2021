#!/usr/bin/env python

import os
from typing import Counter, Iterable, NamedTuple


class ResultSet(NamedTuple):
    position: int
    cost: int


def get_data(fname: str) -> Iterable[int]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fpath = os.path.join(dir_path, fname)
    with open(fpath) as raw_data:
        return (int(x) for x in raw_data.read().split(","))


def process_data(data: Iterable[int]) -> ResultSet:
    position_counts = Counter(data)

    min_position = min(position_counts.keys())
    max_position = max(position_counts.keys())

    # Start at the end so the range doesn't need a +/-
    min_cost = cost(position_counts, max_position)
    best_position = max_position
    for p in range(min_position, max_position):
        position_cost = cost(position_counts, p)
        if position_cost < min_cost:
            min_cost = position_cost
            best_position = p

    print(best_position)

    return ResultSet(best_position, min_cost)


def cost(data: dict[int, int], target: int) -> int:
    return sum(weight * abs(target - position) for position, weight in data.items())


def render_result(result: ResultSet) -> None:
    print(f"{result}")
    # print(sum(result))


def main():
    fname = "input.txt"
    # fname = "sample.txt"
    data = get_data(fname)
    result = process_data(data)

    render_result(result)
    # sample -> ResultSet(position=2, cost=37)
    # input -> ResultSet(position=349, cost=355592)


if __name__ == "__main__":
    main()
