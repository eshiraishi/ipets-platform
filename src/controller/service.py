from typing import List
from fastapi import APIRouter, HTTPException, Response

from .utils import common_parameters
from ..model.service import ServiceModel, UpdateServiceModel
from fastapi import status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from typing_extensions import Annotated

router = APIRouter(
    prefix="/services",
    tags=["Services"],
)


@router.put("/", response_description="Add new service", response_model=ServiceModel)
async def create_service(
    service: ServiceModel, commons: Annotated[dict, Depends(common_parameters)]
):
    service = jsonable_encoder(service)
    new_service = await commons["db"]["services"].insert_one(service)
    created_service = await commons["db"]["services"].find_one(
        {"_id": new_service.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_service)


@router.get(
    "/", response_description="List all services", response_model=List[ServiceModel]
)
async def list_services(commons: Annotated[dict, Depends(common_parameters)]):
    services = await commons["db"]["services"].find().to_list(1000)
    return services


@router.get(
    "/{id}", response_description="Get a single service", response_model=ServiceModel
)
async def show_service(id: str, commons: Annotated[dict, Depends(common_parameters)]):
    if (service := await commons["db"]["services"].find_one({"_id": id})) is not None:
        return service

    raise HTTPException(status_code=404, detail=f"service {id} not found")


@router.patch(
    "/{id}", response_description="Update a service", response_model=ServiceModel
)
async def update_service(
    id: str,
    service: UpdateServiceModel,
    commons: Annotated[dict, Depends(common_parameters)],
):
    service = {k: v for k, v in service.dict().items() if v is not None}

    if len(service) >= 1:
        update_result = await commons["db"]["services"].update_one(
            {"_id": id}, {"$set": service}
        )

        if update_result.modified_count == 1:
            if (
                updated_service := await commons["db"]["services"].find_one(
                    {"_id": id}
                )
            ) is not None:
                return updated_service

    if (
        existing_service := await commons["db"]["services"].find_one({"_id": id})
    ) is not None:
        return existing_service

    raise HTTPException(status_code=404, detail=f"service {id} not found")


@router.delete("/{id}", response_description="Delete a service")
async def delete_service(
    id: str, commons: Annotated[dict, Depends(common_parameters)]
):
    delete_result = await commons["db"]["services"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"service {id} not found")
