"""Representa uma expressao numerica recursivamente
"""
from __future__ import annotations
from enum import Enum
import math
import sys
from types import FrameType
from typing import Any, Literal, cast
from inspect import currentframe, getframeinfo
from unittest import result


class Operador(Enum):
    NONE = "None"
    ADICAO = "+"
    SUBTRACAO = "-"
    MULTIPLICACAO = "*"
    DIVISAO = "/"
    POTENCIACAO = "^"


def precedencia_operadores(primeiroOperador: Operador, segundoOperador: Operador) -> int:
    valores = {member: -1 for member in Operador}

    valores[Operador.ADICAO] = 0
    valores[Operador.SUBTRACAO] = 0

    valores[Operador.DIVISAO] = 1
    valores[Operador.MULTIPLICACAO] = 1

    valores[Operador.POTENCIACAO] = 2

    primeiro = valores[primeiroOperador]
    segundo = valores[segundoOperador]

    resultado = primeiro - segundo

    return resultado


class SyntaxErrorException(Exception):

    def __init__(self, *args: object, frametype: FrameType | None = None) -> None:
        if frametype is not None:
            frameinfo = getframeinfo(frametype)
            mensagem = f"{frameinfo.filename} - {frameinfo.lineno}"
            unpacked_args = [*args]

            unpacked_args.append(mensagem)

        # TODO: Remover antes da submissão do PR
        if debugger_is_active():
            super().__init__(unpacked_args)
        else:
            super().__init__()


class DivByZeroErrorException(Exception):

    def __init__(self, *args: object, frametype: FrameType | None = None) -> None:
        if frametype is not None:
            frameinfo = getframeinfo(frametype)
            mensagem = f"{frameinfo.filename} - {frameinfo.lineno}"
            unpacked_args = [*args]

            unpacked_args.append(mensagem)

        # TODO: Remover antes da submissão do PR
        if debugger_is_active():
            super().__init__(unpacked_args)
        else:
            super().__init__()


