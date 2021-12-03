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

    def _gamma(self) -> str:
        threshold = self.size / 2
        gamma_bits = "".join(
            ("1" if (b >= threshold) else "0") for b in self.bit_counts
        )
        return gamma_bits

    def _epsilon(self, gamma: str) -> str:

        epsilon_bits = "".join(("0" if c == "1" else "1") for c in gamma)
        return epsilon_bits

    def report(self) -> tuple[str, str]:
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


def bit_index_filter(value: str, index: int, c: str) -> bool:
    return value[index] == c


def _process_data(value_set: set[str], gamma: bool = True) -> str:
    index = 0
    while len(value_set) > 1:
        pretty_values = (show(v, end=" ") for v in value_set)

        results: accumulate[State] = accumulate(
            pretty_values, func=State.add, initial=State(bit_counts=[])
        )
        *_, last_value = results

        gamma_bits, epsilon_bits = last_value.report()
        if gamma:
            filter_bit = gamma_bits[index]
        else:
            filter_bit = epsilon_bits[index]

        value_set = {
            v
            for v in value_set
            if bit_index_filter(
                v,
                index,
                c=filter_bit,
            )
        }
        index += 1

    return value_set.pop()


def process_data(values: Iterable[str]) -> tuple[str, str]:
    value_set = set(values)

    oxygen = _process_data(value_set.copy(), gamma=True)
    c02 = _process_data(value_set.copy(), gamma=False)

    return oxygen, c02


def _print_bits(bits: str) -> int:
    bits_value = int(bits, 2)
    print(f"{bits=} {bits_value=}")
    return bits_value


def render_result(result: tuple[str, str]) -> None:
    oxygen_bits, c02_bits = result
    oxygen = _print_bits(oxygen_bits)
    c02 = _print_bits(c02_bits)
    print(f"{oxygen*c02=}")


def main():
    fname = "./input.txt"
    # fname = "sample.txt"
    with get_data(fname) as data:
        result = process_data(data)
    render_result(result)


if __name__ == "__main__":
    main()
