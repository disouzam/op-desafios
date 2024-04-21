"""Busca primos em Pi
"""
import cProfile
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
    lista_primos_sobrepostos = []
    posicao_caractere_atual = 0
    posicao_inicial_candidato_anterior = 0
    posicao_final_candidato_anterior = 0
    ultima_posicao_sobreposicao = 0

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

            if e_primo(candidato):
                maior_primo = candidato
                numero_digitos_primo = comprimento

                posicao_inicial = posicao_caractere_atual
                posicao_final = posicao_caractere_atual + numero_digitos_primo - 1

                sobreposicao_entre_vizinhos = False

                # registra a posicao do primo inserido anteriormente e interrompe temporariamente para processar as sobreposicoes antes de prosseguir
                if posicao_inicial > 0 and \
                    (posicao_inicial <= posicao_final_candidato_anterior or
                        posicao_inicial <= ultima_posicao_sobreposicao):
                    sobreposicao_entre_vizinhos = True

                    if posicao_final > ultima_posicao_sobreposicao:
                        ultima_posicao_sobreposicao = posicao_final

                if not sobreposicao_entre_vizinhos:

                    lista_primos_sobrepostos = filtra_lista_primos_sobrepostos(
                        lista_primos_sobrepostos)
                    for primo in lista_primos_sobrepostos:
                        lista_primos.append(primo)

                    lista_primos_sobrepostos = []
                    lista_primos_sobrepostos.append(
                        (maior_primo, posicao_inicial, posicao_final))
                else:
                    lista_primos_sobrepostos.append(
                        (maior_primo, posicao_inicial, posicao_final))

                    # usa uma lista temporaria para ir enchendo até não encontrar mais sobreposicao

                    # se não houver sobreposicao, adiciona na lista de primos abaixo

                    # Atualiza posicoes do candidato anterior:
                posicao_inicial_candidato_anterior = posicao_inicial
                posicao_final_candidato_anterior = posicao_final

                if not sobreposicao_entre_vizinhos:
                    ultima_posicao_sobreposicao = posicao_final

                    # TODO: Remover antes da submissão
                    with open(arquivo_primos_candidatos, "a", encoding='utf-8') as primo_candidato:
                        primo_candidato.write("\n")

                    # TODO: Remover antes da submissão
                    with open(arquivo_de_posicoes, "a", encoding='utf-8') as posicoes_candidato:
                        posicoes_candidato.write("\n")

                # TODO: Remover antes da submissão
                with open(arquivo_primos_candidatos, "a", encoding='utf-8') as primo_candidato:
                    primo_candidato.write(str(maior_primo) + "\n")

                # TODO: Remover antes da submissão
                with open(arquivo_de_posicoes, "a", encoding='utf-8') as posicoes_candidato:
                    posicoes_candidato.write(
                        f"{posicao_inicial}, {posicao_final}\n")

            comprimento += 1

        posicao_caractere_atual += 1

    if posicao_caractere_atual == len(digitos):
        lista_primos_sobrepostos = filtra_lista_primos_sobrepostos(
            lista_primos_sobrepostos)
        for primo in lista_primos_sobrepostos:
            lista_primos.append(primo)

    # if len(lista_primos) > 1:
    #     raise RuntimeError(
    #         f"Foram encontrados {len(lista_primos)} primos para {len(digitos)} digitos.")

    lista_final = obtem_lista_sem_sobreposicoes(lista_primos)

    lista_primos_como_string = []
    for primo in lista_final:
        lista_primos_como_string.append(f"{primo[0]}")

    return lista_primos_como_string


def verifica_se_sublista_e_disjunta(sub_lista_abaixo_pivo):

    comprimento_sub_lista = len(sub_lista_abaixo_pivo)

    if comprimento_sub_lista == 0:
        return False

    sublista_e_disjunta = True
    if comprimento_sub_lista > 1:
        indice = 0
        while indice < comprimento_sub_lista - 1:
            atual = sub_lista_abaixo_pivo[indice]
            proximo = sub_lista_abaixo_pivo[indice + 1]

            if proximo[1] <= atual[2]:
                sublista_e_disjunta = False
                break

            indice += 1

    return sublista_e_disjunta


def localiza_pivos(lista_primos_sobrepostos):

    lista_pivos = []
    numero_primos_sobrepostos = len(lista_primos_sobrepostos)
    for indice, primo in enumerate(lista_primos_sobrepostos):
        pivo = primo
        contador = 0

        indice_interno = indice + 1
        while indice_interno < numero_primos_sobrepostos:
            posicao_inicial_interno = lista_primos_sobrepostos[indice_interno][1]
            posicao_final_interno = lista_primos_sobrepostos[indice_interno][2]

            if pivo[1] >= posicao_inicial_interno and pivo[2] <= posicao_final_interno:
                contador += 1
                pivo = lista_primos_sobrepostos[indice_interno]

            if posicao_inicial_interno >= pivo[1] and posicao_final_interno <= pivo[2]:
                contador += 1

            indice_interno += 1

        if contador > 0:
            lista_pivos.append(pivo)

    return lista_pivos


