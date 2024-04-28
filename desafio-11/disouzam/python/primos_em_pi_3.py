"""Terceira implementação dos primos em Pi
"""
from __future__ import annotations
import cProfile
from ctypes import ArgumentError
import os
import sys
from typing import cast


from numeros_primos import primo, e_primo
from manipulacao_de_arquivos import ler_primos_do_arquivo
from lista_numeros_primos import lista_num_primos


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
    lista_primos = lista_num_primos()
    lista_temporaria = lista_num_primos()
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
                    lista_temporaria.filtrar_primos()

                    if lista_primos.size() > 0:
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
        lista_temporaria.filtrar_primos()

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

    if not lista_primos.disjunta():
        raise ArgumentError(f"Lista de primos inválida.")

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
