"""Segunda implementação dos primos em Pi
"""
from __future__ import annotations
import cProfile
from ctypes import ArgumentError
import os
import sys


def main(args) -> None:
    """main(args):

    Parâmetros:
    args: Lista de argumentos recebido da linha de comando e pré-processado na chamada da
    função main. Deve conter 1 argumento apenas indicando o caminho relativo ou absoluto
    do arquivo contendo o número Pi
    """
    # Análise dos argumentos recebidos em args
    nargs = len(args)
    if nargs == 0:
        raise ArgumentError("Nenhum argumento foi fornecido.")

    # Validação dos argumentos
    if nargs >= 1:
        arquivo_com_numero_pi = args[0]
        digitos_parte_fracionaria = ler_primos_do_arquivo(
            arquivo_com_numero_pi)

    if nargs >= 2:
        mensagem1 = f"Você informou um número excessivo de argumentos ({nargs}). "
        mensagem1 += "Apenas um argumento que aponte o caminho (relativo ou absoluto) "
        mensagem1 += "do arquivo contendo o número Pi com algumas casas decimais especificadas"
        mensagem1 += "e o número a ser convertido é necessário."
        print(mensagem1)

        mensagem2 = "Deseja prosseguir ignorando os demais argumentos? (S para Sim e N para não)"
        escolha_do_usuario = input(mensagem2)

        if escolha_do_usuario.lower() != "s":
            print("Programa abortado.")
            return

    primos_na_parte_fracionaria = obtem_primos_de_lista_de_inteiros(
        digitos_parte_fracionaria)

    # TODO: Remover antes da submissão
    for primo in primos_na_parte_fracionaria:
        if not e_primo(int(primo)):
            raise ArgumentError(f"Primo inválido: {primo}.")

    caracteres_concatenados = "".join(primos_na_parte_fracionaria)
    print(caracteres_concatenados)

    arquivo_de_resultado = "resultado.txt"
    if not os.path.isfile(arquivo_de_resultado):
        os.remove(arquivo_de_resultado)

    with open(arquivo_de_resultado, "w", encoding='utf-8') as arquivo:
        arquivo.write(caracteres_concatenados)

    print("Primos obtidos com sucesso!")


def obtem_primos_de_lista_de_inteiros(digitos: list[str]) -> list[str]:
    """obtem_primos_de_lista_de_inteiros(digitos_parte_fracionaria):
    Obtém uma lista de primos a partir de uma lista ordenada de dígitos

    Parâmetro:
    digitos: lista de dígitos
    """
    return []


def e_primo(numero) -> bool:
    """e_primo(numero):
    Determina se o número passado como argumento é primo ou não. Retorna True se o número for primo
    e False se não for.
    """
    if numero <= 1:
        return False

    divisor = 2
    while divisor <= numero / 2:
        if numero % divisor == 0:
            return False
        divisor += 1
    return True


def ler_primos_do_arquivo(arquivo_com_numero_pi: str) -> list[str]:
    """ler_primos_do_arquivo(arquivo_com_numero_pi: str) -> list[str]:
    Processa o arquivo fornecido como parâmetro e retorna uma lista de strings, onde
    cada item é um dígito de pi

    Parâmetro:
    arquivo_com_numero_pi: Caminho do arquivo com número pi
    """
    if not os.path.isfile(arquivo_com_numero_pi):
        mensagem1 = "Arquivo não encontrado. Caminho fornecido ou nome do arquivo incorreto."
        raise ArgumentError(f"{mensagem1}")

    with open(arquivo_com_numero_pi, "r", encoding='utf-8') as arquivo:
        for linha in arquivo:
            numero_pi_com_n_casas_decimais = linha.split("\n")
            numero_pi_com_n_casas_decimais = numero_pi_com_n_casas_decimais[0]
            break

    if len(numero_pi_com_n_casas_decimais) <= 2:
        mensagem0 = "O número recebido não pode ser processado "
        mensagem0 += "(comprimento menor ou igual a 2 caracteres)"
        mensagem0 += " ou a primeira linha do arquivo estava vazio."
        raise ArgumentError(f"{mensagem0}")

    digitos_parte_fracionaria = numero_pi_com_n_casas_decimais[2:]
    digitos_parte_fracionaria = list(digitos_parte_fracionaria)

    return digitos_parte_fracionaria


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

    filtered_args = sys.argv[1:]
    main(filtered_args)

    # TODO: Remover antes da submissão do PR
    if debugger_is_active():
        pr.disable()
        pr.dump_stats("profiling-results.prof")
