""" Classe que implementa funções para processamento de listas de números primos e agrupa várias
informações transitórias mas importantes
"""
from __future__ import annotations
import math
from typing import Generator, cast

from numeros_primos import primo
from geracao_lista_bits import combinacoes_bits


class lista_num_primos(object):
    """Lista customizada para facilitar o processamento de listas de números primos"""

    def __init__(self) -> None:
        """__init__(self) -> None:
        Construtor
        """
        self.__lista: list[primo] = []
        self.menor_posicao = -1
        self.maior_posicao = -1

    def __str__(self) -> str:
        """__str__(self) -> str:
        Representação como string para uso em print statements
        """
        resultado = f"len() = {len(self.__lista)} "
        return resultado

    def __repr__(self) -> str:
        """__repr__(self) -> str:
        Representação como string para uso na visualização durante debug, por exemplo
        """
        return self.__str__()

    def __iter__(self) -> Generator[primo, None, None]:
        """__iter__(self) -> Generator[primo, None, None]:
        Iterador para uso em situações de enumeração da lista
        """
        return (item for item in self.__lista)

    def console_repr(self) -> None:
        print("\n\n")
        for item in self.__lista:
            print(item)

    def size(self) -> int:
        """size(self) -> int:
        Tamanho da lista de primos
        """
        return len(self.__lista)

    def append(self, novo_primo: primo) -> bool:
        """append(self, novo_primo: primo) -> bool:
        Insere um novo primo no final da lista
        """
        if novo_primo not in self.__lista:
            if self.size() == 0:
                self.menor_posicao = novo_primo.inicio
                self.maior_posicao = novo_primo.fim
            else:
                if novo_primo.inicio < self.menor_posicao:
                    self.menor_posicao = novo_primo.inicio

                if novo_primo.fim > self.maior_posicao:
                    self.maior_posicao = novo_primo.fim

            self.__lista.append(novo_primo)

            return True
        else:
            return False

    def __recalcular_posicoes(self):

        self.menor_posicao = -1
        self.maior_posicao = -1

        if self.size() > 0:
            self.menor_posicao = self[0].inicio
            self.maior_posicao = self[0].fim

        for numero_primo in self.__lista:
            if numero_primo.inicio < self.menor_posicao:
                self.menor_posicao = numero_primo.inicio

            if numero_primo.fim < self.maior_posicao:
                self.maior_posicao = numero_primo.fim

    def checar_se_combinacao_seria_contigua(self, outra_lista: lista_num_primos):
        if self.maior_posicao + 1 == outra_lista.menor_posicao:
            # Outra lista começa depois da lista atual
            return True
        elif outra_lista.maior_posicao + 1 == self.menor_posicao:
            # Outra lista começa antes da lista atual
            return True
        else:
            return False

    def maior_comprimento_possivel(self):

        if self.size() == 0:
            return 0

        if self.menor_posicao == -1 or self.maior_posicao == -1:
            self.__recalcular_posicoes()

        resultado = self.maior_posicao - self.menor_posicao + 1
        return resultado

    def remove(self, primo_a_ser_removido: primo) -> bool:
        """remove(self, primo_a_ser_removido: primo) -> bool:
        Remove um determinado número primo da lista
        """
        if primo_a_ser_removido in self.__lista:
            self.__lista.remove(primo_a_ser_removido)
            self.menor_posicao = -1
            self.maior_posicao = -1

            return True
        else:
            return False

    def extend(self, outra_lista: lista_num_primos) -> None:
        """extend(self, outra_lista: lista_num_primos) -> None:
        Concatena os itens da outra lista na lista atual
        """
        for item in outra_lista:
            if isinstance(item, primo):
                self.append(item)

    def clear(self) -> None:
        """clear(self) -> None:
        Limpa a lista
        """
        self.__lista.clear()

    def __getitem__(self, index) -> primo:
        """__getitem__(self, index) -> primo:
        Função especial para permitir acesso indexado
        """
        try:
            resultado = self.__lista[index]
        except Exception as ex:
            raise IndexError("list index out of range") from ex

        return cast(primo, resultado)

    def __setitem__(self, index, novo_valor) -> None:
        """__setitem__(self, index, novo_valor) -> None:
        Função especial para permitir atribuição indexada
        """
        self.__lista[index] = novo_valor

    def copy(self) -> lista_num_primos:
        """copy(self) -> lista_num_primos:
        Executa uma cópia de todos os itens na lista atual e retona uma nova referência
        """
        copia = lista_num_primos()

        for item in self.__lista:
            copia.append(item)

        return copia

    def lista_de_primos_como_string(self) -> list[str]:
        """lista_de_primos_como_string(self) -> list[str]:
        Retorna uma lista de strings para posterior processamento pelos clientes dessa classe
        """
        resultado: list[str] = []
        for item in self.__lista:
            resultado.append(f"{item.numero_primo}")
        return resultado

    def lista_de_primos_concatenada(self) -> str:
        lista_de_strings = self.lista_de_primos_como_string()
        resultado = ''.join(lista_de_strings)
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

    def contigua(self) -> bool:
        """contigua(self)-> bool:
        Checa se a lista é feita de primos contíguos (sem espaço entre eles)
        """
        for indice in range(0, len(self.__lista) - 1):
            primo_atual = self.__lista[indice]
            primo_seguinte = self.__lista[indice + 1]

            if primo_atual.fim + 1 != primo_seguinte.inicio:
                return False

        return True

    def comprimento(self) -> int:
        """comprimento(self) -> int:
        Retorna o comprimento de listas disjuntas de números primos (em Pi)
        """
        if not self.disjunta():
            return int(0)
        else:
            resultado = 0
            for item in self.__lista:
                resultado += item.numero_caracteres()
            return resultado

    def filtrar_primos(self) -> None:
        """filtrar_primos(self)
        Processa uma lista temporaria de primos com sobreposicao e mantem os primos disjuntos
        quando existir ou devolve a lista original
        """
        # Razões para não seguir com o processamento
        if self.size() == 0:
            return

        self.exclui_sobreposicao_total()

        maior_comprimento = 0
        maior_comprimento_possivel = self.maior_comprimento_possivel()
        melhor_combinacao = self.copy()

        for indice_externo, primo_atual in enumerate(self):
            lista_temporaria = lista_num_primos()
            sub_lista = lista_num_primos()

            lista_temporaria.append(primo_atual)

            for indice_interno in range(indice_externo + 1, self.size()):
                primo_interno = self[indice_interno]

                if not primo_atual.sobrepoe_outro_primo_parcialmente(primo_interno):
                    sub_lista.append(primo_interno)

            sub_lista.filtrar_primos()
            lista_temporaria.extend(sub_lista)

            if lista_temporaria.comprimento() > maior_comprimento:
                melhor_combinacao = lista_temporaria.copy()
                maior_comprimento = melhor_combinacao.comprimento()
                # print("\nMelhor combinação: ")
                # melhor_combinacao.console_repr()

            if maior_comprimento == maior_comprimento_possivel:
                break

        self.__lista = melhor_combinacao.__lista.copy()
        # print("\nResultado:")
        # self.console_repr()

    def exclui_sobreposicao_total(self) -> None:
        sub_listas: list[lista_num_primos] = []
        maiores_primos: list[lista_num_primos] = []

        primos_temporarios = self.copy()

        indice_sublistas = 0
        while primos_temporarios.size() > 0:
            primo_candidato = primos_temporarios[0]
            primos_temporarios.remove(primo_candidato)

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
        while indice_sublistas < numero_sublistas:
            del lista_temporaria
            lista_temporaria = sub_listas[indice_sublistas].copy()

            lista_temporaria.filtra_primos_disjuntos_de_lista_com_sobreposicao_total(
                maiores_primos[indice_sublistas][0])

            sub_listas[indice_sublistas] = lista_temporaria
            indice_sublistas += 1

        # Mesclar as sublistas
        lista_temporaria = lista_num_primos()
        numero_sublistas = len(sub_listas)
        indice_sublistas = 0
        while indice_sublistas < numero_sublistas:
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

        self.__lista = lista_temporaria.__lista.copy()

    def filtra_primos_disjuntos_de_lista_com_sobreposicao_total(self, maior_primo: primo) -> None:
        """filtra_primos_disjuntos_de_lista_com_sobreposicao_total(primos: list[primo], maior_primo: primo) -> list[primo]:
        Filtra uma lista de primos com sobreposicao total e devolve uma
        lista de itens disjuntos, se existir

        Parâmetros:
        primos: Lista de números primos
        maior_primo: Primo com maior número de caracteres
        """
        lista_primos_menores = lista_num_primos()

        # Monta lista de primos menores
        falta_de_sobreposicao_total = False
        for numero_primo in self:
            if numero_primo != maior_primo:
                lista_primos_menores.append(numero_primo)
                if not maior_primo.sobrepoe_outro_primo_completamente(numero_primo):
                    falta_de_sobreposicao_total = True
                    break

        if falta_de_sobreposicao_total:
            return

        tamanho_lista_primos = lista_primos_menores.size()
        lista_disjunta_encontrada = False

        numero_combinacoes = math.pow(2, tamanho_lista_primos)

        intervalo = int(numero_combinacoes/10)
        contador = 0
        indice_externo = 0

        # Válido apenas para um primo principal
        for combinacao in combinacoes_bits(tamanho_lista_primos):
            contador += 1
            indice_externo += 1

            # if contador == intervalo:
            #     print(f"\t\t{indice_externo}/{numero_combinacoes}")
            #     contador = 0

            lista_temporaria = lista_num_primos()
            total_caracteres = 0

            for indice, numero_primo in enumerate(lista_primos_menores):
                if combinacao[indice] == 1:
                    lista_temporaria.append(numero_primo)
                    total_caracteres += numero_primo.numero_caracteres()

            lista_temporaria_e_disjunta = lista_temporaria.disjunta()

            if lista_temporaria_e_disjunta and total_caracteres == maior_primo.numero_caracteres():
                lista_disjunta_encontrada = True
                break

        if lista_disjunta_encontrada:
            self.__lista = lista_temporaria.__lista.copy()
