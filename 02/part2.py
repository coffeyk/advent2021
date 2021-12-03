#!/usr/bin/env python

import os
from contextlib import contextmanager
from enum import auto
from itertools import accumulate
from typing import Iterable, Iterator, NamedTuple, Type, TypeVar

from util import StrEnum, show

# In addition to horizontal position and depth, you'll also need to track a third value, aim, which also starts at 0. The commands also mean something entirely different than you first thought:

# down X increases your aim by X units.
# up X decreases your aim by X units.
# forward X does two things:
# It increases your horizontal position by X units.
# It increases your depth by your aim multiplied by X.


class CommandName(StrEnum):
    FORWARD = auto()
    DOWN = auto()
    UP = auto()


C = TypeVar("C", bound="Command")


class Command(NamedTuple):
    name: CommandName
    value: int

    @classmethod
    def from_raw(cls: Type[C], raw_command: str) -> C:
        raw_name, raw_value = raw_command.split()
        return cls(CommandName(raw_name), int(raw_value))


S = TypeVar("S", bound="State")


class State(NamedTuple):
    horizontal: int = 0
    depth: int = 0
    aim: int = 0

    def forward(self: S, value: int) -> S:
        """forward X does two things:

        * It increases your horizontal position by X units.
        * It increases your depth by your aim multiplied by X.
        """
        return self._replace(
            horizontal=self.horizontal + value,
            depth=self.depth + self.aim * value,
        )

    def up(self: S, value: int) -> S:
        """up X decreases your aim by X units."""
        return self._replace(
            aim=self.aim - value,
        )

    def down(self: S, value: int) -> S:
        """down X increases your aim by X units."""
        return self._replace(
            aim=self.aim + value,
        )

    _command_map = {
        CommandName.FORWARD: forward,
        CommandName.UP: up,
        CommandName.DOWN: down,
    }

    def move(self: S, command: Command) -> S:
        return self._command_map[command.name](self, command.value)


@contextmanager
def get_data(fname: str) -> Iterator[Iterable[Command]]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fpath = os.path.join(dir_path, fname)
    with open(fpath) as raw_data:
        commands = (Command.from_raw(r) for r in raw_data)
        yield commands


def process_data(commands: Iterable[Command]) -> State:
    pretty_commands = (show(c, end=" ") for c in commands)
    results: accumulate[State] = accumulate(
        pretty_commands, func=State.move, initial=State()
    )

    pretty_results = (show(s) for s in results)
    *_, last_value = pretty_results

    return last_value


def render_result(result: State) -> None:
    print(f"{result.depth * result.horizontal=}")


def main():
    fname = "./input.txt"
    # fname = "sample.txt"
    with get_data(fname) as data:
        result = process_data(data)
    render_result(result)


if __name__ == "__main__":
    main()
