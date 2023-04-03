# generated by fastapi-codegen:
#   filename:  openapi.yml
#   timestamp: 2023-04-02T00:41:28+00:00

from __future__ import annotations
import os
from typing import Dict
from fastapi import FastAPI, HTTPException, Path, status
from pydantic import constr
import motor.motor_asyncio as motor
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from .model import (
    REGEX_OBJECT_ID,
    TEMPLATE_404,
    UpdateConsumerModel,
    ConsumerModel,
    UpdateProviderModel,
    ProviderModel,
    UpdateRequestModel,
    RequestListModel,
    RequestModel,
    UpdateServiceModel,
    ServiceListModel,
    ServiceModel,
)

client = motor.AsyncIOMotorClient(os.environ["MONGODB_URL"])
# client = motor.MotorClient(os.environ["MONGODB_URL"])
db = client.ipetsPlatform

app = FastAPI(
    title="iPets",
    description="Especificacao dos contratos disponibilizados pela plataforma do aplicativo iPets, um\naplicativo para contratacao de servicos para pets.\nParte do projeto do grupo 21 na disciplina de Engenharia de Software, ministrada em\n2023.1 na UFABC.",
    version="0.1.0",
    servers=[{"url": "http://localhost:8080/"}],
)


@app.put("/requests", response_model=RequestModel, tags=["Pedidos"])
async def create_request(body: UpdateRequestModel) -> JSONResponse:
    """
    Cadastra os dados de um novo pedido na plataforma
    """
    new_document = await db["requests"].insert_one(jsonable_encoder(body))
    created_document = await db["requests"].find_one({"_id": new_document.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_document)


@app.get("/requests/{object_id}", response_model=RequestModel, tags=["Pedidos"])
async def get_request_by_id(
    object_id: constr(regex=REGEX_OBJECT_ID) = Path(alias="objectId"),
) -> JSONResponse:
    """
    Obtem os dados de um pedido existente por ID na plataforma
    """
    if (document := await db["requests"].find_one({"_id": object_id})) is not None:
        return JSONResponse(content=document)
    raise HTTPException(status_code=404, detail=TEMPLATE_404.format(object_id))


@app.patch("/requests/{object_id}", response_model=RequestModel, tags=["Pedidos"])
async def update_request_by_id(
    body: UpdateRequestModel,
    object_id: constr(regex=REGEX_OBJECT_ID) = Path(alias="objectId"),
) -> JSONResponse:
    """
    Atualiza os dados de um pedido existente por ID na plataforma
    """
    document: Dict = {
        key: value for key, value in body.dict().items() if value is not None
    }
    if len(document) >= 1:
        update_result = await db["requests"].update_one(
            {"_id": object_id}, {"$set": document}
        )

        if update_result.modified_count == 1:
            if (
                updated_document := await db["requests"].find_one({"_id": object_id})
            ) is not None:
                return JSONResponse(content=updated_document)

    if (
        existing_document := await db["requests"].find_one({"_id": object_id})
    ) is not None:
        return existing_document

    raise HTTPException(status=404, detail=TEMPLATE_404.format(object_id))


@app.put("/services", response_model=ServiceModel, tags=["Servicos"])
async def create_service(body: UpdateServiceModel) -> JSONResponse:
    """
    Cadastra os dados de um novo servico na plataforma
    """
    new_document = await db["services"].insert_one(jsonable_encoder(body))
    created_document = await db["services"].find_one({"_id": new_document.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_document)


@app.get("/services", response_model=ServiceListModel, tags=["Utilidades"])
async def get_all_services() -> JSONResponse:
    """
    Obtem todos os servicos existentes na plataforma
    """
    # TODO: Tirar hardcode usando skip e limit:
    # https://pymongo.readthedocs.io/en/3.11.0/api/pymongo/collection.html#pymongo.collection.Collection.find
    services = await db["services"].find().to_list(1000)
    service_list: ServiceListModel = ServiceListModel(
        data=[ServiceModel.parse_obj(service) for service in services]
    )
    return JSONResponse(content=service_list)


@app.get("/services/{object_id}", response_model=ServiceModel, tags=["Servicos"])
async def get_service_by_id(
    object_id: constr(regex=REGEX_OBJECT_ID) = Path(alias="objectId"),
) -> JSONResponse:
    """
    Obtem os dados de um servico existente por ID na plataforma
    """
    if (document := await db["services"].find_one({"_id": object_id})) is not None:
        return JSONResponse(content=document)
    raise HTTPException(status_code=404, detail=TEMPLATE_404.format(object_id))


@app.patch("/services/{object_id}", response_model=ServiceModel, tags=["Servicos"])
async def update_service_by_id(
    body: UpdateServiceModel,
    object_id: constr(regex=REGEX_OBJECT_ID) = Path(alias="objectId"),
) -> JSONResponse:
    """
    Atualiza os dados de um servico existente por ID na plataforma
    """
    document: Dict = {
        key: value for key, value in body.dict().items() if value is not None
    }
    if len(document) >= 1:
        update_result = await db["services"].update_one(
            {"_id": object_id}, {"$set": document}
        )

        if update_result.modified_count == 1:
            if (
                updated_document := await db["services"].find_one({"_id": object_id})
            ) is not None:
                return JSONResponse(content=updated_document)

    if (
        existing_document := await db["services"].find_one({"_id": object_id})
    ) is not None:
        return existing_document

    raise HTTPException(status=404, detail=TEMPLATE_404.format(object_id))


@app.delete("/services/{object_id}", response_model=None, tags=["Servicos"])
async def remove_service_by_id(
    object_id: constr(regex=REGEX_OBJECT_ID) = Path(alias="objectId"),
) -> None:
    """
    Remove os dados de um servico existente por ID na plataforma
    """
    delete_result = await db["services"].delete_one({"_id": object_id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=TEMPLATE_404.format(object_id))


@app.get(
    "/user/{object_id}/requests", response_model=RequestListModel, tags=["Utilidades"]
)
async def get_requests_by_provider_id(
    object_id: constr(regex=REGEX_OBJECT_ID) = Path(alias="objectId"),
) -> JSONResponse:
    """
    Obtem os dados de todos os pedidos de servicos feitos para um usuario prestador existente por ID
    """
    # TODO
    pass


@app.put(
    "/users/consumers", response_model=ConsumerModel, tags=["Usuarios consumidores"]
)
async def create_consumer(body: UpdateConsumerModel) -> JSONResponse:
    """
    Cadastra os dados de um novo usuario consumidor na plataforma
    """
    new_document = await db["consumers"].insert_one(jsonable_encoder(body))
    created_document = await db["consumers"].find_one({"_id": new_document.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_document)


@app.get(
    "/users/consumers/{object_id}",
    response_model=ConsumerModel,
    tags=["Usuarios consumidores"],
)
async def get_consumer_by_id(
    object_id: constr(regex=REGEX_OBJECT_ID) = Path(alias="objectId"),
) -> JSONResponse:
    """
    Obtem os dados de um usuario consumidor existente por ID na plataforma
    """
    if (document := await db["consumers"].find_one({"_id": object_id})) is not None:
        return JSONResponse(content=document)
    raise HTTPException(status_code=404, detail=TEMPLATE_404.format(object_id))


@app.patch(
    "/users/consumers/{object_id}",
    response_model=ConsumerModel,
    tags=["Usuarios consumidores"],
)
async def update_consumer_by_id(
    body: UpdateConsumerModel,
    object_id: constr(regex=REGEX_OBJECT_ID) = Path(alias="objectId"),
) -> JSONResponse:
    """
    Atualiza os dados de usuario consumidor existente por ID na plataforma
    """
    document: Dict = {
        key: value for key, value in body.dict().items() if value is not None
    }
    if len(document) >= 1:
        update_result = await db["consumers"].update_one(
            {"_id": object_id}, {"$set": document}
        )

        if update_result.modified_count == 1:
            if (
                updated_document := await db["consumers"].find_one({"_id": object_id})
            ) is not None:
                return JSONResponse(content=updated_document)

    if (
        existing_document := await db["consumers"].find_one({"_id": object_id})
    ) is not None:
        return existing_document

    raise HTTPException(status=404, detail=TEMPLATE_404.format(object_id))


@app.delete(
    "/users/consumers/{object_id}", response_model=None, tags=["Usuarios consumidores"]
)
async def remove_consumer_by_id(
    object_id: constr(regex=REGEX_OBJECT_ID) = Path(alias="objectId"),
) -> None:
    """
    Remove os dados de um usuario consumidor existente por ID na plataforma
    """
    delete_result = await db["consumers"].delete_one({"_id": object_id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=TEMPLATE_404.format(object_id))


@app.put(
    "/users/providers", response_model=ProviderModel, tags=["Usuarios prestadores"]
)
async def create_provider(body: UpdateProviderModel) -> JSONResponse:
    """
    Cadastra os dados de um novo usuario prestador na plataforma
    """
    new_document = await db["providers"].insert_one(jsonable_encoder(body))
    created_document = await db["providers"].find_one({"_id": new_document.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_document)


@app.get(
    "/users/providers/{object_id}",
    response_model=ProviderModel,
    tags=["Usuarios prestadores"],
)
async def get_provider_by_id(
    object_id: constr(regex=REGEX_OBJECT_ID) = Path(alias="objectId"),
) -> JSONResponse:
    """
    Obtem os dados de um usuario prestador existente por ID na plataforma
    """
    if (document := await db["providers"].find_one({"_id": object_id})) is not None:
        return JSONResponse(content=document)
    raise HTTPException(status_code=404, detail=TEMPLATE_404.format(object_id))


@app.patch(
    "/users/providers/{object_id}",
    response_model=ProviderModel,
    tags=["Usuarios prestadores"],
)
async def update_provider_by_id(
    body: UpdateProviderModel,
    object_id: constr(regex=REGEX_OBJECT_ID) = Path(alias="objectId"),
) -> JSONResponse:
    """
    Atualiza os dados de usuario prestador existente por ID na plataforma
    """
    document: Dict = {
        key: value for key, value in body.dict().items() if value is not None
    }
    if len(document) >= 1:
        update_result = await db["providers"].update_one(
            {"_id": object_id}, {"$set": document}
        )

        if update_result.modified_count == 1:
            if (
                updated_document := await db["providers"].find_one({"_id": object_id})
            ) is not None:
                return JSONResponse(content=updated_document)

    if (
        existing_document := await db["providers"].find_one({"_id": object_id})
    ) is not None:
        return existing_document

    raise HTTPException(status=404, detail=TEMPLATE_404.format(object_id))


@app.delete(
    "/users/providers/{object_id}", response_model=None, tags=["Usuarios prestadores"]
)
async def remove_provider_by_id(
    object_id: constr(regex=REGEX_OBJECT_ID) = Path(alias="objectId"),
) -> None:
    """
    Remove os dados de um usuario prestador existente por ID na plataforma
    """
    delete_result = await db["providers"].delete_one({"_id": object_id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=TEMPLATE_404.format(object_id))
