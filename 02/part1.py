#!/usr/bin/env python

from itertools import accumulate

from contextlib import contextmanager
from typing import Iterable, Iterator
from enum import Enum, auto
from dataclasses import dataclass

# forward X increases the horizontal position by X units.
# down X increases the depth by X units.
# up X


class CommandName(Enum):
    FORWARD = auto()
    DOWN = auto()
    UP = auto()


@dataclass
class Command:
    name: CommandName
    value: int


@dataclass
class Point:
    horizontal: int
    depth: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.horizontal + other.horizontal, self.depth + other.depth)


@contextmanager
def get_data() -> Iterator[Iterable[Command]]:
    fname = "input.txt"
    # fname = "sample.txt"
    with open(fname) as raw_data:
        data = (line.split() for line in raw_data)
        transformed_data = (transform_point(d) for d in data)
        yield transformed_data


def transform_point(raw_point: list[str]) -> Command:
    # assert len(raw_point) ==
    raw_command, raw_value = raw_point
    return Command(CommandName[raw_command.upper()], int(raw_value))


def command_vector(command: Command) -> Point:
    command_map = {
        CommandName.FORWARD: Point(1, 0),
        CommandName.UP: Point(0, -1),
        CommandName.DOWN: Point(0, 1),
    }
    direction = command_map[command.name]
    return Point(
        horizontal=command.value * direction.horizontal,
        depth=command.value * direction.depth,
    )


def process_data(commands: Iterable[Command]) -> Iterator[Point]:
    command_vectors = (command_vector(c) for c in commands)

    return accumulate(command_vectors)


def render_result(result: Iterator[Point]):
    last_value = None
    for p in result:
        print(p)
        last_value = p
    if last_value is not None:
        print(f"{last_value.depth * last_value.horizontal=}")


def main():
    with get_data() as data:
        result = process_data(data)
        render_result(result)


if __name__ == "__main__":
    main()
