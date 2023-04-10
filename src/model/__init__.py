REGEX_OBJECT_ID: str = r"^[a-fA-F\d]{24}$"
REGEX_CNPJ: str = r"\d{14}"
REGEX_CPF: str = r"\d{11}"

TEMPLATE_404: str = "Documento inexistente para o id %s"


""" class UpdateRequestModel(BaseModel):
    consumerId: Optional[PyObjectId]
    serviceId: Optional[PyObjectId]
    date: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ConsumerModel(BaseModel):
    id: PyObjectId
    cpf: constr(regex=REGEX_CPF)
    name: str
    email: EmailStr
    address: Address
    creditCard: CreditCard
    avatar: Optional[str]
    pets: list[Pet]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ServiceModel(BaseModel):
    id: PyObjectId
    name: str
    description: Optional[str]
    price: float
    providerId: PyObjectId

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class RequestModel(BaseModel):
    id: PyObjectId
    consumerId: PyObjectId
    serviceId: PyObjectId
    date: str
    status: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ServiceListModel(BaseModel):
    data: list[ServiceModel]


class RequestListModel(BaseModel):
    data: list[RequestModel]


class Address(BaseModel):
    street: Optional[str]
    number: Optional[str]
    complement: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class BankAccount(BaseModel):
    agency: Optional[str]
    accountNumber: Optional[str]
    digit: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CreditCard(BaseModel):
    code: Optional[str]
    name: Optional[str]
    expirationDate: Optional[str]
    verifyingDigits: Optional[str]

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

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateConsumerModel(BaseModel):
    cpf: Optional[constr(regex=REGEX_CPF)]
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[SecretStr]
    address: Optional[Address]
    creditCard: Optional[CreditCard]
    avatar: Optional[str]
    pets: Optional[list[Pet]]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateServiceModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    providerId: Optional[PyObjectId]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
 """