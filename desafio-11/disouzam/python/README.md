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
python -m primos_em_pi datafile
```