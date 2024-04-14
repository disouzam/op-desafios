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
    lista_primos: List[int] = []
    lista_posicoes = []
    posicao_caractere_atual = 0

    # TODO: Remover antes da submissão
    arquivo_de_posicoes = "posicoes.txt"
    arquivo_primos_candidatos = "primos_candidatos.txt"

    if os.path.exists(arquivo_de_posicoes):
        os.remove(arquivo_de_posicoes)

    if os.path.exists(arquivo_primos_candidatos):
        os.remove(arquivo_primos_candidatos)

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

            lista_primos.append(str(maior_primo))
            lista_posicoes.append((posicao_inicial, posicao_final))

            # TODO: Remover antes da submissão
            with open(arquivo_primos_candidatos, "a", encoding='utf-8') as primo_candidato:
                primo_candidato.write(str(maior_primo) + "\n")

            indice = posicao_inicial
            string_posicoes = ''
            while indice <= posicao_final:
                string_posicoes += str(indice) + " "
                indice += 1

            string_posicoes = string_posicoes.strip()

            # TODO: Remover antes da submissão
            with open(arquivo_de_posicoes, "a", encoding='utf-8') as posicoes_candidato:
                posicoes_candidato.write(string_posicoes + "\n")

        posicao_caractere_atual += 1

    # Primeiro passe de remoção de sobreposições
    # Remove somente sobreposição total
    quantidade_primos_sem_filtrar = len(lista_primos)
    primo_analisado = 0
    lista_primos_filtrada: List[int] = []
    lista_posicoes_filtrada = []

    while primo_analisado < quantidade_primos_sem_filtrar - 1:
        posicoes_primo_atual = lista_posicoes[primo_analisado]
        posicoes_proximo_primo = lista_posicoes[primo_analisado + 1]

        # Sobreposição não existe ou é parcial
        if posicoes_proximo_primo[0] > posicoes_primo_atual[1] or posicoes_proximo_primo[1] > posicoes_primo_atual[1]:
            lista_primos_filtrada.append(lista_primos[primo_analisado])
            lista_posicoes_filtrada.append(
                lista_posicoes[primo_analisado])
            continue

        tamanho_primo_atual = posicoes_primo_atual[1] - \
            posicoes_primo_atual[0] + 1
        tamanho_proximo_primo = posicoes_proximo_primo[1] - \
            posicoes_proximo_primo[0] + 1

        if tamanho_proximo_primo <= tamanho_primo_atual:
            lista_primos_filtrada.append(lista_primos[primo_analisado])
            lista_posicoes_filtrada.append(
                lista_posicoes[primo_analisado])
        else:
            lista_primos_filtrada.append(lista_primos[primo_analisado+1])
            lista_posicoes_filtrada.append(
                lista_posicoes[primo_analisado+1])

        primo_analisado += 1

    return lista_primos_filtrada


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
