from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, constr
from . import REGEX_CNPJ
from .utils import Address, BankAccount, PyObjectId


class ProviderModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    cnpj: constr(regex=REGEX_CNPJ)
    name: str
    email: EmailStr
    password: str
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
    password: Optional[str]
    address: Optional[Address]
    bankAccount: Optional[BankAccount]
    avatar: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
