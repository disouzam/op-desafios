"""Terceira implementação dos primos em Pi
"""
from __future__ import annotations
import cProfile
from ctypes import ArgumentError
import math
import os
import sys
from typing import cast
import pdb


from numeros_primos import primo, e_primo
from manipulacao_de_arquivos import ler_primos_do_arquivo
from geracao_lista_bits import combinacoes_bits


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
        digitos_parte_fracionaria = ler_primos_do_arquivo(
            arquivo_com_numero_pi)

    if nargs >= 2:
        mensagem = f"Você informou um número excessivo de argumentos ({nargs}). "
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
        digitos_parte_fracionaria)

    # TODO: Remover antes da submissão do PR
    for numero_primo in primos_na_parte_fracionaria:
        if not e_primo(int(numero_primo)):
            raise ArgumentError(f"Primo inválido: {primo}.")

    caracteres_concatenados = "".join(primos_na_parte_fracionaria)
    print(caracteres_concatenados)

    arquivo_de_resultado = "resultado_primos_3.txt"
    if os.path.isfile(arquivo_de_resultado):
        os.remove(arquivo_de_resultado)

    with open(arquivo_de_resultado, "w", encoding='utf-8') as arquivo:
        arquivo.write(caracteres_concatenados)


def obtem_primos_de_lista_de_inteiros(digitos: list[str]) -> list[str]:
    """obtem_primos_de_lista_de_inteiros(digitos: list[str]) -> list[str]:
    Obtém uma lista de primos a partir de uma lista ordenada de dígitos

    Parâmetro:
    digitos: lista de dígitos
    """
    lista_primos: list[primo] = []
    lista_temporaria: list[primo] = []
    primo_anterior: None | primo = None
    maximo_indice_final = 0

    # TODO: Remover antes da submissão do PR
    arquivo_primos_candidatos = "primos_candidatos_primos_3.txt"

    # TODO: Remover antes da submissão do PR
    if os.path.exists(arquivo_primos_candidatos):
        os.remove(arquivo_primos_candidatos)

    # Levanta todos os primos existentes, não checando sobreposição
    for posicao_caractere_atual in range(0, len(digitos)):
        for comprimento in range(1, 5):
            inicio = posicao_caractere_atual
            fim = posicao_caractere_atual + comprimento - 1

            if fim > len(digitos) - 1:
                continue

            candidato = int("".join(digitos[inicio:fim + 1]))

            if e_primo(candidato):
                sobreposicao_entre_vizinhos = False
                primo_atual = primo(candidato, inicio, fim)

                if primo_anterior is None:
                    primo_anterior = primo_atual

                if inicio > 0:
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
                    lista_temporaria = filtrar_primos_disjuntos(
                        lista_temporaria)

                    # # TODO: Remover antes da submissão
                    # print(
                    #     f"{primo_atual.inicio} - Tamanho da lista temporaria: {len(lista_temporaria)}")

                    if len(lista_primos) > 0:
                        # TODO: Remover antes da submissão
                        with open(arquivo_primos_candidatos, "a", encoding='utf-8') as primo_candidato:
                            primo_candidato.write("\n")

                    for numero_primo in lista_temporaria:
                        lista_primos.append(numero_primo)

                        # TODO: Remover antes da submissão
                        with open(arquivo_primos_candidatos, "a", encoding='utf-8') as primo_candidato:
                            primo_candidato.write(f"{numero_primo}\n")

                    lista_temporaria.clear()
                    lista_temporaria.append(primo_atual)
                    maximo_indice_final = primo_atual.fim
                else:
                    lista_temporaria.append(primo_atual)

    if posicao_caractere_atual == len(digitos) - 1:
        lista_temporaria = filtrar_primos_disjuntos(
            lista_temporaria)

        # # TODO: Remover antes da submissão
        # print(
        #     f"{primo_atual.inicio} - Tamanho da lista temporaria: {len(lista_temporaria)}")

        # TODO: Remover antes da submissão
        with open(arquivo_primos_candidatos, "a", encoding='utf-8') as primo_candidato:
            primo_candidato.write("\n")

        for numero_primo in lista_temporaria:
            lista_primos.append(numero_primo)

            # TODO: Remover antes da submissão
            with open(arquivo_primos_candidatos, "a", encoding='utf-8') as primo_candidato:
                primo_candidato.write(f"{numero_primo}\n")

    del lista_temporaria, candidato, comprimento, inicio, fim, posicao_caractere_atual
    del primo_anterior, primo_atual, sobreposicao_entre_vizinhos, numero_primo

    if not lista_e_disjunta(lista_primos):
        raise ArgumentError(f"Lista de primos inválida.")

    lista_primos_como_string: list[str] = []
    for primo_atual in lista_primos:
        lista_primos_como_string.append(f"{primo_atual.numero_primo}")

    return lista_primos_como_string


