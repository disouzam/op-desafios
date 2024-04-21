"""Classe primo
    Organiza as informações de um número primo posicionado nos decimais do número pi

    Como exemplo o número pi com 20 caracteres é:

    3.14159265358979323846

    Primos disjuntos (ou seja, que não compartilham caracteres nessa sequência de dígitos) são:
    41 (inícia na posicao 1 e termina na posição 2)
    59 (início: 3, fim: 4)
    2 (início: 5, fim: 5)
    653 (início: 6, fim: 8)
    5 (início: 9, fim: 9)
    89 (início: 10, fim: 11)
    7 (início: 12, fim: 12)
    9323 (início: 13, fim: 16)

    a posição zero representa o primeiro caractere após a vírgula, dígito 1, que não é primo
"""
from __future__ import annotations
from ctypes import ArgumentError


class primo(object):
    """primo
    Organiza as informações de um número primo posicionado nos decimais do número pi
    """

    def __init__(self, numero_primo: int, inicio: int, fim: int) -> None:
        """Construtor"""

        if inicio > fim:
            raise ArgumentError("Início não pode ser maior que fim.")

        self.numero_primo = numero_primo
        self.inicio = inicio
        self.fim = fim

    def __str__(self) -> str:
        """Representação como string para uso em print statements"""
        resultado = f"primo: {self.numero_primo}, "
        resultado += f"inicio: {self.inicio}, "
        resultado += f"fim: {self.fim}, "
        return resultado

    def numero_caracteres(self) -> int:
        return self.fim - self.inicio + 1

    def sobrepoe_outro_primo_parcialmente(self, outro_primo: primo) -> bool:
        """sobrepoe_outro_primo(outro_primo) -> bool:
        Retorna True se os intervalos de inicio e fim se sobrepoem
        """
        if self.fim < outro_primo.inicio or self.inicio > outro_primo.fim:
            return False
        else:
            return True

    def sobrepoe_outro_primo_completamente(self, outro_primo: primo) -> bool:
        """sobreposicao_completa(self, outro_primo) -> bool:
        Retorna True se o outro_primo é totalmente sobreposto pelo primo atual
        """
        if outro_primo.inicio >= self.inicio and outro_primo.fim <= self.fim:
            return True
        else:
            return False