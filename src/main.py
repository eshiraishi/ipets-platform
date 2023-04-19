from fastapi import FastAPI, Depends
from .controller import provider, service, consumer, request
from .model.utils import get_database
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="iPets",
    description="Especificacao dos contratos disponibilizados pela plataforma do aplicativo iPets, um\naplicativo para contratacao de servicos para pets.\nParte do projeto do grupo 21 na disciplina de Engenharia de Software, ministrada em\n2023.1 na UFABC.",
    version="0.1.0",
    servers=[{"url": "http://ipets.azurewebsites.net/"}],
    dependencies=[Depends(get_database)],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        "http://localhost",
        "http://127.0.0.1",
        "http://0.0.0.0",
        "https://i-pets-six.vercel.app/",
        "http://ipets.azurewebsites.net/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(provider.router)
app.include_router(consumer.router)
app.include_router(service.router)
app.include_router(request.router)