def remove_duplicatas(lista_pivos):

    num_pivos = len(lista_pivos)
    indice_externo = 0
    duplicatas = []
    lista_pivos_filtrada = []

    while indice_externo < num_pivos - 1:
        pivo_externo = lista_pivos[indice_externo]

        indice_interno = indice_externo + 1

        duplicata_encontrada = False
        while indice_interno < num_pivos:
            pivo_interno = lista_pivos[indice_interno]
            if pivo_interno == pivo_externo:
                duplicata_encontrada = True
                duplicatas.append(indice_interno)
            indice_interno += 1

        if indice_externo not in duplicatas:
            lista_pivos_filtrada.append(pivo_externo)

        if indice_externo == num_pivos - 2 and not duplicata_encontrada:
            lista_pivos_filtrada.append(pivo_interno)
        indice_externo += 1

    if num_pivos > 1:
        lista_pivos = lista_pivos_filtrada

    return lista_pivos


def filtra_lista_primos_sobrepostos(lista_primos_sobrepostos):

    lista_primos_sobrepostos_filtrada = []
    lista_pivos = []

    if len(lista_primos_sobrepostos) == 0:
        return lista_primos_sobrepostos_filtrada
    elif len(lista_primos_sobrepostos) == 1:
        return lista_primos_sobrepostos

    lista_pivos = localiza_pivos(lista_primos_sobrepostos)
    lista_pivos = remove_duplicatas(lista_pivos)

    # Terceiro passe: processa os pivôs
    sub_lista_abaixo_pivo = []

    for indice_pivo, pivo in enumerate(lista_pivos):
        posicao_pivo_lista_original = lista_primos_sobrepostos.index(pivo)
        if pivo in sub_lista_abaixo_pivo:
            continue

        sub_lista_abaixo_pivo = []
        for indice, primo in enumerate(lista_primos_sobrepostos):
            if primo != pivo and primo[1] >= pivo[1] and primo[2] <= pivo[2]:
                sub_lista_abaixo_pivo.append(primo)
            elif indice < posicao_pivo_lista_original and \
                    primo not in lista_primos_sobrepostos_filtrada:
                lista_primos_sobrepostos_filtrada.append(primo)

        sublista_e_disjunta = verifica_se_sublista_e_disjunta(
            sub_lista_abaixo_pivo)

        comprimento_pivo = pivo[2] - pivo[1] + 1

        if sublista_e_disjunta:
            total_caracteres = 0

            for primo in sub_lista_abaixo_pivo:
                total_caracteres += primo[2] - primo[1] + 1

            if total_caracteres == comprimento_pivo:
                for primo in sub_lista_abaixo_pivo:
                    lista_primos_sobrepostos_filtrada.append(primo)
            else:
                lista_primos_sobrepostos_filtrada.append(pivo)
        else:
            # busca encontrar uma lista disjunta
            lista_bits = combinacoes_bits(len(sub_lista_abaixo_pivo))
            lista_disjunta_encontrada = False

            for combinacao in lista_bits:
                lista_temporaria = []
                total_caracteres = 0

                for indice, primo in enumerate(sub_lista_abaixo_pivo):
                    if combinacao[indice] == 1:
                        lista_temporaria.append(primo)
                        total_caracteres += primo[2] - primo[1] + 1

                lista_temporaria_e_disjunta = verifica_se_sublista_e_disjunta(
                    lista_temporaria)

                if lista_temporaria_e_disjunta and total_caracteres == comprimento_pivo:
                    lista_disjunta_encontrada = True
                    break

            if lista_disjunta_encontrada:
                for primo in lista_temporaria:
                    lista_primos_sobrepostos_filtrada.append(primo)
            else:
                # avalia se há interseção com pivos adjacentes
                # busca encontrar uma lista disjunta
                lista_estendida = sub_lista_abaixo_pivo
                maximo_caracteres = 0
                indice_melhor_combinacao = 0

                lista_com_anterior = []
                if indice_pivo > 0:
                    lista_com_anterior.append(lista_pivos[indice_pivo - 1])
                    lista_com_anterior.append(pivo)

                    if lista_pivos[indice_pivo - 1] not in lista_estendida and \
                            not verifica_se_sublista_e_disjunta(lista_com_anterior):
                        lista_estendida = [
                            lista_pivos[indice_pivo - 1]] + lista_estendida

                lista_com_seguinte = []
                if indice_pivo < len(lista_pivos) - 1:
                    lista_com_seguinte.append(pivo)
                    lista_com_seguinte.append(lista_pivos[indice_pivo + 1])

                    if lista_pivos[indice_pivo + 1] not in lista_estendida and \
                            not verifica_se_sublista_e_disjunta(lista_com_seguinte):
                        lista_estendida = lista_estendida + [
                            lista_pivos[indice_pivo + 1]]

                lista_bits = combinacoes_bits(len(lista_estendida))
                lista_disjunta_encontrada = False

                for indice_combinacao, combinacao in enumerate(lista_bits):
                    lista_temporaria = []
                    total_caracteres = 0

                    for indice, primo in enumerate(lista_estendida):
                        if combinacao[indice] == 1:
                            lista_temporaria.append(primo)
                            total_caracteres += primo[2] - primo[1] + 1

                    lista_temporaria_e_disjunta = verifica_se_sublista_e_disjunta(
                        lista_temporaria)

                    if lista_temporaria_e_disjunta and total_caracteres > maximo_caracteres:
                        lista_disjunta_encontrada = True
                        maximo_caracteres = total_caracteres
                        indice_melhor_combinacao = indice_combinacao

                if lista_disjunta_encontrada and maximo_caracteres > comprimento_pivo:
                    combinacao = lista_bits[indice_melhor_combinacao]
                    for indice, primo in enumerate(lista_estendida):
                        if combinacao[indice] == 1:
                            lista_primos_sobrepostos_filtrada.append(primo)
                else:
                    lista_primos_sobrepostos_filtrada.append(pivo)

    if len(lista_pivos) > 0:
        for indice_pivo, pivo in enumerate(lista_pivos):
            posicao_pivo_lista_original = lista_primos_sobrepostos.index(pivo)
            for indice, primo in enumerate(lista_primos_sobrepostos):
                if indice > posicao_pivo_lista_original and primo not in lista_primos_sobrepostos_filtrada \
                        and primo not in lista_pivos:
                    lista_primos_sobrepostos_filtrada.append(primo)
    elif not verifica_se_sublista_e_disjunta(lista_primos_sobrepostos):
        lista_bits = combinacoes_bits(len(lista_primos_sobrepostos))
        lista_disjunta_encontrada = False
        maximo_caracteres = 0
        indice_melhor_combinacao = 0

        for indice_combinacao, combinacao in enumerate(lista_bits):
            lista_temporaria = []
            total_caracteres = 0

            for indice, primo in enumerate(lista_primos_sobrepostos):
                if combinacao[indice] == 1:
                    lista_temporaria.append(primo)
                    total_caracteres += primo[2] - primo[1] + 1

            lista_temporaria_e_disjunta = verifica_se_sublista_e_disjunta(
                lista_temporaria)

            if lista_temporaria_e_disjunta and total_caracteres > maximo_caracteres:
                lista_disjunta_encontrada = True
                maximo_caracteres = total_caracteres
                indice_melhor_combinacao = indice_combinacao

        if lista_disjunta_encontrada and maximo_caracteres > comprimento_pivo:
            combinacao = lista_bits[indice_melhor_combinacao]
            for indice, primo in enumerate(lista_primos_sobrepostos):
                if combinacao[indice] == 1:
                    lista_primos_sobrepostos_filtrada.append(primo)

    # Quarto passe: Filtra os primos
    lista_primos_filtrada = remove_duplicatas(
        lista_primos_sobrepostos_filtrada)

    # Chamada recursiva
    if not verifica_se_sublista_e_disjunta(lista_primos_filtrada):
        lista_primos_filtrada = filtra_lista_primos_sobrepostos(
            lista_primos_filtrada)

    lista_primos_sobrepostos_filtrada = lista_primos_filtrada

    return lista_primos_sobrepostos_filtrada


