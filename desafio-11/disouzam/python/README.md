# Introdução


# Verificação do código com Pylint

O comando a seguir altera o diretório para a pasta do desafio:

```shell
cd desafio-11/disouzam/python
```

Executando dentro da pasta do desafio (desafio-11/disouzam/python), o comando para verificar o
código através do Pylint é:

```python
pylint --rcfile=../../../ci/pylint3.rc primos_em_pi.py
```

# Como executar o script

Esse código foi testado com a versão 3.11.2 do Python e pode apresentar alguma instabilidade com
o Python 3.11.8 (não foi checado contra essa versão).

Executando dentro da pasta do desafio (desafio-11/disouzam/python), o comando é:

```python
python -m primos_em_pi pi-1M.txt
```

# Profiling

Alguns experimentos foram feitos usando cProfile, tanto diretamente via linha de comando:

```shell
python -m cProfile -o profiling-results.prof -m primos_em_pi pi-1M.txt
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
- [The Python Profiles](https://docs.python.org/3/library/profile.html#introduction-to-the-profilers)
- [How to Profile Python Code With cProfile](https://www.turing.com/kb/python-code-with-cprofile)
- [Profiling a python 3.6 module from the command line](https://stackoverflow.com/questions/54465048/profiling-a-python-3-6-module-from-the-command-line)