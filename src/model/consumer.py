
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, constr
from . import REGEX_CPF
from .utils import Address, CreditCard, Pet, PyObjectId


class ConsumerModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    cpf: constr(regex=REGEX_CPF) | None
    name: str | None
    email: EmailStr | None
    password: str | None
    address: Address | None
    creditCard: CreditCard | None
    avatar: str | None
    pets: list[Pet] | None
    phone: str | None
    birthDate: str | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateConsumerModel(BaseModel):
    cpf: constr(regex=REGEX_CPF) | None
    name: str | None
    email: EmailStr | None
    password: str | None
    address: Address | None
    creditCard: CreditCard | None
    avatar: str | None
    pets: list[Pet] | None
    phone: str | None
    birthDate: str | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
