# ipets-platform

Repositório contendo o código da plataforma para o iPets, aplicativo voltado para contratacao de servicos para pets. Parte do projeto do grupo 21 na disciplina de Engenharia de Software, ministrada em 2023.1 na UFABC.

Como gerar o servidor:

```bash
python -m pip install --upgrade
pip install virtualenv
python -m virtualenv virtualenv
.\virtualenv\Scripts\activate
pip install -r dev-requirements.txt
fastapi-codegen --input openapi.yml --output app
```

Como iniciar o servidor:

```shell
uvicorn src.main:app --reload
```
