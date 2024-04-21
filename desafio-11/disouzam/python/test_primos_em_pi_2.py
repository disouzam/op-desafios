"""Testes do novo módulo primos_em_py_2 sendo refatorado do módulo original
"""
from primos_em_pi_2 import obtem_primos_de_lista_de_inteiros


def test_obtem_primos_de_lista_de_inteiros_20_digitos_de_pi():
    digitos = ['1', '4', '1', '5', '9', '2', '6', '5', '3',
               '5', '8', '9', '7', '9', '3', '2', '3', '8', '4', '6']
    lista_primos = obtem_primos_de_lista_de_inteiros(digitos)
    assert len(lista_primos) == 0