def lista_e_disjunta(lista: list[primo]) -> bool:
    """lista_e_disjunta(lista: list[primo]) -> bool:
    Checa se uma lista é disjunta ou não
    """
    for indice in range(0, len(lista) - 1):
        primo_atual = lista[indice]
        primo_seguinte = lista[indice + 1]

        if primo_atual.sobrepoe_outro_primo_parcialmente(primo_seguinte):
            return False

    return True


def filtrar_primos_disjuntos(primos: list[primo]) -> list[primo]:
    """filtrar_primos_disjuntos(lista_temporaria)
    Processa uma lista temporaria de primos com sobreposicao e mantem os primos disjuntos
    quando existir ou devolve a lista original
    """
    # Razões para não seguir com o processamento
    if len(primos) == 0:
        return primos

    # TODO: Remover antes da submissão do PR
    # print(
    #     f"{primos[0].inicio} - Tamanho da lista temporaria: {len(primos)}")

    sub_listas: list[list[primo]] = [[]]
    maiores_primos: list[list[primo]] = [[]]

    # Inicia a formação das sublistas
    primos_temporarios = primos.copy()

    indice_sublistas = 0
    while len(primos_temporarios) > 0:
        primo_candidato = primos_temporarios[0]
        primos_temporarios.remove(primo_candidato)

        if indice_sublistas > 0:
            sub_listas.append([])
            maiores_primos.append([])

        sub_listas[indice_sublistas].append(primo_candidato)
        maiores_primos[indice_sublistas].append(primo_candidato)
        maior_primo_atual = primo_candidato

        indice_interno = 0
        while indice_interno < len(primos_temporarios):
            novo_candidato_a_maior_primo = primos_temporarios[indice_interno]
            if novo_candidato_a_maior_primo.sobrepoe_outro_primo_completamente(maior_primo_atual):
                # Troca de maior número primo
                sub_listas[indice_sublistas].append(
                    novo_candidato_a_maior_primo)
                maiores_primos[indice_sublistas].clear()
                maiores_primos[indice_sublistas].append(
                    novo_candidato_a_maior_primo)
                primos_temporarios.remove(novo_candidato_a_maior_primo)
                maior_primo_atual = novo_candidato_a_maior_primo
                indice_interno = 0
            elif maior_primo_atual.sobrepoe_outro_primo_completamente(novo_candidato_a_maior_primo):
                # Adiciona nov primo à sublista atual
                sub_listas[indice_sublistas].append(
                    novo_candidato_a_maior_primo)
                primos_temporarios.remove(novo_candidato_a_maior_primo)
                indice_interno = 0
            else:
                # Avança para o próximo índice para atingir o final da lista de primos temporários
                indice_interno += 1

        indice_sublistas += 1

    numero_sublistas = len(sub_listas)
    indice_sublistas = 0
    lista_temporaria: list[primo] = []
    while len(primos) > 0 and indice_sublistas < numero_sublistas:
        del lista_temporaria
        lista_temporaria = sub_listas[indice_sublistas].copy()

        # TODO: Remover antes da submissão do PR
        # print(
        #     f"Chamada à filtra_primos_disjuntos_de_lista_com_sobreposicao_total: {len(lista_temporaria)} elementos")
        lista_temporaria = filtra_primos_disjuntos_de_lista_com_sobreposicao_total(
            lista_temporaria, maiores_primos[indice_sublistas][0])

        sub_listas[indice_sublistas] = lista_temporaria
        indice_sublistas += 1

    # Mesclar as sublistas
    lista_temporaria: list[primo] = []
    numero_sublistas = len(sub_listas)
    indice_sublistas = 0
    while len(primos) > 0 and indice_sublistas < numero_sublistas:
        lista_temporaria.extend(sub_listas[indice_sublistas])
        indice_sublistas += 1

    # Ordenar as sublistas
    quantidade_primos = len(lista_temporaria)
    for indice_externo in range(0, quantidade_primos - 1):
        primo_externo = lista_temporaria[indice_externo]
        for indice_interno in range(indice_externo + 1, quantidade_primos):
            primo_interno = lista_temporaria[indice_interno]
            if primo_interno.inicio < primo_externo.inicio or \
                (primo_interno.inicio == primo_externo.inicio
                    and primo_interno.numero_caracteres() < primo_externo.numero_caracteres()):
                lista_temporaria[indice_externo] = primo_interno
                lista_temporaria[indice_interno] = primo_externo

    # TODO: Remover antes da submissão do PR
    # print(
    #     f"Chamada à filtra_primos_sobrepostos: {len(lista_temporaria)} elementos")
    lista_temporaria = filtra_primos_sobrepostos(lista_temporaria)

    return lista_temporaria


