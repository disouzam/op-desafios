"""Representa uma expressao numerica recursivamente
"""


class expressao_numerica(object):

    def __init__(self, linha: str) -> None:
        self.__linha = linha

    def __str__(self) -> str:
        resultado = f"Conteúdo: {self.__linha}"
        return resultado

    def __repr__(self) -> str:
        return self.__str__()

    def processa_linha(self) -> None:
        saldo_de_parenteses = 0
        for caractere in self.__linha:
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
            try:
                if int(caractere) in range(0, 10):
                    print("Dígito...")
                    continue
            except:
                print("Caractere não classificado...")
                raise Exception("Caractere não classificado...")
        if saldo_de_parenteses != 0:
            raise Exception("Saldo de parênteses diferente de zero...")
