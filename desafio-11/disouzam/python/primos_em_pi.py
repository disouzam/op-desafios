"""Busca primos em Pi
"""
from ctypes import ArgumentError
import os
import pathlib
import sys


def main(args):
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

    linhas_de_instrucao = []
    # Validação dos argumentos
    if nargs >= 1:
        arquivo_de_dados = args[0]

        if not os.path.isfile(arquivo_de_dados):
            mensagem1 = "Arquivo não encontrado. Caminho fornecido ou nome do arquivo incorreto."
            print(mensagem1)
            return

        caminho_do_arquivo_de_dados = pathlib.Path(arquivo_de_dados)
        pasta_raiz = caminho_do_arquivo_de_dados.parent
        with open(arquivo_de_dados, "r", encoding='utf-8') as arquivo:
            for linha in arquivo:
                linha_processada = linha.split("\n")
                arquivo_de_regras_e_dados = linha_processada[0].split(",")
                linhas_de_instrucao.append(arquivo_de_regras_e_dados)

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


if __name__ == "__main__":
    filtered_args = sys.argv[1:]
    main(filtered_args)
