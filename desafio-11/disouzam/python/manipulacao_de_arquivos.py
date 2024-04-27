"""Manipulação de arquivos para suporte à descoberta de Primos em Pi
"""
from ctypes import ArgumentError
import os


def ler_primos_do_arquivo(arquivo_com_numero_pi: str) -> list[str]:
    """ler_primos_do_arquivo(arquivo_com_numero_pi: str) -> list[str]:
    Processa o arquivo fornecido como parâmetro e retorna uma lista de strings, onde
    cada item é um dígito de pi

    Parâmetro:
    arquivo_com_numero_pi: Caminho do arquivo com número pi
    """
    if not os.path.isfile(arquivo_com_numero_pi):
        mensagem = "Arquivo não encontrado. Caminho fornecido ou nome do arquivo incorreto."
        raise ArgumentError(f"{mensagem}")

    with open(arquivo_com_numero_pi, "r", encoding='utf-8') as arquivo:
        for linha in arquivo:
            numero_pi_com_n_casas_decimais = linha.split("\n")
            numero_pi_com_n_casas_decimais = numero_pi_com_n_casas_decimais[0]
            break

    if len(numero_pi_com_n_casas_decimais) <= 2:
        mensagem = "O número recebido não pode ser processado "
        mensagem += "(comprimento menor ou igual a 2 caracteres)"
        mensagem += " ou a primeira linha do arquivo estava vazio."
        raise ArgumentError(f"{mensagem}")

    digitos_parte_fracionaria = numero_pi_com_n_casas_decimais[2:]
    digitos_parte_fracionaria = list(digitos_parte_fracionaria)

    return digitos_parte_fracionaria
