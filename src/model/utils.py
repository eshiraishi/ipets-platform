from typing import Optional
from bson import ObjectId
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os


class Address(BaseModel):
    street: Optional[str]
    number: Optional[str]
    complement: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postcode: Optional[str]


class BankAccount(BaseModel):
    agency: Optional[str]
    accountNumber: Optional[str]
    digit: Optional[str]


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
    code: Optional[str]
    name: Optional[str]
    expirationDate: Optional[str]
    cvv: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Pet(BaseModel):
    name: Optional[str]
    species: Optional[str]
    race: Optional[str]
    age: Optional[int]
    description: Optional[str]
    avatar: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
