# ipets-platform

Repositório contendo o código da plataforma para o iPets, aplicativo voltado para contratacao de servicos para pets. Parte do projeto do grupo 21 na disciplina de Engenharia de Software, ministrada em 2023.1 na UFABC.

Como gerar o servidor:

```shell
python -m pip install --upgrade
pip install virtualenv
python -m virtualenv virtualenv
.\virtualenv\Scripts\activate
pip install -r dev-requirements.txt
fastapi-codegen --input openapi.yml --output app
```

Como  gerar os requirements:

```shell
pip install -r dev-requirments.txt
```

No windows:

```shell
python -m piptools compile requirements.in --resolver=backtracking
```

No linux:

```shell
pip-compile requirements.in --resolver=backtracking
```

Como instalar as dependências:

```shell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Como iniciar o servidor:

```shell
uvicorn src.main:app --reload
```

Como executar os testes (aviso: irá apagar todos os registros):

```shell
pytest src/tests --envfile .envrc -x -l --tb=native -vv --cov=src --cov-report=xml --cov-config=.coveragerc
```

Como hospedar o back temporariamente na internet:

```shell
cloudflared tunnel --url http://localhost:8000
```
