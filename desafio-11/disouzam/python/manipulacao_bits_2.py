# Reference: https://realpython.com/python-bitwise-operators/
import sys


def main(args) -> None:

    size = len(f"{15:b}")

    for numero in range(0, 16):
        print(numero)
        numero_em_binario = '{0:0>{width}{base}}'.format(
            numero, base='b', width=size)
        lista_convertida = list(numero_em_binario)
        print(lista_convertida)
        print()
        print()


if __name__ == "__main__":
    filtered_args = sys.argv[1:]
    main(filtered_args)
