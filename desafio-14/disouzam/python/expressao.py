"""Representa uma expressao numerica recursivamente
"""
from enum import Enum


class Operador(Enum):
    ADICAO = "+"
    SUBTRACAO = "-"
    MULTIPLICACAO = "*"
    DIVISAO = "/"
    POTENCIACAO = "^"


class SyntaxErrorException(Exception):
    pass


class expressao_numerica(object):

    expressao_a_esquerda = None
    operador = None
    expressao_a_direita = None
    __resultado = None

    __operadores = {member.value: member for member in Operador}

    def __init__(self, conteudo: str) -> None:
        self.__conteudo = conteudo

        # Adição de espaço em branco ao final do conteúdo para evitar condição de borda ao final
        self.__conteudo += ' '

    def __str__(self) -> str:
        resultado = f"Conteúdo: {self.__conteudo}"
        return resultado

    def __repr__(self) -> str:
        return self.__str__()

    def resultado(self):
        return self.__resultado

    def processa_linha(self) -> None:

        saldo_de_parenteses = 0
        posicao_abertura_parenteses = -1
        posicao_fechamento_parenteses = -1
        numero_como_string = None
        for posicao, caractere in enumerate(self.__conteudo):

            if caractere == "(":
                if saldo_de_parenteses == 0:
                    posicao_abertura_parenteses = posicao
                saldo_de_parenteses += 1
                continue
            if caractere == ")":
                saldo_de_parenteses -= 1
                if saldo_de_parenteses == 0:
                    posicao_fechamento_parenteses = posicao
                if saldo_de_parenteses < 0:
                    raise SyntaxErrorException(
                        "ERR SYNTAX")
                continue

            try:
                if int(caractere) in range(0, 10):
                    if numero_como_string is None:
                        numero_como_string = caractere
                    else:
                        numero_como_string += caractere
                    continue
            except ValueError:
                if numero_como_string is not None:
                    if self.expressao_a_esquerda is None:
                        self.expressao_a_esquerda = int(numero_como_string)
                    elif self.expressao_a_direita is None:
                        self.expressao_a_direita = int(numero_como_string)

                # Reseta o valor da variável para monitorar próximo número
                numero_como_string = None

            # Ignora espaços em branco
            if caractere == " ":
                continue

            if caractere in self.__operadores:
                self.operador = self.__operadores[caractere]
        if saldo_de_parenteses != 0:
            raise SyntaxErrorException(
                "Saldo de parênteses diferente de zero...")