def filtra_primos_sobrepostos(primos: list[primo]) -> list[primo]:
    """filtra_primos_sobrepostos(primos: list[primo]) -> list[primo]:
    Usando permutação, obtém a maior lista possível sem sobreposicao
    """
    tamanho_lista_primos = len(primos)

    # TODO: Remover antes da submissão do PR
    # print("Início do cálculo de combinacoes")
    if tamanho_lista_primos == 0:
        return primos

    # TODO: Remover antes da submissão do PR
    # print("Fim do cálculo de combinacoes")

    maior_comprimento_obtido = 0
    melhor_combinacao: list[primo] = []
    lista_disjunta_encontrada = False
    lista_temporaria: list[primo] = []

    primeira_posicao = primos[0].inicio
    ultima_posicao = primos[0].fim

    for numero_primo in primos:
        if numero_primo.inicio < primeira_posicao:
            primeira_posicao = numero_primo.inicio
        if numero_primo.fim > ultima_posicao:
            ultima_posicao = numero_primo.fim

    maior_comprimento_possivel = ultima_posicao - primeira_posicao + 1

    numero_combinacoes = math.pow(2, tamanho_lista_primos)

    if tamanho_lista_primos > 15:
        divisoes = 10000
    else:
        divisoes = 10

    intervalo = int(numero_combinacoes / divisoes)
    contador = 0
    indice_externo = 0

    # TODO: Possível explosão combinatória que precisa ser substituída - Primos sobrepostos
    for combinacao in combinacoes_bits(tamanho_lista_primos):
        indice_externo += 1
        contador += 1

        # TODO: Remover antes da submissão do PR
        # if contador == intervalo:
        #     print(f"\t\t{indice_externo}/{numero_combinacoes}")
        #     contador = 0

        del lista_temporaria
        lista_temporaria: list[primo] = []
        total_caracteres = 0

        primo_anterior: None | primo = None
        sobreposicao_encontrada = False

        for indice, numero_primo in enumerate(primos):
            if combinacao[indice] == 1:
                if len(lista_temporaria) >= 1:
                    primo_anterior_casted = cast(primo, primo_anterior)
                    if numero_primo.sobrepoe_outro_primo_parcialmente(primo_anterior_casted) \
                        or primo_anterior_casted.sobrepoe_outro_primo_parcialmente(
                            numero_primo):
                        # # TODO: Remover antes da submissão do PR
                        # print("Saída prematura do loop em filtra_primos_sobrepostos")
                        sobreposicao_encontrada = True
                        lista_temporaria.clear()
                        break
                primo_anterior = numero_primo

                lista_temporaria.append(numero_primo)
                total_caracteres += numero_primo.numero_caracteres()

        if sobreposicao_encontrada:
            sobreposicao_encontrada = False
            lista_temporaria.clear()
            continue

        if total_caracteres < maior_comprimento_obtido:
            lista_temporaria.clear()
            continue

        lista_temporaria_e_disjunta = lista_e_disjunta(lista_temporaria)

        if lista_temporaria_e_disjunta and total_caracteres > maior_comprimento_obtido:
            lista_disjunta_encontrada = True
            melhor_combinacao = lista_temporaria.copy()
            maior_comprimento_obtido = total_caracteres

            if maior_comprimento_obtido == maior_comprimento_possivel:
                # print(
                #     f"Terminou após {100 *round(indice_externo/numero_combinacoes,2)}% completados...")
                break

    if lista_disjunta_encontrada:
        return melhor_combinacao
    else:
        return primos


