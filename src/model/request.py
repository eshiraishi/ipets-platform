from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, constr
from .utils import PyObjectId
from . import REGEX_OBJECT_ID


class RequestModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    # consumerId: PyObjectId
    consumerId: constr(regex=REGEX_OBJECT_ID)
    # serviceId: PyObjectId
    serviceId: constr(regex=REGEX_OBJECT_ID)
    date: str
    status: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateRequestModel(BaseModel):
    # consumerId: Optional[PyObjectId]
    consumerId: Optional[constr(regex=REGEX_OBJECT_ID)]
    # serviceId: Optional[PyObjectId]
    serviceId: Optional[constr(regex=REGEX_OBJECT_ID)]
    date: Optional[str]
    status: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
