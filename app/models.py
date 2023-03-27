# generated by fastapi-codegen:
#   filename:  openapi.yml
#   timestamp: 2023-03-27T03:19:12+00:00

from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, SecretStr, constr


class ObjectId(BaseModel):
    __root__: constr(regex=r'^[a-fA-F\d]{24}$') = Field(
        ..., example='45cbc4a0e4123f6920000002'
    )


class Cpf(BaseModel):
    __root__: constr(regex=r'\d{11}') = Field(..., example='98202023025')


class Cnpj(BaseModel):
    __root__: constr(regex=r'\d{14}') = Field(..., example='31846757000124')


class Address(BaseModel):
    id: ObjectId
    street: str = Field(..., example='Av. Paulista')
    number: str = Field(..., example='1001')
    complement: Optional[str] = Field(None, example='apto 21')
    city: str = Field(..., example='Sao Paulo')
    state: str = Field(..., example='SP')
    zip: str = Field(..., example='01311000')


class BankAccount(BaseModel):
    id: ObjectId
    agency: str = Field(..., example='60883')
    accountNumber: str = Field(..., example='3413')
    digit: Optional[str] = Field(None, example='1')


class CreditCard(BaseModel):
    id: Optional[ObjectId] = None
    code: Optional[str] = Field(None, example='5118598797832798')
    name: Optional[str] = Field(None, example='ARIEL S DOS SANTOS')
    expirationDate: Optional[str] = Field(None, example='1994-11-05T08:15:30-05:00')
    verifyingDigits: Optional[str] = Field(None, example='183')


class Service(BaseModel):
    id: ObjectId
    serviceType: str = Field(..., example='Tosa')
    price: float = Field(..., example=89.9)
    providerId: ObjectId


class Request(BaseModel):
    id: ObjectId
    consumerId: ObjectId
    serviceId: ObjectId
    date: str = Field(..., example='1994-11-05T08:15:30-05:00')
    status: Optional[str] = Field(None, example='Rejeitado')


class Pet(BaseModel):
    id: ObjectId
    name: str = Field(..., example='Scooby')
    species: str = Field(..., example='Cachorro')
    race: str = Field(..., example='Dogue Alemao')
    age: int = Field(..., example=5)
    description: str = Field(
        ...,
        example='Possui pedigree e foi comprado do criador "Chacara dos Dogues Alemaes".',
    )


class ServiceList(BaseModel):
    data: Optional[List[Service]] = None


class RequestList(BaseModel):
    data: Optional[List[Request]] = None


class ServiceData(BaseModel):
    serviceType: str = Field(..., example='Tosa')
    price: float = Field(..., example=89.9)
    providerId: ObjectId


class RequestData(BaseModel):
    consumerId: ObjectId
    serviceId: ObjectId
    date: str = Field(..., example='1994-11-05T08:15:30-05:00')


class UserProviderData(BaseModel):
    cnpj: Cnpj
    name: str = Field(..., example='IPETS SERVICOS SA')
    email: EmailStr = Field(..., example='ariel.silva@ipets.com')
    password: Optional[SecretStr] = None
    address: Address
    bankAccount: BankAccount
    avatar: Optional[str] = Field(None, example='U3dhZ2dlciByb2Nrcw==')


class UserConsumerData(BaseModel):
    cpf: Cpf
    name: str = Field(..., example='Ariel Silva dos Santos')
    email: EmailStr = Field(..., example='ariel.silva@ipets.com')
    password: SecretStr
    address: Address
    creditCard: CreditCard
    avatar: Optional[str] = Field(None, example='U3dhZ2dlciByb2Nrcw==')
    pets: List[UUID]


class CreditCardData(BaseModel):
    code: str = Field(..., example='5118598797832798')
    name: str = Field(..., example='ARIEL S DOS SANTOS')
    expirationDate: str = Field(..., example='1994-11-05T08:15:30-05:00')
    verifyingDigits: str = Field(..., example='183')


class BankAccountData(BaseModel):
    agency: str = Field(..., example='60883')
    accountNumber: str = Field(..., example='3413')
    digit: Optional[str] = Field(None, example='1')


class AddressData(BaseModel):
    street: str = Field(..., example='Av. Paulista')
    number: str = Field(..., example='1001')
    complement: Optional[str] = Field(None, example='apto 21')
    city: str = Field(..., example='Sao Paulo')
    state: str = Field(..., example='SP')
    zip: str = Field(..., example='01311000')


class PetData(BaseModel):
    name: str = Field(..., example='Scooby')
    species: str = Field(..., example='Cachorro')
    race: Optional[str] = Field(None, example='Dogue Alemao')
    age: int = Field(..., example=5)
    description: Optional[str] = Field(
        None,
        example='Possui pedigree e foi comprado do criador "Chacara dos Dogues Alemaes".',
    )


class UserProvider(BaseModel):
    id: ObjectId
    cnpj: Optional[Cnpj] = None
    name: str = Field(..., example='IPETS SERVICOS SA')
    email: EmailStr = Field(..., example='ariel.silva@ipets.com')
    address: Address
    bankAccount: BankAccount
    avatar: Optional[str] = Field(None, example='U3dhZ2dlciByb2Nrcw==')


class UserConsumer(BaseModel):
    id: ObjectId
    cpf: Optional[Cpf] = None
    name: str = Field(..., example='Ariel Silva dos Santos')
    email: EmailStr = Field(..., example='ariel.silva@ipets.com')
    address: Address
    creditCard: CreditCard
    avatar: Optional[str] = Field(None, example='U3dhZ2dlciByb2Nrcw==')
    pets: List[UUID]
