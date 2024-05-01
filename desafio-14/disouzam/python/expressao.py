"""Representa uma expressao numerica recursivamente
"""
from enum import Enum
from types import FrameType
from typing import cast
from inspect import FrameInfo, currentframe, getframeinfo


class Operador(Enum):
    ADICAO = "+"
    SUBTRACAO = "-"
    MULTIPLICACAO = "*"
    DIVISAO = "/"
    POTENCIACAO = "^"


class SyntaxErrorException(Exception):

    def __init__(self, *args: object, frametype: FrameType | None = None) -> None:
        if frametype is not None:
            frameinfo = getframeinfo(frametype)
            mensagem = f"{frameinfo.filename} - {frameinfo.lineno}"
            unpacked_args = [*args]

            unpacked_args.append(mensagem)
        super().__init__(unpacked_args)


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

        try:
            valor_convertido = float(self.__conteudo)
            self.__resultado = valor_convertido
        except ValueError:
            self.__processa_conteudo()

    def __str__(self) -> str:
        representacao_como_string = f"len: {self.len}, Conteúdo: {self.__conteudo}"
        return representacao_como_string

    def __repr__(self) -> str:
        return self.__str__()

    def resultado(self):

        # Expressão numérica base, sem sub-expressões numéricas à esquerda e à direita
        if self.__resultado is not None:
            return self.__resultado

        if self.expressao_a_direita is None and self.operador is None:
            if isinstance(self.expressao_a_esquerda, expressao_numerica):
                return self.expressao_a_esquerda.resultado()

        if self.expressao_a_direita is not None and self.operador is None:
            frameinfo = cast(FrameType, currentframe())
            raise SyntaxErrorException(frametype=frameinfo)

    def __processa_conteudo(self) -> None:

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
                            frameinfo = cast(FrameType, currentframe())
                            raise SyntaxErrorException(frametype=frameinfo)
                else:
                    frameinfo = cast(FrameType, currentframe())
                    raise SyntaxErrorException(frametype=frameinfo)
                continue

            if caractere == ")":
                saldo_de_parenteses -= 1
                if saldo_de_parenteses < 0:
                    frameinfo = cast(FrameType, currentframe())
                    raise SyntaxErrorException(frametype=frameinfo)
                continue

            try:
                if caractere == "." or int(caractere) in range(0, 10):
                    if numero_como_string is None:
                        numero_como_string = caractere
                        posicao_inicial_numero = posicao
                    else:
                        numero_como_string += caractere
                    continue
            except ValueError:
                if numero_como_string is not None:
                    if self.expressao_a_esquerda is None:
                        self.expressao_a_esquerda = expressao_numerica(
                            numero_como_string)

                    elif self.expressao_a_direita is None and self.operador is not None:
                        expressao_remanescente = self.__conteudo[posicao_inicial_numero: self.len]
                        self.expressao_a_direita = expressao_numerica(
                            expressao_remanescente)
                    else:
                        frameinfo = cast(FrameType, currentframe())
                        raise SyntaxErrorException(frametype=frameinfo)

                # Reseta o valor da variável para monitorar próximo número
                posicao_inicial_numero = -1
                numero_como_string = None

            # Ignora espaços em branco
            if caractere == " ":
                continue

            if caractere in self.__operadores:
                self.operador = self.__operadores[caractere]
        if saldo_de_parenteses != 0:
            frameinfo = cast(FrameType, currentframe())
            raise SyntaxErrorException(
                f"Saldo de parênteses diferente de zero...", frametype=frameinfo)

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
            frameinfo = cast(FrameType, currentframe())
            raise SyntaxErrorException(frametype=frameinfo)

        return posicao_fechamento_parenteses

    def procura_operador(self, posicao_fechamento):
        posicao_operador = -1

        for posicao in range(posicao_fechamento + 1, self.len):
            caractere = self.__conteudo[posicao]
            if caractere in self.__operadores:
                return posicao

        return posicao_operador
