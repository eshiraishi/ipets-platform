from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, constr
from . import REGEX_CPF
from .utils import Address, CreditCard, Pet, PyObjectId


class ConsumerModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    cpf: constr(regex=REGEX_CPF)
    name: str
    email: EmailStr
    password: str
    address: Address
    creditCard: CreditCard
    avatar: Optional[str]
    pets: list[Pet]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateConsumerModel(BaseModel):
    cpf: Optional[constr(regex=REGEX_CPF)]
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    address: Optional[Address]
    creditCard: Optional[CreditCard]
    avatar: Optional[str]
    pets: Optional[list[Pet]]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