def obtem_lista_sem_sobreposicoes(lista_primos):
    """
    """

    maximo_comprimento_sobreposicoes = 0

    # TODO: Remover antes da submissão
    arquivo_primos_candidatos_sem_sobreposicoes = "primos_candidatos_sem_sobreposicoes.txt"
    arquivo_primos_candidatos_sobreposicoes = "primos_candidatos_sobreposicoes.txt"
    arquivo_de_posicoes_sobreposicoes = "posicoes_sobreposicoes.txt"
    arquivo_de_posicoes_sem_sobreposicoes = "posicoes_sem_sobreposicoes.txt"

    if os.path.exists(arquivo_de_posicoes_sem_sobreposicoes):
        os.remove(arquivo_de_posicoes_sem_sobreposicoes)

    if os.path.exists(arquivo_de_posicoes_sobreposicoes):
        os.remove(arquivo_de_posicoes_sobreposicoes)

    if os.path.exists(arquivo_primos_candidatos_sem_sobreposicoes):
        os.remove(arquivo_primos_candidatos_sem_sobreposicoes)

    if os.path.exists(arquivo_primos_candidatos_sobreposicoes):
        os.remove(arquivo_primos_candidatos_sobreposicoes)

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
            if len(sobreposicoes) > maximo_comprimento_sobreposicoes:
                maximo_comprimento_sobreposicoes = len(sobreposicoes)
                print(
                    f"Máximo comprimento das sobreposições: {len(sobreposicoes)}")
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

    return lista_final


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

# TODO: Remover antes da submissão do PR


def debugger_is_active() -> bool:
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
