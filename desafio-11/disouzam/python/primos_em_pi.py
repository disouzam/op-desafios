"""Busca primos em Pi
"""
from ctypes import ArgumentError
import os
import string
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
    primos_na_parte_fracionaria = obtem_primos_de_lista_de_inteiros(
        digitos_parte_fracionaria)

    # TODO: Remover antes da submissão
    for primo in primos_na_parte_fracionaria:
        if not e_primo(int(primo)):
            raise ArgumentError(f"Primo inválido: {primo}.")

    caracteres_concatenados = "".join(primos_na_parte_fracionaria)
    print(caracteres_concatenados)


def obtem_primos_de_lista_de_inteiros(digitos):
    """obtem_primos_de_lista_de_inteiros(digitos_parte_fracionaria):
    Obtém uma lista de primos a partir de uma lista ordenada de dígitos

    Parâmetro:
    digitos: lista de dígitos
    """
    lista_primos = []
    posicao_caractere_atual = 0

    # TODO: Remover antes da submissão
    arquivo_de_posicoes = "posicoes.txt"
    arquivo_primos_candidatos = "primos_candidatos.txt"
    arquivo_de_posicoes_sobreposicoes = "posicoes_sobreposicoes.txt"
    arquivo_primos_candidatos_sobreposicoes = "primos_candidatos_sobreposicoes.txt"
    arquivo_de_posicoes_sem_sobreposicoes = "posicoes_sem_sobreposicoes.txt"
    arquivo_primos_candidatos_sem_sobreposicoes = "primos_candidatos_sem_sobreposicoes.txt"

    if os.path.exists(arquivo_de_posicoes):
        os.remove(arquivo_de_posicoes)

    if os.path.exists(arquivo_primos_candidatos):
        os.remove(arquivo_primos_candidatos)

    if os.path.exists(arquivo_de_posicoes_sobreposicoes):
        os.remove(arquivo_de_posicoes_sobreposicoes)

    if os.path.exists(arquivo_primos_candidatos_sobreposicoes):
        os.remove(arquivo_primos_candidatos_sobreposicoes)

    if os.path.exists(arquivo_de_posicoes_sem_sobreposicoes):
        os.remove(arquivo_de_posicoes_sem_sobreposicoes)

    if os.path.exists(arquivo_primos_candidatos_sem_sobreposicoes):
        os.remove(arquivo_primos_candidatos_sem_sobreposicoes)

    # Levanta todos os primos existentes, não checando sobreposição
    while posicao_caractere_atual < len(digitos):
        comprimento = 1
        maior_primo = 0
        numero_digitos_primo = 0

        while comprimento < 5:
            candidato = digitos[posicao_caractere_atual:
                                posicao_caractere_atual + comprimento]
            candidato = "".join(candidato)
            candidato = int(candidato)

            if e_primo(candidato) and candidato > maior_primo:
                maior_primo = candidato
                numero_digitos_primo = comprimento

            comprimento += 1

        if maior_primo != 0:
            posicao_inicial = posicao_caractere_atual
            posicao_final = posicao_caractere_atual + numero_digitos_primo - 1

            lista_primos.append((maior_primo, posicao_inicial, posicao_final))

            # TODO: Remover antes da submissão
            with open(arquivo_primos_candidatos, "a", encoding='utf-8') as primo_candidato:
                primo_candidato.write(str(maior_primo) + "\n")

            # TODO: Remover antes da submissão
            with open(arquivo_de_posicoes, "a", encoding='utf-8') as posicoes_candidato:
                posicoes_candidato.write(
                    f"{posicao_inicial}, {posicao_final}\n")

        posicao_caractere_atual += 1

    # Processa as sobreposições
    indice_candidato_analisado_na_lista = 0
    total_primos_candidatos_na_lista = len(lista_primos)
    while indice_candidato_analisado_na_lista < total_primos_candidatos_na_lista - 2:

        sobreposicoes = []

        candidato = lista_primos[indice_candidato_analisado_na_lista]
        posicao_inicial_candidato = candidato[1]
        posicao_final_candidato = candidato[2]

        indice_proximo_candidato = indice_candidato_analisado_na_lista + 1
        proximo_candidato = lista_primos[indice_proximo_candidato]
        posicao_inicial_ultimo_candidato = proximo_candidato[1]
        posicao_final_ultimo_candidato = proximo_candidato[2]

        sobreposicoes.append(candidato)

        while posicao_inicial_ultimo_candidato <= posicao_final_candidato:
            sobreposicoes.append(proximo_candidato)

            posicao_inicial_candidato = posicao_inicial_ultimo_candidato
            posicao_final_candidato = posicao_final_ultimo_candidato

            indice_proximo_candidato += 1
            proximo_candidato = lista_primos[indice_proximo_candidato]
            posicao_inicial_ultimo_candidato = proximo_candidato[1]
            posicao_final_ultimo_candidato = proximo_candidato[2]

        if len(sobreposicoes) > 1:
            indice_candidato_analisado_na_lista = indice_proximo_candidato
            for sobreposicao in sobreposicoes:
                # TODO: Remover antes da submissão
                with open(arquivo_primos_candidatos_sobreposicoes, "a", encoding='utf-8') as primo_candidato:
                    primo_candidato.write(f"{sobreposicao[0]}\n")

                # TODO: Remover antes da submissão
                with open(arquivo_de_posicoes_sobreposicoes, "a", encoding='utf-8') as posicoes_candidato:
                    posicoes_candidato.write(
                        f"{sobreposicao[1]}, {sobreposicao[2]}\n")
        else:
            indice_candidato_analisado_na_lista += 1
            sobreposicao = sobreposicoes[0]
            # TODO: Remover antes da submissão
            with open(arquivo_primos_candidatos_sem_sobreposicoes, "a", encoding='utf-8') as primo_candidato:
                primo_candidato.write(f"{sobreposicao[0]}\n")

            # TODO: Remover antes da submissão
            with open(arquivo_de_posicoes_sem_sobreposicoes, "a", encoding='utf-8') as posicoes_candidato:
                posicoes_candidato.write(
                    f"{sobreposicao[1]}, {sobreposicao[2]}\n")

    lista_primos_como_string = []
    for primo in lista_primos:
        lista_primos_como_string.append(f"{primo[0]}")

    return lista_primos_como_string


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
