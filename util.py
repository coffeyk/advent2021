from enum import Enum
from typing import TypeVar, Iterable
from itertools import tee


class StrEnum(str, Enum):
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[str]
    ) -> str:
        """
        Return the lower-cased version of the member name.
        """
        return name.lower()


T = TypeVar("T")


def show(state: T, end: str = "\n") -> T:
    print(state, end=end)
    return state


def pairwise(data: Iterable[T]) -> Iterable[tuple[T, T | None]]:
    a, b = tee(data, 2)
    # First pair has no previous
    yield (next(a), None)
    yield from zip(a, b)
