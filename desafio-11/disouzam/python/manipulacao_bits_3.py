import math
import sys


def combinacoes_bits(tamanho):
    """combinacoes_bits(tamanho)
    Gera lista de combinações de bits para avaliar a superposição entre primos

    Parâmetro:
    tamanho: Número de bits para gerar a combinação
    """
    contador = 0
    maximo = int(math.pow(2, tamanho)) - 1

    for contador in range(maximo, 0, -1):
        numero_em_binario = '{0:0>{width}{base}}'.format(
            contador, base='b', width=tamanho)
        lista_convertida = list(numero_em_binario)
        yield lista_convertida


def main(args) -> None:
    contador = 0
    for combinacao in combinacoes_bits(4):
        print(f"{contador} - {combinacao}")
        contador += 1

    print()

    contador = 0
    for combinacao in combinacoes_bits(5):
        print(f"{contador} - {combinacao}")
        contador += 1

    print()

    contador = 0
    maximo = int(math.pow(2, 29)) - 1
    intervalo = int(maximo / 1000)
    indice = 0
    for combinacao in combinacoes_bits(29):
        if contador == intervalo:
            print(f"{indice/maximo*100:.2f}% - {combinacao}")
            contador = 0

        indice += 1
        contador += 1


if __name__ == "__main__":
    filtered_args = sys.argv[1:]
    main(filtered_args)
