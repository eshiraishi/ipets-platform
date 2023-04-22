from bson import ObjectId
from pydantic import BaseModel, Field, constr
from . import REGEX_OBJECT_ID
from .utils import PyObjectId


class ServiceModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str | None
    price: float
    providerId: constr(regex=REGEX_OBJECT_ID)
    thumbnail: str | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateServiceModel(BaseModel):
    name: str | None
    description: str | None
    price: float | None
    providerId: constr(regex=REGEX_OBJECT_ID) | None
    thumbnail: str | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
