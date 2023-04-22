from fastapi import APIRouter, HTTPException, Response
from bson import json_util
from .utils import common_parameters
from ..model.service import ServiceModel, UpdateServiceModel
from ..model.utils import PyObjectId
from fastapi import status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from typing_extensions import Annotated

router = APIRouter(
    prefix="/services",
    tags=["Services"],
)


@router.post(
    "/", response_description="Add new service", response_model=ServiceModel
)
async def create_service(
    body: UpdateServiceModel,
    commons: Annotated[dict, Depends(common_parameters)],
):
    body = jsonable_encoder(body)
    new_document = await commons["db"]["services"].insert_one(body)
    created_document = await commons["db"]["services"].find_one(
        {"_id": new_document.inserted_id}
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=json_util.dumps(created_document),
    )


@router.get(
    "/",
    response_description="list all services",
    response_model=list[ServiceModel],
)
async def list_services(commons: Annotated[dict, Depends(common_parameters)]):
    documents = await commons["db"]["services"].find().to_list(None)
    return documents


@router.get(
    "/{document_id}",
    response_description="Get a single service",
    response_model=ServiceModel,
)
async def show_service(
    document_id: PyObjectId,
    commons: Annotated[dict, Depends(common_parameters)],
):
    document = await commons["db"]["services"].find_one({"_id": document_id})
    if document is not None:
        return document

    raise HTTPException(
        status_code=404, detail=f"service {document_id} not found"
    )


@router.put(
    "/{document_id}",
    response_description="Update a service",
    response_model=ServiceModel,
)
async def update_service(
    document_id: PyObjectId,
    body: UpdateServiceModel,
    commons: Annotated[dict, Depends(common_parameters)],
):
    update_set = {k: v for k, v in body.dict().items() if v is not None}

    if len(update_set) >= 1:
        update_result = await commons["db"]["services"].update_one(
            {"_id": document_id}, {"$set": update_set}
        )

        if update_result.modified_count == 1:
            if (
                updated_document := await commons["db"]["services"].find_one(
                    {"_id": document_id}
                )
            ) is not None:
                return updated_document

    if (
        existing_document := await commons["db"]["services"].find_one(
            {"_id": document_id}
        )
    ) is not None:
        return existing_document

    raise HTTPException(
        status_code=404, detail=f"service {document_id} not found"
    )


@router.delete("/{document_id}", response_description="Delete a service")
async def delete_service(
    document_id: PyObjectId,
    commons: Annotated[dict, Depends(common_parameters)],
):
    delete_result = await commons["db"]["services"].delete_one(
        {"_id": document_id}
    )

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=404, detail=f"service {document_id} not found"
    )
