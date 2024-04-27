""" Classe que implementa funções para processamento de listas de números primos e agrupa várias
informações transitórias mas importantes
"""
from __future__ import annotations
import math
from typing import Generator, cast
import pdb

from numeros_primos import primo
from geracao_lista_bits import combinacoes_bits


class lista_num_primos(object):
    """lista_num_primos(object):
    Lista customizada para facilitar o processamento de listas de números primos
    """

    def __init__(self) -> None:
        self.__lista: list[primo] = []
        self.__maior_primo: None | primo = None

    def __str__(self) -> str:
        """Representação como string para uso em print statements"""
        resultado = f"len() = {len(self.__lista)} "
        return resultado

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self) -> Generator[primo, None, None]:
        return (item for item in self.__lista)

    def size(self) -> int:
        return len(self.__lista)

    def maior_primo(self) -> primo | None:
        if self.__maior_primo is not None:
            return self.__maior_primo
        elif self.size() > 0:
            self.__maior_primo = self.__lista[0]
            for indice in range(1, self.size()):
                primo_anterior = self.__lista[indice - 1]
                primo_atual = self.__lista[indice]
                if primo_atual.numero_primo > primo_anterior.numero_primo:
                    self.__maior_primo = primo_atual
            return self.__maior_primo
        else:
            return None

    def append(self, novo_primo: primo) -> bool:
        if novo_primo not in self.__lista:
            self.__lista.append(novo_primo)

            if self.__maior_primo is None or novo_primo.numero_primo > self.__maior_primo.numero_primo:
                self.__maior_primo = novo_primo

            return True
        else:
            return False

    def remove(self, primo_a_ser_removido: primo) -> bool:
        if primo_a_ser_removido in self.__lista:

            if primo_a_ser_removido == self.__maior_primo:
                self.__maior_primo = self.maior_primo()

            self.__lista.remove(primo_a_ser_removido)
            return True
        else:
            return False

    def extend(self, outra_lista: lista_num_primos) -> None:
        for item in outra_lista:
            if isinstance(item, primo):
                self.append(item)

    def clear(self) -> None:
        self.__lista.clear()

    def __getitem__(self, index):
        try:
            resultado = self.__lista[index]
        except Exception as ex:
            raise IndexError("list index out of range") from ex

        return cast(primo, resultado)

    def __setitem__(self, index, novo_valor) -> None:
        self.__lista[index] = novo_valor

    def copy(self) -> lista_num_primos:
        copia = lista_num_primos()

        for item in self.__lista:
            copia.append(item)

        return copia

    def lista_de_primos_como_string(self) -> list[str]:
        resultado: list[str] = []
        for item in self.__lista:
            resultado.append(f"{item.numero_primo}")
        return resultado

    def disjunta(self) -> bool:
        """lista_e_disjunta(self) -> bool:
        Checa se uma lista é disjunta ou não
        """
        for indice in range(0, len(self.__lista) - 1):
            primo_atual = self.__lista[indice]
            primo_seguinte = self.__lista[indice + 1]

            if primo_atual.sobrepoe_outro_primo_parcialmente(primo_seguinte):
                return False

        return True

    def filtrar_primos_disjuntos(self) -> None:
        """filtrar_primos_disjuntos()
        Processa uma lista temporaria de primos com sobreposicao e mantem os primos disjuntos
        quando existir ou devolve a lista original
        """
        # Razões para não seguir com o processamento
        if self.size() == 0:
            return

        sub_listas: list[lista_num_primos] = []
        maiores_primos: list[lista_num_primos] = []

        # Inicia a formação das sublistas
        primos_temporarios = self.copy()

        indice_sublistas = 0
        while primos_temporarios.size() > 0:
            primo_candidato = primos_temporarios[0]
            primos_temporarios.remove(primo_candidato)

            if indice_sublistas > 0:
                sub_listas.append(lista_num_primos())
                maiores_primos.append(lista_num_primos())

            sub_listas[indice_sublistas].append(primo_candidato)
            maiores_primos[indice_sublistas].append(primo_candidato)
            maior_primo_atual = primo_candidato

            indice_interno = 0
            while indice_interno < primos_temporarios.size():
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
        lista_temporaria = lista_num_primos()
        while self.size() > 0 and indice_sublistas < numero_sublistas:
            del lista_temporaria
            lista_temporaria = sub_listas[indice_sublistas].copy()

            lista_temporaria.__filtra_primos_disjuntos_de_lista_com_sobreposicao_total()

            sub_listas[indice_sublistas] = lista_temporaria
            indice_sublistas += 1

        # Mesclar as sublistas
        lista_temporaria = lista_num_primos()
        numero_sublistas = len(sub_listas)
        indice_sublistas = 0
        while len(self.__lista) > 0 and indice_sublistas < numero_sublistas:
            lista_temporaria.extend(sub_listas[indice_sublistas])
            indice_sublistas += 1

        # Ordenar as sublistas
        quantidade_primos = lista_temporaria.size()
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

        return

    def __filtra_primos_disjuntos_de_lista_com_sobreposicao_total(self) -> None:
        """filtra_primos_disjuntos_de_lista_com_sobreposicao_total() -> list[primo]:
        Filtra uma lista de primos com sobreposicao total e devolve uma
        lista de itens disjuntos, se existir

        Parâmetros:
        primos: Lista de números primos
        maior_primo: Primo com maior número de caracteres
        """
        lista_primos_menores: list[primo] = []

        # Monta lista de primos menores
        falta_de_sobreposicao_total = False
        for numero_primo in self.__lista:
            if numero_primo != self.__maior_primo and isinstance(self.__maior_primo, primo):
                lista_primos_menores.append(numero_primo)
                if not self.__maior_primo.sobrepoe_outro_primo_completamente(numero_primo):
                    falta_de_sobreposicao_total = True
                    break

        if falta_de_sobreposicao_total:
            return

        tamanho_lista_primos = len(lista_primos_menores)

        if tamanho_lista_primos > 9:
            pdb.set_trace()

        assert tamanho_lista_primos <= 9, f"Tamanho da lista de primos era {tamanho_lista_primos}"

        primos_filtrados = filtra_primos_com_sobreposicao_total(
            primos, lista_primos_menores, maior_primo)

        self.__lista = primos_filtrados

    def __filtra_primos_sobrepostos(self):
        """filtra_primos_sobrepostos(primos: list[primo]) -> list[primo]:
        Usando permutação, obtém a maior lista possível sem sobreposicao
        """
        tamanho_lista_primos = self.size()

        # TODO: Remover antes da submissão do PR
        # print("Início do cálculo de combinacoes")
        if tamanho_lista_primos == 0:
            return

        # TODO: Remover antes da submissão do PR
        # print("Fim do cálculo de combinacoes")

        maior_comprimento_obtido = 0
        melhor_combinacao = lista_num_primos()
        lista_disjunta_encontrada = False
        lista_temporaria = lista_num_primos()

        primeira_posicao = self[0].inicio
        ultima_posicao = self[0].fim

        for numero_primo in self:
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
            if contador == intervalo:
                print(f"\t\t{indice_externo}/{numero_combinacoes}")
                contador = 0

            del lista_temporaria
            lista_temporaria = lista_num_primos()
            total_caracteres = 0

            primo_anterior: None | primo = None
            sobreposicao_encontrada = False

            for indice, numero_primo in enumerate(self.__lista):
                if combinacao[indice] == 1:
                    if lista_temporaria.size() >= 1:
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

            lista_temporaria_e_disjunta = lista_temporaria.disjunta()

            if lista_temporaria_e_disjunta and total_caracteres > maior_comprimento_obtido:
                lista_disjunta_encontrada = True
                melhor_combinacao = lista_temporaria.copy()
                maior_comprimento_obtido = total_caracteres

                if maior_comprimento_obtido == maior_comprimento_possivel:
                    # print(
                    #     f"Terminou após {100 *round(indice_externo/numero_combinacoes,2)}% completados...")
                    break

        if lista_disjunta_encontrada:
            self = melhor_combinacao.copy()
