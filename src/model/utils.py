from bson import ObjectId
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os


class Address(BaseModel):
    street: str | None
    number: str | None
    complement: str | None
    city: str | None
    state: str | None
    postcode: str | None


class BankAccount(BaseModel):
    agency: str | None
    accountNumber: str | None
    digit: str | None


def get_database():
    client = AsyncIOMotorClient(os.environ["MONGODB_URL"])
    return client["platform"]


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


class CreditCard(BaseModel):
    code: str | None
    name: str | None
    expirationDate: str | None
    cvv: str | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Pet(BaseModel):
    name: str | None
    species: str | None
    race: str | None
    age: int | None
    description: str | None
    avatar: str | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
