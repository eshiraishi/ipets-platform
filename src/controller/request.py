from typing import List
from fastapi import APIRouter, HTTPException, Response
from bson import json_util
from .utils import common_parameters
from ..model.request import RequestModel, UpdateRequestModel
from ..model.utils import PyObjectId
from fastapi import status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from typing_extensions import Annotated

router = APIRouter(
    prefix="/requests",
    tags=["Requests"],
)


@router.post(
    "/", response_description="Add new request", response_model=RequestModel
)
async def create_request(
    body: UpdateRequestModel,
    commons: Annotated[dict, Depends(common_parameters)],
):
    body = jsonable_encoder(body)
    new_document = await commons["db"]["requests"].insert_one(body)
    created_document = await commons["db"]["requests"].find_one(
        {"_id": new_document.inserted_id}
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=json_util.dumps(created_document),
    )


@router.get(
    "/",
    response_description="List all requests",
    response_model=List[RequestModel],
)
async def list_requests(commons: Annotated[dict, Depends(common_parameters)]):
    documents = await commons["db"]["requests"].find().to_list(None)
    return documents


@router.get(
    "/{doc_id}",
    response_description="Get a single request",
    response_model=RequestModel,
)
async def show_request(
    doc_id: PyObjectId, commons: Annotated[dict, Depends(common_parameters)]
):
    document = await commons["db"]["requests"].find_one({"_id": doc_id})
    if document is not None:
        return document

    raise HTTPException(status_code=404, detail=f"request {doc_id} not found")


@router.put(
    "/{doc_id}",
    response_description="Update a request",
    response_model=RequestModel,
)
async def update_request(
    doc_id: PyObjectId,
    body: UpdateRequestModel,
    commons: Annotated[dict, Depends(common_parameters)],
):
    update_set = {k: v for k, v in body.dict().items() if v is not None}

    if len(update_set) >= 1:
        update_result = await commons["db"]["requests"].update_one(
            {"_id": doc_id}, {"$set": update_set}
        )

        if update_result.modified_count == 1:
            if (
                updated_document := await commons["db"]["requests"].find_one(
                    {"_id": doc_id}
                )
            ) is not None:
                return updated_document

    if (
        existing_document := await commons["db"]["requests"].find_one(
            {"_id": doc_id}
        )
    ) is not None:
        return existing_document

    raise HTTPException(status_code=404, detail=f"request {doc_id} not found")


@router.delete("/{doc_id}", response_description="Delete a request")
async def delete_request(
    doc_id: PyObjectId, commons: Annotated[dict, Depends(common_parameters)]
):
    delete_result = await commons["db"]["requests"].delete_one({"_id": doc_id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"request {doc_id} not found")
