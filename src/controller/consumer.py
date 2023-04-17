from typing import List
from fastapi import APIRouter, HTTPException, Response
from bson import json_util
from .utils import common_parameters
from ..model.consumer import ConsumerModel, UpdateConsumerModel
from ..model.utils import PyObjectId
from fastapi import status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from typing_extensions import Annotated

router = APIRouter(
    prefix="/consumers",
    tags=["Consumers"],
)


@router.post(
    "/", response_description="Add new consumer", response_model=ConsumerModel
)
async def create_consumer(
    body: UpdateConsumerModel,
    commons: Annotated[dict, Depends(common_parameters)],
):
    body = jsonable_encoder(body)
    new_document = await commons["db"]["consumers"].insert_one(body)
    print("NEW DOCUMENT", new_document)
    created_document = await commons["db"]["consumers"].find_one(
        {"_id": new_document.inserted_id}
    )
    print("CREATED DOCUMENT", created_document)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=json_util.dumps(created_document),
    )


@router.get(
    "/",
    response_description="List all consumers",
    response_model=List[ConsumerModel],
)
async def list_consumers(commons: Annotated[dict, Depends(common_parameters)]):
    documents = await commons["db"]["consumers"].find().to_list(None)
    return documents


@router.get(
    "/{doc_id}",
    response_description="Get a single consumer",
    response_model=ConsumerModel,
)
async def show_consumer(
    doc_id: PyObjectId, commons: Annotated[dict, Depends(common_parameters)]
):
    document = await commons["db"]["consumers"].find_one({"_id": doc_id})
    if document is not None:
        return document

    raise HTTPException(status_code=404, detail=f"consumer {doc_id} not found")


@router.put(
    "/{doc_id}",
    response_description="Update a consumer",
    response_model=ConsumerModel,
)
async def update_consumer(
    doc_id: PyObjectId,
    body: UpdateConsumerModel,
    commons: Annotated[dict, Depends(common_parameters)],
):
    update_set = {k: v for k, v in body.dict().items() if v is not None}

    if len(update_set) >= 1:
        update_result = await commons["db"]["consumers"].update_one(
            {"_id": doc_id}, {"$set": update_set}
        )

        if update_result.modified_count == 1:
            if (
                updated_document := await commons["db"]["consumers"].find_one(
                    {"_id": doc_id}
                )
            ) is not None:
                return updated_document

    if (
        existing_document := await commons["db"]["consumers"].find_one(
            {"_id": doc_id}
        )
    ) is not None:
        return existing_document

    raise HTTPException(status_code=404, detail=f"consumer {doc_id} not found")


@router.delete("/{doc_id}", response_description="Delete a consumer")
async def delete_consumer(
    doc_id: PyObjectId, commons: Annotated[dict, Depends(common_parameters)]
):
    delete_result = await commons["db"]["consumers"].delete_one(
        {"_id": doc_id}
    )

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"consumer {doc_id} not found")