class expressao_numerica(object):

    expressao_a_esquerda = None
    operador = Operador.NONE
    expressao_a_direita = None
    __resultado = None
    continha_parenteses = False

    __operadores = {member.value: member for member in Operador}

    def __init__(self, conteudo: str, pai: expressao_numerica = None) -> None:
        self.__pai = pai
        conteudo = conteudo.strip()
        if conteudo[0] == "(" and conteudo[-1] == ")":
            self.continha_parenteses = True
            self.__conteudo = conteudo[1:len(conteudo) - 1]
        else:
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

        if self.expressao_a_esquerda is None and self.expressao_a_direita is None:
            representacao_como_string += ", Tipo: Primitiva"
        return representacao_como_string

    def __repr__(self) -> str:
        return self.__str__()

    def primitiva(self):
        expressao_e_primitiva = self.__resultado is not None
        return expressao_e_primitiva

    def resultado(self):

        # Expressão numérica base, sem sub-expressões numéricas à esquerda e à direita
        if self.__resultado is not None:
            return self.__resultado

        # Se não existe a expressão à esquerda, lança um erro de sintaxe
        if self.expressao_a_esquerda is None:
            frameinfo = cast(FrameType, currentframe())
            raise SyntaxErrorException(frametype=frameinfo)

        # Se existe só a expressão à esquerda, o resultado é somente dela
        if self.expressao_a_direita is None and self.operador == Operador.NONE:
            if isinstance(self.expressao_a_esquerda, expressao_numerica):
                self.__resultado = self.expressao_a_esquerda.resultado()
                return self.__resultado

        # Ter uma expressão à direta e não ter operador, lança um erro de sintaxe
        if self.expressao_a_direita is not None and self.operador == Operador.NONE:
            frameinfo = cast(FrameType, currentframe())
            raise SyntaxErrorException(frametype=frameinfo)

        # Ter um operador mas não ter uma expressão à direita, lança um erro de sintaxe
        if self.expressao_a_direita is None and self.operador != Operador.NONE:
            frameinfo = cast(FrameType, currentframe())
            raise SyntaxErrorException(frametype=frameinfo)

        # Recursão
        if self.expressao_a_esquerda is not None and self.expressao_a_direita is not None:
            resultado_a_esquerda = None
            resultado_a_direita = None

            precedencia_esquerda_sobre_atual = precedencia_operadores(
                self.expressao_a_esquerda.operador, self.operador)

            precedencia_esquerda_sobre_direita = precedencia_operadores(
                self.expressao_a_esquerda.operador, self.expressao_a_direita.operador)

            precedencia_atual_sobre_direita = precedencia_operadores(
                self.operador, self.expressao_a_direita.operador)

            if precedencia_esquerda_sobre_atual > 0 and precedencia_esquerda_sobre_direita > 0:
                if self.expressao_a_direita.continha_parenteses:
                    self.processa_primeiro_a_direita()
                else:
                    self.processa_primeiro_a_esquerda()

            elif precedencia_esquerda_sobre_atual < 0 and \
                    precedencia_atual_sobre_direita >= 0:
                if self.expressao_a_esquerda.continha_parenteses:
                    self.processa_primeiro_a_esquerda()
                elif self.expressao_a_direita.continha_parenteses:
                    self.processa_primeiro_a_direita()
                else:
                    self.processa_primeiro_a_atual()

            elif precedencia_esquerda_sobre_atual < 0 and precedencia_atual_sobre_direita < 0:
                if self.expressao_a_esquerda.continha_parenteses:
                    self.processa_primeiro_a_esquerda()
                else:
                    self.processa_primeiro_a_direita()

            if self.__pai is not None:
                return

            # Realiza mais um passe de avaliação de resultados se tiver na raiz
            if self.__pai is None:
                resultado = self.resultado()

            self.__resultado = float(resultado)
            return self.__resultado

    def processa_primeiro_a_atual(self):
        expressao_a_esquerda = cast(
            expressao_numerica, self.expressao_a_esquerda)

        expressao_a_direita = cast(
            expressao_numerica, self.expressao_a_direita)

        expressao_a_esquerda_da_direita = cast(
            expressao_numerica, expressao_a_direita.expressao_a_esquerda)

        if not expressao_a_esquerda.primitiva():
            expressao_a_esquerda.resultado()

        if not expressao_a_direita.primitiva():
            expressao_a_direita.resultado()

        if expressao_a_esquerda.primitiva() and \
                expressao_a_esquerda_da_direita is not None and \
                expressao_a_esquerda_da_direita.primitiva():
            resultado_intermediario = self.executar_operacoes_matematicas(
                expressao_a_esquerda, expressao_a_esquerda_da_direita, self.operador)
            self.expressao_a_direita = expressao_a_direita.expressao_a_direita
            self.operador = expressao_a_direita.operador

        elif expressao_a_esquerda.primitiva() and \
                expressao_a_direita.primitiva():
            resultado_intermediario = self.executar_operacoes_matematicas(
                expressao_a_esquerda, expressao_a_direita, self.operador)
            self.expressao_a_direita = None
            self.operador = Operador.NONE

        self.expressao_a_esquerda = expressao_numerica(
            str(resultado_intermediario), self)

        # Reseta a expressão atual pois já foi manipulada
        self.__conteudo = str('')
        self.continha_parenteses = False

    def processa_primeiro_a_esquerda(self):
        return self.expressao_a_esquerda.resultado()

    def processa_primeiro_a_direita(self):
        return self.expressao_a_direita.resultado()

    def executar_operacoes_matematicas(self, esquerda, direita, operador):
        resultado_esquerda = esquerda.resultado()
        resultado_direita = direita.resultado()

        if operador == Operador.POTENCIACAO:
            resultado = math.pow(resultado_esquerda, resultado_direita)

        if operador == Operador.MULTIPLICACAO:
            resultado = resultado_esquerda * resultado_direita

        if operador == Operador.DIVISAO:
            if resultado_direita == 0:
                frameinfo = cast(FrameType, currentframe())
                raise DivByZeroErrorException(frametype=frameinfo)
            resultado = resultado_esquerda / resultado_direita

        if operador == Operador.ADICAO:
            resultado = resultado_esquerda + resultado_direita

        if operador == Operador.SUBTRACAO:
            resultado = resultado_esquerda - resultado_direita

        resultado = float(resultado)
        return resultado

    def __processa_conteudo(self) -> None:

        saldo_de_parenteses = 0
        posicao_abertura_parenteses = -1
        posicao_inicial_numero = -1
        numero_como_string = None
        posicao = -1

        # pylint: disable=consider-using-enumerate
        while posicao < len(self.__conteudo):
            posicao += 1
            caractere = self.__conteudo[posicao]

            if self.expressao_a_direita is not None and \
                self.operador != Operador.NONE and \
                    self.expressao_a_esquerda is not None:
                break

            if caractere == "(":
                if saldo_de_parenteses == 0:
                    posicao_abertura_parenteses = posicao

                saldo_de_parenteses += 1

                posicao_fechamento = self.procura_parenteses_de_fechamento(
                    posicao_abertura_parenteses)

                if posicao_fechamento != -1:

                    posicao = posicao_fechamento - 1

                    expressao_dentro_dos_parenteses = self.__conteudo[
                        posicao_abertura_parenteses:posicao_fechamento + 1]

                    posicao_proximo_operador = self.procura_operador(
                        posicao_fechamento)

                    expressao_remanescente = self.__conteudo[posicao_fechamento + 2: self.len]

                    if self.expressao_a_esquerda is None:
                        self.expressao_a_esquerda = expressao_numerica(
                            expressao_dentro_dos_parenteses, self)
                    elif self.expressao_a_direita is None:

                        # Fim da expressão atual
                        if posicao_proximo_operador == -1 and len(expressao_remanescente) == 1:
                            self.expressao_a_direita = expressao_numerica(
                                expressao_dentro_dos_parenteses, self)
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
                            numero_como_string, self)

                    elif self.expressao_a_direita is None and self.operador is not None:
                        expressao_remanescente = self.__conteudo[posicao_inicial_numero: self.len]
                        self.expressao_a_direita = expressao_numerica(
                            expressao_remanescente, self)
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

                posicao_proximo_operador = self.procura_operador(
                    posicao)

                if posicao_proximo_operador != -1:
                    encontrou_digito_valido = False
                    for indice in range(posicao + 1, posicao_proximo_operador):
                        if self.__conteudo[indice] != " " and self.__conteudo not in self.__operadores:
                            encontrou_digito_valido = True
                            break

                    if not encontrou_digito_valido:
                        frameinfo = cast(FrameType, currentframe())
                        raise SyntaxErrorException(frametype=frameinfo)

                expressao_remanescente = self.__conteudo[posicao + 1: self.len]
                self.expressao_a_direita = expressao_numerica(
                    expressao_remanescente, self)

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


def debugger_is_active() -> bool:
    # TODO: Remover antes da submissão do PR
    """Return if the debugger is currently active

    # pylint: disable=line-too-long
    Source: https://stackoverflow.com/questions/38634988/check-if-program-runs-in-debug-mode/67065084
    """
    return hasattr(sys, 'gettrace') and sys.gettrace() is not None
