from primos_em_pi import filtra_lista_primos_sobrepostos


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
