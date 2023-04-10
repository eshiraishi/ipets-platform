from typing import Optional
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os


class Address(BaseModel):
    street: Optional[str]
    number: Optional[str]
    complement: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]


class BankAccount(BaseModel):
    agency: Optional[str]
    accountNumber: Optional[str]
    digit: Optional[str]


def get_database():
    client = AsyncIOMotorClient(os.environ["MONGODB_URL"])
    return client.ipetsPlatform
