"""Potências de 2
"""
from __future__ import annotations
import cProfile
from ctypes import ArgumentError
import sys


def main(args) -> None:
    """main(args):

    Parâmetros:
    args: Lista de argumentos recebido da linha de comando e pré-processado na chamada da
    função main. Deve conter 1 argumento apenas indicando o caminho relativo ou absoluto
    do arquivo contendo os números com possíveis potências de 2
    """
    # Análise dos argumentos recebidos em args
    nargs = len(args)
    if nargs == 0:
        raise ArgumentError("Nenhum argumento foi fornecido.")

    # Validação dos argumentos
    if nargs >= 1:
        arquivo_com_potencias_de_2 = args[0]

    if nargs >= 2:
        mensagem = f"Você informou um número excessivo de argumentos ({nargs}). "
        mensagem += "Apenas um argumento que aponte o caminho (relativo ou absoluto) "
        mensagem += "do arquivo contendo as possíveis potências de 2."
        print(mensagem)

        mensagem2 = "Deseja prosseguir ignorando os demais argumentos? (S para Sim e N para não)"
        escolha_do_usuario = input(mensagem2)

        if escolha_do_usuario.lower() != "s":
            print("Programa abortado.")
            return

    lista_de_candidatos: list[int] = []
    with open(arquivo_com_potencias_de_2, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha_processada = (linha.split("\n"))[0]
            candidato = int(linha_processada)
            lista_de_candidatos.append(candidato)

    lista_de_resultados = processa_candidatos(lista_de_candidatos)

    with open("resultado.txt", "w", encoding='utf-8') as arquivo:
        for resultado in lista_de_resultados:
            print(resultado)
            arquivo.write(f"{resultado}\n")


def processa_candidatos(lista_de_candidatos) -> list[str]:
    resultados: list[str] = []

    for candidato in lista_de_candidatos:
        potencia_de_2, expoente = descobre_expoente(candidato)
        if potencia_de_2:
            resultado = f"{candidato} {str(potencia_de_2).lower()} {expoente}"
        else:
            resultado = f"{candidato} {str(potencia_de_2).lower()}"
        resultados.append(resultado)

    return resultados


def descobre_expoente(candidato: int) -> tuple[bool, int]:

    if candidato == 0:
        return False, -1

    if candidato == 1:
        return True, 0

    resultado = 2
    potencia_de_2 = True
    expoente = 1

    while resultado < candidato:
        resultado = resultado * 2
        expoente += 1

    if resultado > candidato:
        potencia_de_2 = False
        expoente = -1

    return potencia_de_2, expoente


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
