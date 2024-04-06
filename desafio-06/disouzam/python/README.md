# Introdução

Processa uma palavra ou frase e retorna todas as combinações possíveis de anagramas com palavras presentes no arquivo desafio-06/disouzam/python/words.txt (cópia local do arquivo disponível em https://osprogramadores.com/desafios/d06/words.txt)


# Verificação do código com Pylint

O comando a seguir altera o diretório para a pasta do desafio:

```shell
cd desafio-06/disouzam/python
```

Executando dentro da pasta do desafio (desafio-06/disouzam/python), o comando para verificar o código através do Pylint é:

```shell
pylint --rcfile=../../../ci/pylint3.rc anagrama.py
```

# Como executar o script

Esse código foi testado com a versão 3.12.1 do Python e pode apresentar alguma instabilidade com o Python 3.11 (não foi checado contra essa versão).

Executando dentro da pasta do desafio (desafio-06/disouzam/python), o comando é (com uma palavra de exemplo):

```shell
python -m anagrama "vermelho"
```

Exemplo com uma frase:

```shell
python -m anagrama "oi gente"
```

Ambos os exemplos foram extraídos do texto original do desafio no site [OsProgramadores](https://osprogramadores.com/desafios/d06/)

Exemplos com caracteres inválidos:

```shell
python -m anagrama "Hello world!"
```

```shell
python -m anagrama "Hello world! Hoje é dia 24 de março de 2024."
```

# Profiling

Alguns experimentos foram feitos usando cProfile, tanto diretamente via linha de comando:

```shell
python -m cProfile -o profiling-results.prof -m anagrama "hoje ainda nao choveu"
```

ou via instrumentação dentro da chamada da função main:

```python
import cProfile

def main():
    pass

if __name__ == "__main__":
    pr = cProfile.Profile(builtins=False, subcalls=False)
    pr.enable()
    main(sys.argv)
    pr.disable()
    pr.dump_stats("profiling-results.prof")
```

Tentei usar o RunSnakeRun (recomendado por esse vídeo antigo no YouTube: [Python Profiling](https://www.youtube.com/watch?v=QJwVYlDzAXs)) mas não funcionou de forma imediata no Windows. Deve ser necessário uma configuração mais elaborada.

O [SnakeViz](https://github.com/jiffyclub/snakeviz) no entanto funcionou de forma fácil e pode ser chamado dessa forma

```shell
python -m snakeviz profiling-results.prof
```

# Referências

- [PEP 257 – Docstring Conventions](https://peps.python.org/pep-0257/)
- [Advanced Python with Joe Marini](https://www.linkedin.com/learning/advanced-python/function-documentation-strings)
- [The Python Profiles](https://docs.python.org/3/library/profile.html#introduction-to-the-profilers)
- [How to Profile Python Code With cProfile](https://www.turing.com/kb/python-code-with-cprofile)
- [Profiling a python 3.6 module from the command line](https://stackoverflow.com/questions/54465048/profiling-a-python-3-6-module-from-the-command-line)