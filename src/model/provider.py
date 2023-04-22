from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, constr
from . import REGEX_CNPJ
from .utils import Address, BankAccount, PyObjectId


class ProviderModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    cnpj: constr(regex=REGEX_CNPJ) | None
    name: str | None
    email: EmailStr | None
    password: str | None
    address: Address | None
    bankAccount: BankAccount | None
    avatar: str | None
    phone: str | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateProviderModel(BaseModel):
    cnpj: constr(regex=REGEX_CNPJ) | None
    name: str | None
    email: EmailStr | None
    password: str | None
    address: Address | None
    bankAccount: BankAccount | None
    avatar: str | None
    phone: str | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
