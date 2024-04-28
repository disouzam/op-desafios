""" Classe que implementa funções para processamento de listas de números primos e agrupa várias
informações transitórias mas importantes
"""
from __future__ import annotations
from typing import Generator, cast

from numeros_primos import primo


class lista_num_primos(object):
    """Lista customizada para facilitar o processamento de listas de números primos"""

    def __init__(self) -> None:
        """__init__(self) -> None:
        Construtor
        """
        self.__lista: list[primo] = []
        self.__maior_primo: None | primo = None

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

    def maior_primo(self) -> primo | None:
        """maior_primo(self) -> primo | None:
        Maior número primo presente nessa lista
        """
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
        """append(self, novo_primo: primo) -> bool:
        Insere um novo primo no final da lista
        """
        if novo_primo not in self.__lista:
            self.__lista.append(novo_primo)

            if self.__maior_primo is None or novo_primo.numero_primo > self.__maior_primo.numero_primo:
                self.__maior_primo = novo_primo

            return True
        else:
            return False

    def remove(self, primo_a_ser_removido: primo) -> bool:
        """remove(self, primo_a_ser_removido: primo) -> bool:
        Remove um determinado número primo da lista
        """
        if primo_a_ser_removido in self.__lista:

            if primo_a_ser_removido == self.__maior_primo:
                self.__maior_primo = self.maior_primo()

            self.__lista.remove(primo_a_ser_removido)
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

        maior_comprimento = 0
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

        self.__lista = melhor_combinacao.__lista.copy()
        # print("\nResultado:")
        # self.console_repr()
