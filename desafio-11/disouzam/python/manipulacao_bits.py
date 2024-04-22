import numpy
import sys


def main(args) -> None:
    a = numpy.zeros(10, dtype=numpy.int8)
    print(a)
    print(type(a))

    for item in a:
        print(item)
        print(type(item))

    b = numpy.ones(10, dtype=numpy.int8)

    print(b)
    print(type(b))

    for item in b:
        print(item)
        print(type(item))

    c = numpy.concatenate((a, b))

    print(c)
    print(type(c))

    for item in c:
        print(item)
        print(type(item))


if __name__ == "__main__":
    filtered_args = sys.argv[1:]
    main(filtered_args)
