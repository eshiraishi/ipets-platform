from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, SecretStr, constr

from . import REGEX_CNPJ
from ..model.utils import Address, BankAccount


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class ServiceModel(BaseModel):
    id: PyObjectId
    name: str
    description: Optional[str]
    price: float
    providerId: PyObjectId
    thumbnail: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UpdateServiceModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    providerId: Optional[PyObjectId]
    thumbnail: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        