def filtra_primos_disjuntos_de_lista_com_sobreposicao_total(primos: list[primo], maior_primo: primo) -> list[primo]:
    """filtra_primos_disjuntos_de_lista_com_sobreposicao_total(primos: list[primo], maior_primo: primo) -> list[primo]:
    Filtra uma lista de primos com sobreposicao total e devolve uma
    lista de itens disjuntos, se existir

    Parâmetros:
    primos: Lista de números primos
    maior_primo: Primo com maior número de caracteres
    """
    lista_primos_menores: list[primo] = []

    # Monta lista de primos menores
    falta_de_sobreposicao_total = False
    for numero_primo in primos:
        if numero_primo != maior_primo:
            lista_primos_menores.append(numero_primo)
            if not maior_primo.sobrepoe_outro_primo_completamente(numero_primo):
                falta_de_sobreposicao_total = True
                break

    if falta_de_sobreposicao_total:
        return primos

    tamanho_lista_primos = len(lista_primos_menores)

    if tamanho_lista_primos > 9:
        pdb.set_trace()

    assert tamanho_lista_primos <= 9, f"Tamanho da lista de primos era {tamanho_lista_primos}"

    primos_filtrados = filtra_primos_com_sobreposicao_total(
        primos, lista_primos_menores, maior_primo)

    return primos_filtrados


def filtra_primos_com_sobreposicao_total(
        primos: list[primo],
        lista_primos_menores: list[primo],
        maior_primo: primo) -> list[primo]:

    lista_disjunta_encontrada = False
    tamanho_lista_primos = len(lista_primos_menores)
    numero_combinacoes = math.pow(2, tamanho_lista_primos)

    intervalo = int(numero_combinacoes/10)
    contador = 0
    indice_externo = 0

    # Válido apenas para um primo principal
    # TODO: Possível explosão combinatória que precisa ser substituída - Primos disjuntos
    for combinacao in combinacoes_bits(tamanho_lista_primos):
        contador += 1
        indice_externo += 1

        # if contador == intervalo:
        #     print(f"\t\t{indice_externo}/{numero_combinacoes}")
        #     contador = 0

        lista_temporaria: list[primo] = []
        total_caracteres = 0

        for indice, numero_primo in enumerate(lista_primos_menores):
            if combinacao[indice] == 1:
                lista_temporaria.append(numero_primo)
                total_caracteres += numero_primo.numero_caracteres()

        lista_temporaria_e_disjunta = lista_e_disjunta(lista_temporaria)

        if lista_temporaria_e_disjunta and total_caracteres == maior_primo.numero_caracteres():
            lista_disjunta_encontrada = True
            break

    if lista_disjunta_encontrada:
        return lista_temporaria
    else:
        return primos


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
