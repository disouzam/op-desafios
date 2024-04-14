"""Busca primos em Pi
"""
from ctypes import ArgumentError
import os
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

    # Validação dos argumentos
    if nargs >= 1:
        arquivo_com_numero_pi = args[0]

        if not os.path.isfile(arquivo_com_numero_pi):
            mensagem1 = "Arquivo não encontrado. Caminho fornecido ou nome do arquivo incorreto."
            print(mensagem1)
            return

        with open(arquivo_com_numero_pi, "r", encoding='utf-8') as arquivo:
            for linha in arquivo:
                numero_pi_com_n_casas_decimais = linha.split("\n")
                numero_pi_com_n_casas_decimais = numero_pi_com_n_casas_decimais[0]
                break

        if len(numero_pi_com_n_casas_decimais) <= 2:
            mensagem0 = "O número recebido não pode ser processado "
            mensagem0 += "(comprimento menor ou igual a 2 caracteres)"
            mensagem0 += " ou a primeira linha do arquivo estava vazio."
            print(mensagem0)

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

    print(numero_pi_com_n_casas_decimais)


def e_primo(numero):
    """
        Determina se o número passado como argumento é primo ou não
    """
    divisor = 2
    while divisor <= numero / 2:
        if numero % divisor == 0:
            return False
        divisor += 1
    return True


if __name__ == "__main__":
    filtered_args = sys.argv[1:]
    main(filtered_args)
