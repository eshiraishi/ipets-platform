from fastapi import APIRouter, HTTPException, Response
from bson import json_util
from .utils import common_parameters
from ..model.provider import ProviderModel, UpdateProviderModel
from ..model.utils import PyObjectId
from fastapi import status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from typing_extensions import Annotated

router = APIRouter(
    prefix="/providers",
    tags=["Providers"],
)


@router.post(
    "/", response_description="Add new provider", response_model=ProviderModel
)
async def create_provider(
    body: UpdateProviderModel,
    commons: Annotated[dict, Depends(common_parameters)],
):
    body = jsonable_encoder(body)
    new_document = await commons["db"]["providers"].insert_one(body)
    created_document = await commons["db"]["providers"].find_one(
        {"_id": new_document.inserted_id}
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=json_util.dumps(created_document),
    )


@router.get(
    "/",
    response_description="list all providers",
    response_model=list[ProviderModel],
)
async def list_providers(commons: Annotated[dict, Depends(common_parameters)]):
    documents = await commons["db"]["providers"].find().to_list(None)
    return documents


@router.get(
    "/{document_id}",
    response_description="Get a single provider",
    response_model=ProviderModel,
)
async def show_provider(
    document_id: PyObjectId,
    commons: Annotated[dict, Depends(common_parameters)],
):
    document = await commons["db"]["providers"].find_one({"_id": document_id})
    if document is not None:
        return document

    raise HTTPException(
        status_code=404, detail=f"provider {document_id} not found"
    )


@router.put(
    "/{document_id}",
    response_description="Update a provider",
    response_model=ProviderModel,
)
async def update_provider(
    document_id: PyObjectId,
    body: UpdateProviderModel,
    commons: Annotated[dict, Depends(common_parameters)],
):
    update_set = {k: v for k, v in body.dict().items() if v is not None}

    if len(update_set) >= 1:
        update_result = await commons["db"]["providers"].update_one(
            {"_id": document_id}, {"$set": update_set}
        )

        if update_result.modified_count == 1:
            if (
                updated_document := await commons["db"]["providers"].find_one(
                    {"_id": document_id}
                )
            ) is not None:
                return updated_document

    if (
        existing_document := await commons["db"]["providers"].find_one(
            {"_id": document_id}
        )
    ) is not None:
        return existing_document

    raise HTTPException(
        status_code=404, detail=f"provider {document_id} not found"
    )


@router.delete("/{document_id}", response_description="Delete a provider")
async def delete_provider(
    document_id: PyObjectId,
    commons: Annotated[dict, Depends(common_parameters)],
):
    delete_result = await commons["db"]["providers"].delete_one(
        {"_id": document_id}
    )

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=404, detail=f"provider {document_id} not found"
    )
