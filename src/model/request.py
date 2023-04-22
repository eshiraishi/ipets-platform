from bson import ObjectId
from pydantic import BaseModel, Field, constr
from .utils import PyObjectId
from . import REGEX_OBJECT_ID


class RequestModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    consumerId: constr(regex=REGEX_OBJECT_ID)
    serviceId: constr(regex=REGEX_OBJECT_ID)
    date: str
    status: str | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateRequestModel(BaseModel):
    consumerId: constr(regex=REGEX_OBJECT_ID) | None
    serviceId: constr(regex=REGEX_OBJECT_ID) | None
    date: str | None
    status: str | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
