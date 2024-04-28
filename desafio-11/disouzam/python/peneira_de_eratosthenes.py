"""Implementação da peneira de Eratosthenes para obtenção de todos os primos.
Essa implementação foi baseada em leitura do código do Adriano Roberto de Lima, escrita em Go
também nesse repositório.
Referência: https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
Perfil do Adriano Lima: https://github.com/arlima
"""
import math
import sys
import cProfile


def primos_ate_n(numero_maximo_para_busca) -> list[int]:
    lista_de_numeros = [True] * (numero_maximo_para_busca + 1)
    limite_de_busca = int(math.sqrt(numero_maximo_para_busca)) + 1

    lista_de_numeros[0] = False
    lista_de_numeros[1] = False

    for i in range(2, limite_de_busca):
        if lista_de_numeros[i]:
            for j in range(i*i, numero_maximo_para_busca + 1, i):
                lista_de_numeros[j] = False

    numeros_primos: list[int] = []
    for numero, classificacao in enumerate(lista_de_numeros):
        if classificacao:
            numeros_primos.append(numero)

    return numeros_primos


def debugger_is_active() -> bool:
    # TODO: Remover antes da submissão do PR
    """Return if the debugger is currently active

    # pylint: disable=line-too-long
    Source: https://stackoverflow.com/questions/38634988/check-if-program-runs-in-debug-mode/67065084
    """
    return hasattr(sys, 'gettrace') and sys.gettrace() is not None


if __name__ == "__main__":
    # TODO: Remover antes da submissão do PR
    if debugger_is_active():
        pr = cProfile.Profile(builtins=False, subcalls=False)
        pr.enable()

    primos_ate_n(10000)

    # TODO: Remover antes da submissão do PR
    if debugger_is_active():
        pr.disable()
        pr.dump_stats("profiling-results.prof")
