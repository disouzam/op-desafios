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

        self.len = len(self.__conteudo)

    def __str__(self) -> str:
        resultado = f"len: {self.len}, Conteúdo: {self.__conteudo}"
        return resultado

    def __repr__(self) -> str:
        return self.__str__()

    def resultado(self):
        return self.__resultado

    def processa_linha(self) -> None:

        saldo_de_parenteses = 0
        posicao_abertura_parenteses = -1
        posicao_inicial_numero = -1
        numero_como_string = None
        for posicao, caractere in enumerate(self.__conteudo):

            if self.expressao_a_esquerda is not None and \
                    self.operador is not None and \
                    self.expressao_a_direita is not None:
                break

            if caractere == "(":
                if saldo_de_parenteses == 0:
                    posicao_abertura_parenteses = posicao

                saldo_de_parenteses += 1

                posicao_fechamento = self.procura_parenteses_de_fechamento(
                    posicao_abertura_parenteses)

                if posicao_fechamento != -1:

                    expressao_dentro_dos_parenteses = self.__conteudo[
                        posicao_abertura_parenteses+1:posicao_fechamento]

                    posicao_proximo_operador = self.procura_operador(
                        posicao_fechamento)

                    expressao_remanescente = self.__conteudo[posicao_fechamento + 1: self.len]

                    if self.expressao_a_esquerda is None:
                        self.expressao_a_esquerda = expressao_numerica(
                            expressao_dentro_dos_parenteses)
                    elif self.expressao_a_direita is None:

                        # Fim da expressão atual
                        if posicao_proximo_operador == -1 and len(expressao_remanescente) == 1:
                            self.expressao_a_direita = expressao_numerica(
                                expressao_dentro_dos_parenteses)
                        else:
                            raise SyntaxErrorException("ERR SYNTAX")
                else:
                    raise SyntaxErrorException("ERR SYNTAX")
                continue

            if caractere == ")":
                saldo_de_parenteses -= 1
                if saldo_de_parenteses < 0:
                    raise SyntaxErrorException("ERR SYNTAX")
                continue

            try:
                if int(caractere) in range(0, 10):
                    if numero_como_string is None:
                        numero_como_string = caractere
                        posicao_inicial_numero = posicao
                    else:
                        numero_como_string += caractere
                    continue
            except ValueError:
                if numero_como_string is not None:
                    if self.expressao_a_esquerda is None:
                        self.expressao_a_esquerda = int(numero_como_string)

                    elif self.expressao_a_direita is None and self.operador is not None:
                        expressao_remanescente = self.__conteudo[posicao_inicial_numero: self.len]
                        self.expressao_a_direita = expressao_numerica(
                            expressao_remanescente)
                    else:
                        raise SyntaxErrorException("ERR SYNTAX")

                # Reseta o valor da variável para monitorar próximo número
                posicao_inicial_numero = -1
                numero_como_string = None

            # Ignora espaços em branco
            if caractere == " ":
                continue

            if caractere in self.__operadores:
                self.operador = self.__operadores[caractere]
        if saldo_de_parenteses != 0:
            raise SyntaxErrorException(
                "Saldo de parênteses diferente de zero...")

        if self.expressao_a_esquerda is not None and isinstance(self.expressao_a_esquerda, expressao_numerica):
            if self.operador is None and self.expressao_a_direita is None:
                return self.expressao_a_esquerda.resultado()
            elif self.operador is None and self.expressao_a_direita is not None:
                raise SyntaxErrorException("ERR SYNTAX")
            elif self.operador is not None and self.expressao_a_direita is None:
                raise SyntaxErrorException("ERR SYNTAX")
            else:
                # Implementar operacoes
                pass

    def procura_parenteses_de_fechamento(self, posicao_abertura_parenteses):
        saldo_de_parenteses = 0
        posicao_fechamento_parenteses = -1

        for posicao in range(posicao_abertura_parenteses, self.len):
            caractere = self.__conteudo[posicao]
            if caractere == "(":
                saldo_de_parenteses += 1
            if caractere == ")":
                saldo_de_parenteses -= 1

            if saldo_de_parenteses == 0:
                return posicao

        if saldo_de_parenteses != 0:
            raise SyntaxErrorException("ERR SYNTAX")

        return posicao_fechamento_parenteses

    def procura_operador(self, posicao_fechamento):
        posicao_operador = -1

        for posicao in range(posicao_fechamento + 1, self.len):
            caractere = self.__conteudo[posicao]
            if caractere in self.__operadores:
                return posicao

        return posicao_operador
