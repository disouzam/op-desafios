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

    arquivo_de_resultado = "resultado.txt"
    if not os.path.isfile(arquivo_de_resultado):
        os.remove(arquivo_de_resultado)

    with open(arquivo_de_resultado, "w", encoding='utf-8') as arquivo:
        arquivo.write(caracteres_concatenados)

    print("Primos obtidos com sucesso!")


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

            if e_primo(candidato):
                maior_primo = candidato
                numero_digitos_primo = comprimento

                posicao_inicial = posicao_caractere_atual
                posicao_final = posicao_caractere_atual + numero_digitos_primo - 1

                lista_primos.append(
                    (maior_primo, posicao_inicial, posicao_final))

                # TODO: Remover antes da submissão
                with open(arquivo_primos_candidatos, "a", encoding='utf-8') as primo_candidato:
                    primo_candidato.write(str(maior_primo) + "\n")

                # TODO: Remover antes da submissão
                with open(arquivo_de_posicoes, "a", encoding='utf-8') as posicoes_candidato:
                    posicoes_candidato.write(
                        f"{posicao_inicial}, {posicao_final}\n")

            comprimento += 1

        posicao_caractere_atual += 1

    # Processa as sobreposições
    lista_primos_com_sobreposicao = []
    lista_primos_com_sobreposicao_filtrada = []
    lista_primos_sem_sobreposicao = []

    indice_candidato_analisado_na_lista = 0
    total_primos_candidatos_na_lista = len(lista_primos)
    ultimo_indice_valido = total_primos_candidatos_na_lista - 1
    while indice_candidato_analisado_na_lista <= ultimo_indice_valido:

        sobreposicoes = []

        candidato = lista_primos[indice_candidato_analisado_na_lista]
        posicao_inicial_candidato = candidato[1]
        posicao_final_candidato = candidato[2]

        sobreposicoes.append(candidato)
        indice_proximo_candidato = indice_candidato_analisado_na_lista + 1

        while indice_proximo_candidato <= ultimo_indice_valido:

            proximo_candidato = lista_primos[indice_proximo_candidato]
            posicao_inicial_ultimo_candidato = proximo_candidato[1]
            posicao_final_ultimo_candidato = proximo_candidato[2]

            if posicao_inicial_ultimo_candidato <= posicao_final_candidato:
                sobreposicoes.append(proximo_candidato)
                indice_proximo_candidato += 1
                posicao_inicial_candidato = posicao_inicial_ultimo_candidato

                if posicao_final_ultimo_candidato > posicao_final_candidato:
                    posicao_final_candidato = posicao_final_ultimo_candidato
            else:
                break

        indice_candidato_analisado_na_lista = indice_proximo_candidato
        if len(sobreposicoes) > 1:
            for sobreposicao in sobreposicoes:
                lista_primos_com_sobreposicao.append(sobreposicao)
                # TODO: Remover antes da submissão
                with open(arquivo_primos_candidatos_sobreposicoes, "a", encoding='utf-8') as primo_candidato:
                    primo_candidato.write(f"{sobreposicao[0]}\n")

                # TODO: Remover antes da submissão
                with open(arquivo_de_posicoes_sobreposicoes, "a", encoding='utf-8') as posicoes_candidato:
                    posicoes_candidato.write(
                        f"{sobreposicao[1]}, {sobreposicao[2]}\n")
            # processa as sobreposicoes
            lista_bits = combinacoes_bits(len(sobreposicoes))
            lista_filtrada = obter_lista_filtrada(
                sobreposicoes, lista_bits)
            lista_primos_com_sobreposicao_filtrada = lista_primos_com_sobreposicao_filtrada + lista_filtrada
        else:
            sobreposicao = sobreposicoes[0]
            lista_primos_sem_sobreposicao.append(sobreposicao)
            # TODO: Remover antes da submissão
            with open(arquivo_primos_candidatos_sem_sobreposicoes, "a", encoding='utf-8') as primo_candidato:
                primo_candidato.write(f"{sobreposicao[0]}\n")

            # TODO: Remover antes da submissão
            with open(arquivo_de_posicoes_sem_sobreposicoes, "a", encoding='utf-8') as posicoes_candidato:
                posicoes_candidato.write(
                    f"{sobreposicao[1]}, {sobreposicao[2]}\n")

    indice_lista_filtrada = 0
    indice_lista_sem_sobreposicao = 0
    itens_na_lista_filtrada = len(lista_primos_com_sobreposicao_filtrada)
    itens_na_lista_sem_sobreposicao = len(lista_primos_sem_sobreposicao)

    lista_final = []

    while indice_lista_filtrada < itens_na_lista_filtrada \
            or indice_lista_sem_sobreposicao < itens_na_lista_sem_sobreposicao:

        item_filtrado = None
        item_sem_sobreposicao = None

        if indice_lista_filtrada < itens_na_lista_filtrada:
            item_filtrado = lista_primos_com_sobreposicao_filtrada[indice_lista_filtrada]

        if indice_lista_sem_sobreposicao < itens_na_lista_sem_sobreposicao:
            item_sem_sobreposicao = lista_primos_sem_sobreposicao[indice_lista_sem_sobreposicao]

        if item_filtrado == None and item_sem_sobreposicao != None:
            lista_final.append(item_sem_sobreposicao)
            indice_lista_sem_sobreposicao += 1

        if item_filtrado != None and item_sem_sobreposicao == None:
            lista_final.append(item_filtrado)
            indice_lista_filtrada += 1

        if item_filtrado != None and item_sem_sobreposicao != None:
            if item_filtrado[1] < item_sem_sobreposicao[1]:
                lista_final.append(item_filtrado)
                indice_lista_filtrada += 1
            else:
                lista_final.append(item_sem_sobreposicao)
                indice_lista_sem_sobreposicao += 1

    lista_primos_como_string = []
    for primo in lista_final:
        lista_primos_como_string.append(f"{primo[0]}")

    return lista_primos_como_string


