from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, constr
from . import REGEX_OBJECT_ID
from .utils import PyObjectId


class ServiceModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str]
    price: float
    # providerId: PyObjectId
    providerId: constr(regex=REGEX_OBJECT_ID)
    thumbnail: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateServiceModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    # providerId: Optional[PyObjectId]
    providerId: Optional[constr(regex=REGEX_OBJECT_ID)]
    thumbnail: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
