#!/usr/bin/env python

from typing import List

# count the number of times a depth measurement increases from the previous measurement

def get_data() -> List[int]:
    fname = "input.txt"
    # fname = "sample.txt"
    with open(fname) as raw_data:
        data = [int(line) for line in raw_data]
    return data

def process_data(data: List[int]) -> int:
    prev = None
    result = 0
    for point in data:
        status = "N/A"

        if prev is not None:
            if point > prev:
                result += 1
                status = "increased"
            else:
                status = "decreased"

        print(f"{point} ({status})")
        prev = point

    return result


def render_result(result: int):
    print(result)


def main():
    data = get_data()
    result = process_data(data)
    render_result(result)


if __name__ == "__main__":
    main()