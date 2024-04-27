""" Classe que implementa funções para processamento de listas de números primos e agrupa várias
informações transitórias mas importantes
"""
from __future__ import annotations
from numeros_primos import primo


class lista_num_primos(object):
    """lista_num_primos(object):
    Lista customizada para facilitar o processamento de listas de números primos
    """

    def __init__(self) -> None:
        self.__lista: list[primo] = []

    def __str__(self) -> str:
        """Representação como string para uso em print statements"""
        resultado = f"len() = {len(self.__lista)} "
        return resultado

    def __repr__(self) -> str:
        return self.__str__()

    def add(self, novo_primo: primo) -> bool:
        if novo_primo not in self.__lista:
            self.__lista.append(novo_primo)
            return True
        else:
            return False

    def remove(self, primo_a_ser_removido: primo):
        if primo_a_ser_removido in self.__lista:
            self.__lista.remove(primo_a_ser_removido)
            return True
        else:
            return False
