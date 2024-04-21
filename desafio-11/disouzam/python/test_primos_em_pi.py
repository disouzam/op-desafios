from .primos_em_pi import filtra_lista_primos_sobrepostos


def test_sobreposicao_lista_vazia():
    lista_primos_sobrepostos = []
    lista_primos_sobrepostos = filtra_lista_primos_sobrepostos(
        lista_primos_sobrepostos)
    assert len(lista_primos_sobrepostos) == 0


def test_sobreposicao_lista_com_um_elemento():
    lista_primos_sobrepostos = [(41, 1, 2)]
    lista_primos_sobrepostos = filtra_lista_primos_sobrepostos(
        lista_primos_sobrepostos)
    assert len(lista_primos_sobrepostos) == 1
    assert lista_primos_sobrepostos[0] == (41, 1, 2)


def test_sobreposicao_lista_com_4_elementos_inicio():
    lista_primos_sobrepostos = [
        (41, 1, 2),
        (4159, 1, 4),
        (5, 3, 3),
        (59, 3, 4)
    ]
    lista_primos_sobrepostos = filtra_lista_primos_sobrepostos(
        lista_primos_sobrepostos)
    assert len(lista_primos_sobrepostos) == 2
    assert lista_primos_sobrepostos == [
        (41, 1, 2),
        (59, 3, 4)
    ]


def test_sobreposicao_lista_com_4_elementos_segunda_sequencia():
    lista_primos_sobrepostos = [
        (653, 6, 8),
        (5, 7, 7),
        (53, 7, 8),
        (3, 8, 8)
    ]
    lista_primos_sobrepostos = filtra_lista_primos_sobrepostos(
        lista_primos_sobrepostos)
    assert len(lista_primos_sobrepostos) == 1
    assert lista_primos_sobrepostos == [
        (653, 6, 8)
    ]


def test_sobreposicao_lista_com_11_elementos_terceira_sequencia():
    lista_primos_sobrepostos = [
        (5, 9, 9),
        (5897, 9, 12),
        (89, 10, 11),
        (97, 11, 12),
        (7, 12, 12),
        (79, 12, 13),
        (9323, 13, 16),
        (3, 14, 14),
        (2, 15, 15),
        (23, 15, 16),
        (3, 16, 16)
    ]
    lista_primos_sobrepostos = filtra_lista_primos_sobrepostos(
        lista_primos_sobrepostos)
    assert len(lista_primos_sobrepostos) == 6
    assert lista_primos_sobrepostos == [
        (5, 9, 9),
        (89, 10, 11),
        (79, 12, 13),
        (3, 14, 14),
        (2, 15, 15),
        (3, 16, 16)
    ]


def test_sobreposicao_lista_com_6_elementos_terceira_sequencia():
    lista_primos_sobrepostos = [
        (5, 9, 9),
        (89, 10, 11),
        (7, 12, 12),
        (79, 12, 13),
        (3, 14, 14),
        (23, 15, 16)
    ]
    lista_primos_sobrepostos = filtra_lista_primos_sobrepostos(
        lista_primos_sobrepostos)
    assert len(lista_primos_sobrepostos) == 5
    assert lista_primos_sobrepostos == [
        (5, 9, 9),
        (89, 10, 11),
        (79, 12, 13),
        (3, 14, 14),
        (23, 15, 16)
    ]


def test_sobreposicao_lista_com_7_elementos_terceira_sequencia():
    lista_primos_sobrepostos = [
        (5, 9, 9),
        (89, 10, 11),
        (7, 12, 12),
        (79, 12, 13),
        (3, 14, 14),
        (2, 15, 15),
        (3, 16, 16)
    ]
    lista_primos_sobrepostos = filtra_lista_primos_sobrepostos(
        lista_primos_sobrepostos)
    assert len(lista_primos_sobrepostos) == 6
    assert lista_primos_sobrepostos == [
        (5, 9, 9),
        (89, 10, 11),
        (79, 12, 13),
        (3, 14, 14),
        (2, 15, 15),
        (3, 16, 16)
    ]
