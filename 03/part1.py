import os
from contextlib import contextmanager
from itertools import accumulate, zip_longest
from typing import Iterable, Iterator, NamedTuple, TypeVar

from util import show

S = TypeVar("S", bound="State")


class State(NamedTuple):
    bit_counts: list[int]
    size: int = 0

    def add_bits(self, bits: str) -> list[int]:
        bit_ints = (int(b == "1") for b in bits)

        bit_pairs = zip_longest(self.bit_counts, bit_ints, fillvalue=0)

        bit_counts = [a + b for (a, b) in bit_pairs]
        print(self.bit_counts)
        print(bit_counts)
        print(bit_ints)

        return bit_counts

    def add(self: S, value: str) -> S:
        return self._replace(bit_counts=self.add_bits(value), size=self.size + 1)

    def _gamma(self) -> list[int]:
        threshold = self.size / 2
        gamma_bits = [int(b > threshold) for b in self.bit_counts]
        return gamma_bits

    def _epsilon(self, gamma: list[int]) -> list[int]:
        epsilon_bits = [int(b == 0) for b in gamma]
        return epsilon_bits

    def report(self) -> tuple[list[int], list[int]]:
        gamma = self._gamma()
        epsilon = self._epsilon(gamma)

        return gamma, epsilon


@contextmanager
def get_data(fname: str) -> Iterator[Iterable[str]]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fpath = os.path.join(dir_path, fname)
    with open(fpath) as raw_data:
        # trim trailing newline?
        yield (line[:-1] for line in raw_data)


def process_data(values: Iterable[str]) -> tuple[list[int], list[int]]:
    pretty_values = (show(v, end=" ") for v in values)
    results: accumulate[State] = accumulate(
        pretty_values, func=State.add, initial=State(bit_counts=[])
    )

    pretty_results = (show(s) for s in results)
    *_, last_value = pretty_results

    # gamma_bits, epsilon_bits = last_value.report()

    return last_value.report()


def _print_bits(bits: list[int]) -> int:
    bits_value = int("".join((str(b) for b in bits)), 2)
    print(f"{bits=} {bits_value=}")
    return bits_value


def render_result(result: tuple[list[int], list[int]]) -> None:
    gamma_bits, epsilon_bits = result
    gamma = _print_bits(gamma_bits)
    epsilon = _print_bits(epsilon_bits)
    print(f"{gamma*epsilon=}")


def main():
    fname = "./input.txt"
    # fname = "sample.txt"
    with get_data(fname) as data:
        result = process_data(data)
    render_result(result)


if __name__ == "__main__":
    main()
