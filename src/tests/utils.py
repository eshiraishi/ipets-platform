from datetime import datetime
from bson import ObjectId
import numpy as np
from PIL import Image
import io
import base64
import secrets
import random
from logging import getLogger

from validate_docbr import CNPJ, CPF
from faker import Faker
from ..controller.utils import common_parameters
from ..model.provider import ProviderModel, UpdateProviderModel
from ..model.consumer import ConsumerModel, UpdateConsumerModel
from ..model.service import ServiceModel, UpdateServiceModel
from ..model.request import RequestModel, UpdateRequestModel

cnpj = CNPJ()
cpf = CPF()
faker = Faker(locale="pt-BR")
logger = getLogger()
logger.setLevel("DEBUG")


def create_random_b64_image() -> str:
    image = Image.fromarray(
        np.random.randint(low=0, high=256, size=(100, 100, 3), dtype=np.uint8)
    ).convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, "JPEG")
    return base64.b64encode(buffer.getvalue()).decode()


def create_provider_dict() -> dict:
    return {
        "cnpj": cnpj.generate(),
        "name": faker.company(),
        "email": faker.email(),
        "password": secrets.token_hex(),
        "avatar": create_random_b64_image(),
        "phone": faker.phone_number(),
        "address": {
            "street": f"{faker.street_prefix()} {faker.street_name()}",
            "number": str(random.randint(1, 10**3) - 1),
            "complement": faker.street_suffix(),
            "city": faker.city(),
            "state": faker.estado_sigla(),
            "postcode": faker.postcode(),
        },
        "bankAccount": {
            "agency": f"{random.randint(0, 10**4)-1:04}",
            "accountNumber": f"{random.randint(0, 10**4)-1:011}",
            "digit": f"{random.randint(0, 10**1)-1}",
        },
    }


def create_consumer_dict() -> dict:
    return {
        "cpf": cpf.generate(),
        "name": faker.name(),
        "email": faker.email(),
        "password": secrets.token_hex(),
        "avatar": create_random_b64_image(),
        "phone": faker.phone_number(),
        "birthDate": faker.past_date().isoformat(),
        "address": {
            "street": f"{faker.street_prefix()} {faker.street_name()}",
            "number": str(random.randint(1, 10**3) - 1),
            "complement": faker.street_suffix(),
            "city": faker.city(),
            "state": faker.estado_sigla(),
            "postcode": faker.postcode(),
        },
        "creditCard": {
            "code": f"{random.randint(0, 10**16)-1:016}",
            "name": faker.name().upper(),
            "expirationDate": f"{faker.past_date().month:02}/{faker.past_date().year}",  # noqa: E501
            "cvv": f"{random.randint(0, 10**4)-1:03}",
        },
        "pets": [
            {
                "name": faker.first_name(),
                "species": random.choice(
                    ["Cachorro", "Cusco", "Guaipeca", "Cão"]
                ),
                "race": random.choice(["SRD", "Vira-lata", "Desconhecido"]),
                "age": random.randint(0, 18),
                "description": random.choice(
                    [
                        "Teve displasia",
                        "Foi o nanico da ninhada",
                        "Animal muito dócil",
                        "Não possui pedrigree",
                    ]
                ),
                "avatar": create_random_b64_image(),
            }
            for _ in range(random.randint(1, 10))
        ],
    }


def create_service_dict() -> dict:
    name = random.choice(["Banho", "Tosa", "Banho e Tosa", "Hotel", "Creche"])
    return {
        "name": name,
        "description": f"Oferecemos serviços de {name.lower()} para cachorros de pequeno e médio porte.",  # noqa: E501
        "price": round(random.uniform(1, 100), 1),
        "providerId": str(ObjectId()),
        "thumbnail": create_random_b64_image(),
    }


def create_request_dict() -> dict:
    return {
        "consumerId": str(ObjectId()),
        "serviceId": str(ObjectId()),
        "date": datetime.now().isoformat(),
        "status": random.choice(["Pendente", "Aceito", "Recusado"]),
    }


def create_dict(collection_name: str) -> dict:
    generators = {
        "providers": create_provider_dict,
        "consumers": create_consumer_dict,
        "services": create_service_dict,
        "requests": create_request_dict,
    }
    assert collection_name in generators.keys()
    return generators[collection_name]()


def get_model_from_collection(
    collection_name: str,
) -> ProviderModel | ConsumerModel | ServiceModel | RequestModel:
    models = {
        "providers": ProviderModel,
        "consumers": ConsumerModel,
        "services": ServiceModel,
        "requests": RequestModel,
    }
    assert collection_name in models.keys()
    return models[collection_name]


def get_update_model_from_collection(
    collection_name: str,
) -> (
    UpdateProviderModel
    | UpdateConsumerModel
    | UpdateServiceModel
    | UpdateRequestModel
):
    models = {
        "providers": UpdateProviderModel,
        "consumers": UpdateConsumerModel,
        "services": UpdateServiceModel,
        "requests": UpdateRequestModel,
    }
    assert collection_name in models.keys()
    return models[collection_name]


async def populate_collection(collection_name: str, amount: int) -> list:
    commons = await common_parameters()
    assert amount >= 1
    if amount == 1:
        result = await commons["db"][collection_name].insert_one(
            create_dict(collection_name)
        )
        return [result.inserted_id]
    else:
        result = await commons["db"][collection_name].insert_many(
            [create_dict(collection_name) for _ in range(amount)]
        )
        return [str(inserted_id) for inserted_id in result.inserted_ids]


async def clear_collection(collection_name: str) -> None:
    commons = await common_parameters()
    await commons["db"][collection_name].drop()
    await commons["db"].create_collection(collection_name)


async def get_random_document_from_collection(collection_name: str) -> dict:
    commons = await common_parameters()
    pipe = [{"$sample": {"size": 1}}]
    docs = await commons["db"][collection_name].aggregate(pipe).to_list(None)
    return docs[0]


async def get_document_by_id(collection_name: str, document_id: str) -> dict:
    commons = await common_parameters()
    document = await commons["db"][collection_name].find_one(
        {"_id": document_id}
    )
    return document
