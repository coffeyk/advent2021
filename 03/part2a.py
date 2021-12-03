from functools import reduce
import os
from contextlib import contextmanager
from typing import Iterable, Iterator, Optional, Callable, Tuple
from dataclasses import dataclass
from pprint import pprint
import operator
import svgling


T = str | Tuple[str, "T"] | Tuple[str, "T", "T"]


@dataclass
class Tree:

    zero: Optional["Tree"] = None
    one: Optional["Tree"] = None

    size: int = 0
    value: str = ""

    def add_word(self, word: str) -> "Tree":
        node = self
        for l in word:
            if l == "0":
                if node.zero is None:
                    node.zero = Tree()
                node = node.zero
            else:
                if node.one is None:
                    node.one = Tree()
                node = node.one
            node.size += 1
        node.value = word

        return node

    def add_word_functional(self, word: str, index: int = 0) -> "Tree":
        if index >= len(word):
            # finish them
            return Tree(one=self.one, zero=self.zero, value=word, size=self.size + 1)
        else:
            l = word[index]
            if l == "0":
                zero = self.zero or Tree()
                return Tree(
                    one=self.one,
                    zero=zero.add_word_functional(word, index + 1),
                    size=self.size + 1,
                )
            else:
                one = self.one or Tree()
                return Tree(
                    one=one.add_word_functional(word, index + 1),
                    zero=self.zero,
                    size=self.size + 1,
                )

    def oxygen(self) -> str:
        """
        To find oxygen generator rating, determine the most common value (0 or 1) in the current bit position,
        and keep only numbers with that bit in that position.
        If 0 and 1 are equally common, keep values with a 1 in the position being considered.
        """
        return self._walk(operator.ge)

    def co2(self) -> str:
        """
        To find CO2 scrubber rating, determine the least common value (0 or 1) in the current bit position,
        and keep only numbers with that bit in that position.
        If 0 and 1 are equally common, keep values with a 0 in the position being considered.
        """
        return self._walk(operator.lt)

    def _walk(self, comparison: Callable[..., bool]) -> str:
        # Traverse down the tree
        if self.zero is not None and self.one is not None:
            # Two good children, compare sizes
            if comparison(self.one.size, self.zero.size):
                node = self.one
            else:
                node = self.zero
        elif self.one is not None:
            # Single child
            node = self.one
        elif self.zero is not None:
            # Single child
            node = self.zero
        else:
            # Found a Leaf
            return self.value
        return node._walk(comparison)

    def render(self, name: str) -> T:
        left = self.zero.render("0") if self.zero else ""
        right = self.one.render("1") if self.one else ""

        title = f"{name}: {self.size}"
        if left and right:
            return (title, left, right)
        elif left:
            return (title, left)
        elif right:
            return (title, right)
        else:
            return (title, self.value)


@contextmanager
def get_data(fname: str) -> Iterator[Iterable[str]]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fpath = os.path.join(dir_path, fname)
    with open(fpath) as raw_data:
        # trim trailing newline
        yield (line[:-1] for line in raw_data)


def process_data(values: Iterable[str]) -> tuple[str, str]:
    # root = Tree()
    # for v in values:
    #     root.add_word(v)
    root = reduce(Tree.add_word_functional, values, Tree())
    # pprint(root)
    with open("3.2a.svg", "w") as fout:
        fout.write(
            svgling.draw_tree(
                root.render("*"),
            )
            .get_svg()
            .tostring()
        )

    oxygen = root.oxygen()
    co2 = root.co2()

    return (oxygen, co2)


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
    # fname = "./input.txt"
    fname = "sample.txt"
    with get_data(fname) as data:
        result = process_data(data)
    render_result(result)
    # bits='101011011111' bits_value=2783
    # bits='010101001001' bits_value=1353
    # oxygen*c02=3765399


if __name__ == "__main__":
    main()
