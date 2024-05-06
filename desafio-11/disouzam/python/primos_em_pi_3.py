"""Terceira implementação dos primos em Pi
"""
from __future__ import annotations
import cProfile
from ctypes import ArgumentError
import os
import sys
from typing import cast
import datetime
from os.path import join
from collections import Counter


from numeros_primos import primo, e_primo
from manipulacao_de_arquivos import ler_primos_do_arquivo, get_file_name_without_extension
from lista_numeros_primos import lista_num_primos
from peneira_de_eratosthenes import primos_ate_n


def main(args) -> None:
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
        file_name = get_file_name_without_extension(arquivo_com_numero_pi)
        digitos_parte_fracionaria = ler_primos_do_arquivo(
            arquivo_com_numero_pi, file_name)

    if nargs >= 2:
        mensagem = f"Você informou um número excessivo de argumentos({nargs}). "
        mensagem += "Apenas um argumento que aponte o caminho (relativo ou absoluto) "
        mensagem += "do arquivo contendo o número Pi com algumas casas decimais especificadas"
        mensagem += "e o número a ser convertido é necessário."
        print(mensagem)

        mensagem2 = "Deseja prosseguir ignorando os demais argumentos? (S para Sim e N para não)"
        escolha_do_usuario = input(mensagem2)

        if escolha_do_usuario.lower() != "s":
            print("Programa abortado.")
            return

    primos_na_parte_fracionaria = obtem_primos_de_lista_de_inteiros(
        digitos_parte_fracionaria, file_name)

    # TODO: Remover antes da submissão do PR
    for numero_primo in primos_na_parte_fracionaria:
        if not e_primo(int(numero_primo)):
            raise ArgumentError(f"Primo inválido: {primo}.")

    caracteres_concatenados = "".join(primos_na_parte_fracionaria)
    print(caracteres_concatenados)

    diretorio_raiz = os.path.dirname(os.path.realpath(__file__))

    arquivo_de_resultado = f"{file_name}-resultado_primos_3.txt"
    arquivo_de_resultado = join("saidas", arquivo_de_resultado)
    arquivo_de_resultado = join(diretorio_raiz, arquivo_de_resultado)
    if os.path.isfile(arquivo_de_resultado):
        os.remove(arquivo_de_resultado)

    with open(arquivo_de_resultado, "w", encoding='utf-8') as arquivo:
        arquivo.write(caracteres_concatenados)


def imprimir_contagem_de_listas(caminho, contador: Counter):
    # TODO: Remover antes da submissão
    with open(caminho, "w", encoding='utf-8') as arquivo:
        for tamanho, ocorrencia in contador.items():
            arquivo.write(f"{tamanho}: {ocorrencia}\n")


