"""Módulo cuida da geração de combinação de bits usando generators / palavra-chave yield
"""
import math


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
        lista_inteiros = []

        for indice, item in enumerate(lista_convertida):
            lista_inteiros.append(int(item))

        yield lista_inteiros
