"""Configuracoes"""
from doctest import debug
import os
import sys
from numeros_primos import primo

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH, "desafio-11", "disouzam", "python"
)

sys.path.append(SOURCE_PATH)
print(sys.path)
