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


class ProviderModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    cnpj: constr(regex=REGEX_CNPJ)
    name: str
    email: EmailStr
    address: Address
    bankAccount: BankAccount
    avatar: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateProviderModel(BaseModel):
    cnpj: Optional[constr(regex=REGEX_CNPJ)]
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[SecretStr]
    address: Optional[Address]
    bankAccount: Optional[BankAccount]
    avatar: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
