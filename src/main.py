from fastapi import FastAPI, Depends
from .controller import provider, service
from .model.utils import get_database


app = FastAPI(
    title="iPets",
    description="Especificacao dos contratos disponibilizados pela plataforma do aplicativo iPets, um\naplicativo para contratacao de servicos para pets.\nParte do projeto do grupo 21 na disciplina de Engenharia de Software, ministrada em\n2023.1 na UFABC.",
    version="0.1.0",
    servers=[{"url": "http://localhost:8080/"}],
    dependencies=[Depends(get_database)],
)
app.include_router(provider.router)
app.include_router(service.router)