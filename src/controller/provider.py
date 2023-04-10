from typing import List
from fastapi import APIRouter, HTTPException, Response

from .utils import common_parameters
from ..model.provider import ProviderModel, UpdateProviderModel
from fastapi import status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from typing_extensions import Annotated

router = APIRouter(
    prefix="/providers",
    tags=["Providers"],
)


@router.put("/", response_description="Add new provider", response_model=ProviderModel)
async def create_provider(
    provider: ProviderModel, commons: Annotated[dict, Depends(common_parameters)]
):
    provider = jsonable_encoder(provider)
    new_provider = await commons["db"]["providers"].insert_one(provider)
    created_provider = await commons["db"]["providers"].find_one(
        {"_id": new_provider.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_provider)


@router.get(
    "/", response_description="List all providers", response_model=List[ProviderModel]
)
async def list_providers(commons: Annotated[dict, Depends(common_parameters)]):
    providers = await commons["db"]["providers"].find().to_list(1000)
    return providers


@router.get(
    "/{id}", response_description="Get a single provider", response_model=ProviderModel
)
async def show_provider(id: str, commons: Annotated[dict, Depends(common_parameters)]):
    if (provider := await commons["db"]["providers"].find_one({"_id": id})) is not None:
        return provider

    raise HTTPException(status_code=404, detail=f"provider {id} not found")


@router.patch(
    "/{id}", response_description="Update a provider", response_model=ProviderModel
)
async def update_provider(
    id: str,
    provider: UpdateProviderModel,
    commons: Annotated[dict, Depends(common_parameters)],
):
    provider = {k: v for k, v in provider.dict().items() if v is not None}

    if len(provider) >= 1:
        update_result = await commons["db"]["providers"].update_one(
            {"_id": id}, {"$set": provider}
        )

        if update_result.modified_count == 1:
            if (
                updated_provider := await commons["db"]["providers"].find_one(
                    {"_id": id}
                )
            ) is not None:
                return updated_provider

    if (
        existing_provider := await commons["db"]["providers"].find_one({"_id": id})
    ) is not None:
        return existing_provider

    raise HTTPException(status_code=404, detail=f"provider {id} not found")


@router.delete("/{id}", response_description="Delete a provider")
async def delete_provider(
    id: str, commons: Annotated[dict, Depends(common_parameters)]
):
    delete_result = await commons["db"]["providers"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"provider {id} not found")
