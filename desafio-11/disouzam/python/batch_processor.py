"""Terceira implementação dos primos em Pi
"""
from __future__ import annotations
import cProfile
import sys
import os
from os import walk
from os.path import join

from numpy import full


def main() -> None:
    """main():
    """
    diretorio_raiz = os.path.dirname(os.path.realpath(__file__))
    pasta_de_dados_de_entrada = "entradas"
    caminho_completo = join(diretorio_raiz, pasta_de_dados_de_entrada)
    lista_de_arquivos = get_all_input_files(caminho_completo)
    for arquivo in lista_de_arquivos:
        print(arquivo)


def get_all_input_files(folder):
    """Get all CSVs under a folder recursively
        Reference:
        https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    """
    txtlist = []
    result_list = []
    for (dirpath, _, filenames) in walk(folder):
        for filename in filenames:
            if filename.endswith(".txt"):
                txtlist.append(filename)

        txtlist.sort()

        for txt in txtlist:
            fulltxtpath = join(dirpath, txt)
            result_list.append(fulltxtpath)
    return txtlist


def debugger_is_active() -> bool:
    # TODO: Remover antes da submissão do PR
    """Return if the debugger is currently active

    # pylint: disable=line-too-long
    Source: https://stackoverflow.com/questions/38634988/check-if-program-runs-in-debug-mode/67065084
    """
    return hasattr(sys, 'gettrace') and sys.gettrace() is not None


if __name__ == "__main__":
    # TODO: Remover antes da submissão do PR
    if debugger_is_active():
        pr = cProfile.Profile(builtins=False, subcalls=False)
        pr.enable()

    main()

    # TODO: Remover antes da submissão do PR
    if debugger_is_active():
        pr.disable()
        pr.dump_stats("profiling-results.prof")