def obtem_primos_de_lista_de_inteiros(digitos: list[str], file_name) -> list[str]:
    """obtem_primos_de_lista_de_inteiros(digitos: list[str]) -> list[str]:
    Obtém uma lista de primos a partir de uma lista ordenada de dígitos

    Parâmetro:
    digitos: lista de dígitos
    """
    lista_primos = lista_num_primos()
    lista_temporaria = lista_num_primos()
    lista_de_transicao = lista_num_primos()
    maior_lista_primos_encontrada = lista_num_primos()
    primo_anterior: None | primo = None
    maximo_indice_final = 0

    diretorio_raiz = os.path.dirname(os.path.realpath(__file__))

    # TODO: Remover antes da submissão do PR
    arquivo_primos_candidatos = f"{file_name}-primos_candidatos_primos_3.txt"
    arquivo_primos_candidatos = join("saidas", arquivo_primos_candidatos)
    arquivo_primos_candidatos = join(diretorio_raiz, arquivo_primos_candidatos)

    contagem_de_tamanho_de_listas = f"{file_name}-contagem_de_tamanho_de_listas_primos_3.txt"
    contagem_de_tamanho_de_listas = join(
        "saidas", contagem_de_tamanho_de_listas)
    contagem_de_tamanho_de_listas = join(
        diretorio_raiz, contagem_de_tamanho_de_listas)

    ocorrencias_tamanho_de_listas = []
    filtragens_evitadas = 0
    maximo_filtragens = 0

    lista_de_primos_Erastothenes = primos_ate_n(9973)

    # TODO: Remover antes da submissão do PR
    if os.path.exists(arquivo_primos_candidatos):
        os.remove(arquivo_primos_candidatos)

    if os.path.exists(contagem_de_tamanho_de_listas):
        os.remove(contagem_de_tamanho_de_listas)

    # Levanta todos os primos existentes, não checando sobreposição
    for posicao_caractere_atual in range(0, len(digitos)):
        for comprimento in range(1, 5):
            inicio = posicao_caractere_atual
            fim = posicao_caractere_atual + comprimento - 1

            if fim > len(digitos) - 1:
                continue

            candidato = int("".join(digitos[inicio:fim + 1]))

            if candidato == 0:
                break

            if candidato in lista_de_primos_Erastothenes:
                sobreposicao_entre_vizinhos = False
                primo_atual = primo(candidato, inicio, fim)

                if primo_anterior is None:
                    primo_anterior = primo_atual

                if lista_temporaria.size() > 0:
                    # Sobreposição entre vizinhos imediatos
                    if primo_anterior != primo_atual and \
                            primo_atual.sobrepoe_outro_primo_parcialmente(
                                cast(primo, primo_anterior)
                            ):
                        sobreposicao_entre_vizinhos = True

                    # Sobreposição entre o primo atual e um dos primos mais longos
                    # dessa sequência contígua
                    if primo_atual.inicio <= maximo_indice_final or primo_atual.fim <= maximo_indice_final:
                        sobreposicao_entre_vizinhos = True

                    # Atualiza o maior índice atingido nessa sequência contígua
                    if primo_atual.fim > maximo_indice_final:
                        maximo_indice_final = primo_atual.fim

                primo_anterior = primo_atual

                if not sobreposicao_entre_vizinhos:
                    print(
                        f"\n\n\tTamanho da lista: {lista_temporaria.size()}")
                    ocorrencias_tamanho_de_listas.append(
                        lista_temporaria.size())

                    comprimento_lista_primos_atual = lista_primos.comprimento()

                    lista_temporaria.filtrar_primos()

                    if lista_de_transicao.size() == 0:
                        lista_de_transicao = lista_temporaria.copy()

                    contador = Counter(ocorrencias_tamanho_de_listas)

                    if lista_de_transicao.checar_se_combinacao_seria_contigua(lista_temporaria):
                        for numero_primo in lista_temporaria:
                            ultimo_primo = lista_de_transicao[-1]
                            if ultimo_primo.fim + 1 == numero_primo.inicio:
                                lista_de_transicao.append(numero_primo)
                    else:
                        lista_de_transicao.clear()
                        lista_de_transicao = lista_temporaria.copy()

                    imprimir_contagem_de_listas(
                        contagem_de_tamanho_de_listas, contador)

                    print(f"Posição atual: {posicao_caractere_atual}")
                    print(
                        f"Comprimento da lista atual: {comprimento_lista_primos_atual}")

                    combinacao_seria_contigua = lista_primos.checar_se_combinacao_seria_contigua(
                        lista_de_transicao)

                    if combinacao_seria_contigua:
                        maior_lista_primos_encontrada = lista_primos.copy()

                        for numero_primo in lista_de_transicao:
                            maior_lista_primos_encontrada.append(numero_primo)

                    maior_lista_primos_encontrada_e_contigua = maior_lista_primos_encontrada.contigua()
                    maior_lista_primos_encontrada_comprimento = maior_lista_primos_encontrada.comprimento()

                    lista_transicao_e_contigua = lista_de_transicao.contigua()
                    lista_transicao_comprimento = lista_de_transicao.comprimento()

                    if maior_lista_primos_encontrada_e_contigua:
                        print(
                            f"Comprimento da lista maior_lista_primos_encontrada: {maior_lista_primos_encontrada_comprimento}")

                    if lista_transicao_e_contigua:
                        print(
                            f"Comprimento da lista lista_transicao: {lista_transicao_comprimento}\n")

                    if maior_lista_primos_encontrada_e_contigua and maior_lista_primos_encontrada_comprimento > comprimento_lista_primos_atual:
                        print(
                            f"Lista atual: {lista_primos.lista_de_primos_concatenada()}")
                        print(
                            f"Lista substituta: {maior_lista_primos_encontrada.lista_de_primos_concatenada()}\n\n")
                        lista_primos.clear()
                        # TODO: Remover antes da submissão
                        if os.path.exists(arquivo_primos_candidatos):
                            os.remove(arquivo_primos_candidatos)

                        with open(arquivo_primos_candidatos, "w", encoding='utf-8') as primo_candidato:
                            for numero_primo in maior_lista_primos_encontrada:
                                lista_primos.append(numero_primo)

                                primo_candidato.write(f"{numero_primo}\n")
                    elif lista_transicao_e_contigua and lista_transicao_comprimento > comprimento_lista_primos_atual:
                        print(
                            f"Lista atual: {lista_primos.lista_de_primos_concatenada()}")
                        print(
                            f"Lista substituta: {lista_de_transicao.lista_de_primos_concatenada()}\n\n")
                        lista_primos.clear()
                        # TODO: Remover antes da submissão
                        if os.path.exists(arquivo_primos_candidatos):
                            os.remove(arquivo_primos_candidatos)

                        with open(arquivo_primos_candidatos, "w", encoding='utf-8') as primo_candidato:
                            for numero_primo in lista_de_transicao:
                                lista_primos.append(numero_primo)

                                primo_candidato.write(f"{numero_primo}\n")
                    else:
                        print("\t\t\tNÃO TROCOU")

                    lista_temporaria.clear()
                    lista_temporaria.append(primo_atual)
                    maximo_indice_final = lista_temporaria.maior_posicao
                else:
                    lista_temporaria.append(primo_atual)

    if posicao_caractere_atual == len(digitos) - 1:
        print(
            f"\n\n\tTamanho da lista: {lista_temporaria.size()}")
        ocorrencias_tamanho_de_listas.append(
            lista_temporaria.size())

        comprimento_lista_primos_atual = lista_primos.comprimento()

        lista_temporaria.filtrar_primos()

        if lista_de_transicao.size() == 0:
            lista_de_transicao = lista_temporaria.copy()

        contador = Counter(ocorrencias_tamanho_de_listas)

        if lista_de_transicao.checar_se_combinacao_seria_contigua(lista_temporaria):
            for numero_primo in lista_temporaria:
                ultimo_primo = lista_de_transicao[-1]
                if ultimo_primo.fim + 1 == numero_primo.inicio:
                    lista_de_transicao.append(numero_primo)
        else:
            lista_de_transicao.clear()
            lista_de_transicao = lista_temporaria.copy()

        imprimir_contagem_de_listas(
            contagem_de_tamanho_de_listas, contador)

        print(f"Posição atual: {posicao_caractere_atual}")
        print(
            f"Comprimento da lista atual: {comprimento_lista_primos_atual}")

        combinacao_seria_contigua = lista_primos.checar_se_combinacao_seria_contigua(
            lista_de_transicao)

        if combinacao_seria_contigua:
            maior_lista_primos_encontrada = lista_primos.copy()

            for numero_primo in lista_de_transicao:
                maior_lista_primos_encontrada.append(numero_primo)

        maior_lista_primos_encontrada_e_contigua = maior_lista_primos_encontrada.contigua()
        maior_lista_primos_encontrada_comprimento = maior_lista_primos_encontrada.comprimento()

        lista_transicao_e_contigua = lista_de_transicao.contigua()
        lista_transicao_comprimento = lista_de_transicao.comprimento()

        if maior_lista_primos_encontrada_e_contigua:
            print(
                f"Comprimento da lista maior_lista_primos_encontrada: {maior_lista_primos_encontrada_comprimento}")

        if lista_transicao_e_contigua:
            print(
                f"Comprimento da lista lista_transicao: {lista_transicao_comprimento}\n")

        if maior_lista_primos_encontrada_e_contigua and maior_lista_primos_encontrada_comprimento > comprimento_lista_primos_atual:
            print(
                f"Lista atual: {lista_primos.lista_de_primos_concatenada()}")
            print(
                f"Lista substituta: {maior_lista_primos_encontrada.lista_de_primos_concatenada()}\n\n")
            lista_primos.clear()
            # TODO: Remover antes da submissão
            if os.path.exists(arquivo_primos_candidatos):
                os.remove(arquivo_primos_candidatos)

            with open(arquivo_primos_candidatos, "w", encoding='utf-8') as primo_candidato:
                for numero_primo in maior_lista_primos_encontrada:
                    lista_primos.append(numero_primo)

                    primo_candidato.write(f"{numero_primo}\n")
        elif lista_transicao_e_contigua and lista_transicao_comprimento > comprimento_lista_primos_atual:
            print(
                f"Lista atual: {lista_primos.lista_de_primos_concatenada()}")
            print(
                f"Lista substituta: {lista_de_transicao.lista_de_primos_concatenada()}\n\n")
            lista_primos.clear()
            # TODO: Remover antes da submissão
            if os.path.exists(arquivo_primos_candidatos):
                os.remove(arquivo_primos_candidatos)

            with open(arquivo_primos_candidatos, "w", encoding='utf-8') as primo_candidato:
                for numero_primo in lista_de_transicao:
                    lista_primos.append(numero_primo)

                    primo_candidato.write(f"{numero_primo}\n")
        else:
            print("\t\t\tNÃO TROCOU")

        lista_temporaria.clear()
        lista_temporaria.append(primo_atual)
        maximo_indice_final = lista_temporaria.maior_posicao

    # TODO: Remover antes da submissão do PR
    arquivo_filtragens_evitadas = f"{file_name}-filtragens_evitadas_primos_3.txt"
    arquivo_filtragens_evitadas = join("saidas", arquivo_filtragens_evitadas)
    arquivo_filtragens_evitadas = join(
        diretorio_raiz, arquivo_filtragens_evitadas)

    with open(arquivo_filtragens_evitadas, 'w', encoding='utf-8') as arquivo:
        arquivo.write(f"Filtragens evitadas: {filtragens_evitadas}\n")
        arquivo.write(f"Total de filtragens: {maximo_filtragens}\n")

    del lista_temporaria, candidato, comprimento, inicio, fim, posicao_caractere_atual
    del primo_anterior, primo_atual, sobreposicao_entre_vizinhos, numero_primo

    if not lista_primos.disjunta():
        raise ArgumentError("Lista de primos inválida.")

    lista_primos_como_string = lista_primos.lista_de_primos_como_string()
    return lista_primos_como_string


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
