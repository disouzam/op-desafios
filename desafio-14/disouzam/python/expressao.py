"""Representa uma expressao numerica recursivamente
"""
from enum import Enum


class Operador(Enum):
    ADICAO = "+"
    SUBTRACAO = "-"
    MULTIPLICACAO = "*"
    DIVISAO = "/"
    POTENCIACAO = "^"


class expressao_numerica(object):

    expressao_a_esquerda = None
    operador = None
    expressao_a_direita = None
    __resultado = None

    __operadores = {member.value: member for member in Operador}

    def __init__(self, linha: str) -> None:
        self.__linha = linha

    def __str__(self) -> str:
        resultado = f"Conteúdo: {self.__linha}"
        return resultado

    def __repr__(self) -> str:
        return self.__str__()

    def resultado(self):
        return self.__resultado

    def processa_linha(self) -> None:
        saldo_de_parenteses = 0
        numero_como_string = None
        for caractere in self.__linha:
            try:
                if int(caractere) in range(0, 10):
                    print("Dígito...")
                    if numero_como_string is None:
                        numero_como_string = caractere
                    else:
                        numero_como_string += caractere
                    continue
            except:
                numero_como_string = None
            if caractere == "(":
                saldo_de_parenteses += 1
                print("Abriu parênteses...")
                continue
            if caractere == ")":
                saldo_de_parenteses -= 1
                if saldo_de_parenteses < 0:
                    raise Exception(
                        "Foram fechados mais parênteses que abertos...")
                print("Fechou parênteses...")
                continue
            if caractere in self.__operadores:
                print("Operador encontrado")
                self.operador = self.__operadores[caractere]
            if caractere == "+":
                print("Sinal de adição...")
                continue
            if caractere == "-":
                print("Sinal de subtração...")
                continue
            if caractere == "*":
                print("Sinal de multiplicação...")
                continue
            if caractere == "/":
                print("Sinal de divisão...")
                continue
            if caractere == "^":
                print("Sinal de potenciação...")
                continue
            if caractere == " ":
                print("Espaço vazio...")
                continue
        if saldo_de_parenteses != 0:
            raise Exception("Saldo de parênteses diferente de zero...")
