"""Processamento de expressões numéricas
"""
from __future__ import annotations
import cProfile
from ctypes import ArgumentError
import sys

from expressao import SyntaxErrorException, expressao_numerica


def main(args) -> None:
    """main(args):

    Parâmetros:
    args: Lista de argumentos recebido da linha de comando e pré-processado na chamada da
    função main. Deve conter 1 argumento apenas indicando o caminho relativo ou absoluto
    do arquivo contendo as expressões numéricas a serem avaliadas
    """
    # Análise dos argumentos recebidos em args
    nargs = len(args)
    if nargs == 0:
        raise ArgumentError("Nenhum argumento foi fornecido.")

    # Validação dos argumentos
    if nargs >= 1:
        arquivo_com_expressoes_numericas = args[0]

    if nargs >= 2:
        mensagem = f"Você informou um número excessivo de argumentos ({nargs}). "
        mensagem += "Apenas um argumento que aponte o caminho (relativo ou absoluto) "
        mensagem += "do arquivo contendo as expressões numéricas."
        print(mensagem)

        mensagem2 = "Deseja prosseguir ignorando os demais argumentos? (S para Sim e N para não)"
        escolha_do_usuario = input(mensagem2)

        if escolha_do_usuario.lower() != "s":
            print("Programa abortado.")
            return

    with open(arquivo_com_expressoes_numericas, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha_processada = linha.strip("\n")
            try:
                expressao = expressao_numerica(linha_processada)
                print(expressao.resultado())
            except SyntaxErrorException as ex:
                print(f"ERR SYNTAX: {ex}")


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
