from enum import Enum
from itertools import tee, count
from typing import Generic, Iterable, Literal, TypeVar
from heapq import heappop, heappush
from dataclasses import dataclass


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


# https://docs.python.org/3/library/heapq.html
RemovedTask = Literal["<removed-task>"]
REMOVED_TASK: RemovedTask = "<removed-task>"


@dataclass(order=True)
class PriorityQueueEntry(Generic[T]):
    priority: int
    count: int
    task: T | RemovedTask


class PriorityQueue(Generic[T]):
    def __init__(self):
        self.pq: list[PriorityQueueEntry[T]] = []
        self.entry_finder: dict[T, PriorityQueueEntry[T]] = {}
        self.counter = count()

    def add_task(self, task: T, priority: int = 0) -> None:
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = PriorityQueueEntry(priority, count, task)
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def remove_task(self, task: T) -> None:
        entry = self.entry_finder[task]
        entry.task = REMOVED_TASK

    def pop_task(self) -> T:
        while self.pq:
            entry = heappop(self.pq)
            if entry.task != REMOVED_TASK:
                del self.entry_finder[entry.task]
                return entry.task
        raise KeyError("pop_task from an empty priority queue")
