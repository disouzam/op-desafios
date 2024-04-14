"""Busca primos em Pi
"""
from ctypes import ArgumentError
import os
import sys
from typing import List


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

    digitos_parte_fracionaria = numero_pi_com_n_casas_decimais[2:]
    digitos_parte_fracionaria = list(digitos_parte_fracionaria)
    primos_na_parte_fracionaria = obtem_primos_da_parte_fracionaria(
        digitos_parte_fracionaria)

    # TODO: Remover antes da submissão
    for primo in primos_na_parte_fracionaria:
        if not e_primo(int(primo)):
            raise ArgumentError(f"Primo inválido: {primo}.")

    caracteres_concatenados = "".join(primos_na_parte_fracionaria)
    print(caracteres_concatenados)


def obtem_primos_da_parte_fracionaria(digitos_parte_fracionaria):
    """obtem_primos_da_parte_fracionaria(digitos_parte_fracionaria):
    Obtém uma lista de primos a partir de uma lista ordenada de dígitos da parte fracionária do
    número Pi

    Parâmetro:
    digitos_parte_fracionaria: lista de dígitos da parte fracionária do número Pi
    """
    lista_primos: List[int] = []
    posicao_caractere_atual = 0

    while posicao_caractere_atual < len(digitos_parte_fracionaria):
        comprimento = 1
        maior_primo = 0
        numero_digitos_primo = 0

        while comprimento < 5:
            candidato = digitos_parte_fracionaria[posicao_caractere_atual:
                                                  posicao_caractere_atual + comprimento]
            candidato = "".join(candidato)
            candidato = int(candidato)

            if e_primo(candidato) and candidato > maior_primo:
                maior_primo = candidato
                numero_digitos_primo = comprimento

            comprimento += 1

        if maior_primo != 0:
            lista_primos.append(str(maior_primo))

        if numero_digitos_primo == 0:
            posicao_caractere_atual += 1
        else:
            posicao_caractere_atual += numero_digitos_primo

    return lista_primos


def e_primo(numero):
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


if __name__ == "__main__":
    filtered_args = sys.argv[1:]
    main(filtered_args)