def obter_lista_filtrada(lista_primos_com_sobreposicao, lista_bits):
    """obter_lista_filtrada(lista_primos_com_sobreposicao, lista_bits):
    Filtra a lista de primos, removendo a sobreposição

    Parâmetros:
    lista_primos_com_sobreposicao: Lista com os números primos, as posições de início e fim
    lista_bits: Lista de bits (0s e 1s) que indicam as combinações possíveis
                entre todos os números primos
    """
    lista_filtrada = []
    indice_da_melhor_combinacao = 0
    posicao_inicial_da_melhor_combinacao = 0
    posicao_mais_a_esquerda = sys.maxsize
    posicao_mais_a_direita = 0
    maior_comprimento = 0

    for primo in lista_primos_com_sobreposicao:
        posicao_inicial_referencia = primo[1]
        posicao_final_referencia = primo[2]

        if posicao_inicial_referencia < posicao_mais_a_esquerda:
            posicao_mais_a_esquerda = posicao_inicial_referencia

        if posicao_final_referencia > posicao_mais_a_direita:
            posicao_mais_a_direita = posicao_final_referencia

    for indice_combinacao, combinacao in enumerate(lista_bits):
        lista_temporaria = []

        for indice, bit in enumerate(combinacao):
            if bit == 1:
                lista_temporaria.append(
                    lista_primos_com_sobreposicao[indice])

        comprimento_lista_temporaria = len(lista_temporaria)

        if comprimento_lista_temporaria == 0:
            continue

        indice_externo = 0
        lista_valida = True
        while indice_externo < comprimento_lista_temporaria:
            indice_interno = indice_externo + 1
            primo_referencia = lista_temporaria[indice_externo]

            posicao_inicial_referencia = primo_referencia[1]
            posicao_final_referencia = primo_referencia[2]

            while indice_interno < comprimento_lista_temporaria:
                primo_interno = lista_temporaria[indice_interno]
                indice_interno += 1

                posicao_inicial_interno = primo_interno[1]
                posicao_final_interno = primo_interno[2]

                if posicao_inicial_interno >= posicao_inicial_referencia and posicao_inicial_interno <= posicao_final_referencia:
                    lista_valida = False
                    break

            indice_externo += 1

        comprimento_caracteres_lista = 0
        posicao_inicial_da_melhor_combinacao = posicao_mais_a_direita
        if lista_valida:
            for item in lista_temporaria:
                posicao_inicial_referencia = item[1]
                posicao_final_referencia = item[2]

                caracteres = posicao_final_referencia - posicao_inicial_referencia + 1
                comprimento_caracteres_lista += caracteres

            if comprimento_caracteres_lista > maior_comprimento:
                maior_comprimento = comprimento_caracteres_lista
                lista_filtrada = lista_temporaria.copy()
            elif comprimento_caracteres_lista == maior_comprimento:
                if posicao_mais_a_esquerda < posicao_inicial_da_melhor_combinacao:
                    lista_filtrada = lista_temporaria.copy()

    return lista_filtrada


def combinacoes_bits(tamanho):
    """combinacoes_bits(tamanho):
    Gera lista de combinações de bits para avaliar a superposição entre primos

    Parâmetro:
    tamanho: Número de bits para gerar a combinação
    """
    lista_combinacoes = []

    if tamanho == 1:
        lista = []
        lista.append(0)
        lista_combinacoes.append(lista)

        lista = []
        lista.append(1)
        lista_combinacoes.append(lista)
        return lista_combinacoes

    sub_combinacoes = combinacoes_bits(tamanho - 1)

    for sub_combinacao in sub_combinacoes:
        lista = []
        lista.append(0)
        lista = lista + sub_combinacao
        lista_combinacoes.append(lista)

        lista = []
        lista.append(1)
        lista = lista + sub_combinacao
        lista_combinacoes.append(lista)

    return lista_combinacoes


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
