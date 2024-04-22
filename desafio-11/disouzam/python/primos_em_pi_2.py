"""Segunda implementação dos primos em Pi
"""
from __future__ import annotations
import cProfile
from ctypes import ArgumentError
import os
import sys
from typing import cast
from numeros_primos import primo


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

    arquivo_de_resultado = "resultado.txt"
    if not os.path.isfile(arquivo_de_resultado):
        os.remove(arquivo_de_resultado)

    with open(arquivo_de_resultado, "w", encoding='utf-8') as arquivo:
        arquivo.write(caracteres_concatenados)

    print("Primos obtidos com sucesso!")


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

    # Levanta todos os primos existentes, não checando sobreposição
    for posicao_caractere_atual in range(0, len(digitos)):
        for comprimento in range(1, 5):
            inicio = posicao_caractere_atual
            fim = posicao_caractere_atual + comprimento - 1
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
                    for numero_primo in lista_temporaria:
                        lista_primos.append(numero_primo)
                    lista_temporaria: list[primo] = []
                    lista_temporaria.append(primo_atual)
                    maximo_indice_final = primo_atual.fim
                else:
                    lista_temporaria.append(primo_atual)

                print(primo_atual)

    if posicao_caractere_atual == len(digitos) - 1:
        lista_temporaria = filtrar_primos_disjuntos(
            lista_temporaria)
        for numero_primo in lista_temporaria:
            lista_primos.append(numero_primo)

    del lista_temporaria, candidato, comprimento, inicio, fim, posicao_caractere_atual
    del primo_anterior, primo_atual, sobreposicao_entre_vizinhos, numero_primo

    lista_primos_como_string: list[str] = []
    for primo_atual in lista_primos:
        lista_primos_como_string.append(f"{primo_atual.numero_primo}")
    return lista_primos_como_string


def filtrar_primos_disjuntos(primos: list[primo]) -> list[primo]:
    """filtrar_primos_disjuntos(lista_temporaria)
    Processa uma lista temporaria de primos com sobreposicao e mantem os primos disjuntos
    quando existir ou devolve a lista original
    """
    # Razões para não seguir com o processamento
    if len(primos) == 0:
        return primos

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
    while len(primos) > 0 and indice_sublistas < numero_sublistas:
        lista_temporaria = sub_listas[indice_sublistas].copy()
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

    lista_temporaria = filtra_primos_sobrepostos(lista_temporaria)

    return lista_temporaria


def filtra_primos_sobrepostos(primos: list[primo]) -> list[primo]:
    """filtra_primos_sobrepostos(primos: list[primo]) -> list[primo]:
    Usando permutação, obtém a maior lista possível sem sobreposicao
    """
    lista_bits = combinacoes_bits(len(primos))
    maior_comprimento_obtido = 0
    melhor_combinacao: list[primo] = []
    lista_disjunta_encontrada = False

    for combinacao in lista_bits:
        lista_temporaria: list[primo] = []
        total_caracteres = 0

        for indice, numero_primo in enumerate(primos):
            if combinacao[indice] == 1:
                lista_temporaria.append(numero_primo)
                total_caracteres += numero_primo.numero_caracteres()

        lista_temporaria_e_disjunta = lista_e_disjunta(lista_temporaria)

        if lista_temporaria_e_disjunta and total_caracteres > maior_comprimento_obtido:
            lista_disjunta_encontrada = True
            melhor_combinacao = lista_temporaria.copy()
            maior_comprimento_obtido = total_caracteres

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

    lista_bits = combinacoes_bits(len(lista_primos_menores))
    lista_disjunta_encontrada = False

    # Válido apenas para um primo principal
    for combinacao in lista_bits:
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


def combinacoes_bits(tamanho) -> list[list[int]]:
    """combinacoes_bits(tamanho)
    Gera lista de combinações de bits para avaliar a superposição entre primos

    Parâmetro:
    tamanho: Número de bits para gerar a combinação
    """
    lista_combinacoes = []

    if tamanho == 0:
        return lista_combinacoes

    if tamanho == 1:
        lista: list[int] = []
        lista.append(0)
        lista_combinacoes.append(lista)

        lista: list[int] = []
        lista.append(1)
        lista_combinacoes.append(lista)
        return lista_combinacoes

    sub_combinacoes: list[list[int]] = combinacoes_bits(tamanho - 1)

    for sub_combinacao in sub_combinacoes:
        lista: list[int] = []
        lista.append(0)
        lista.extend(sub_combinacao)
        lista_combinacoes.append(lista)

        lista: list[int] = []
        lista.append(1)
        lista.extend(sub_combinacao)
        lista_combinacoes.append(lista)

    return lista_combinacoes


def e_primo(numero) -> bool:
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
