from datetime import datetime
from bson import ObjectId
import numpy as np
from PIL import Image
import io
import base64
import secrets
import random

# from mongomock_motor import AsyncMongoMockClient
# from ..model.utils import get_database
# from ..main import app
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


def create_random_b64_image():
    image = Image.fromarray(
        np.random.randint(low=0, high=256, size=(100, 100, 3), dtype=np.uint8)
    ).convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, "JPEG")
    return base64.b64encode(buffer.getvalue()).decode()


def create_provider_dict():
    return {
        "cnpj": cnpj.generate(),
        "name": faker.name(),
        "email": faker.email(),
        "password": secrets.token_hex(),
        "avatar": create_random_b64_image(),
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


def create_consumer_dict():
    return {
        "cpf": cpf.generate(),
        "name": faker.name(),
        "email": faker.email(),
        "password": secrets.token_hex(),
        "avatar": create_random_b64_image(),
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
            }
            for _ in range(random.randint(1, 10))
        ],
    }


# async
def create_service_dict():
    name = random.choice(["Banho", "Tosa", "Banho e Tosa", "Hotel", "Creche"])
    # await populate_collection("providers", 1)
    # provider = await get_random_document_from_collection("providers")
    return {
        "name": name,
        "description": f"Oferecemos serviços de {name.lower()} para cachorros de pequeno e médio porte.",  # noqa: E501
        "price": round(random.uniform(1, 100), 1),
        "providerId": str(ObjectId()),  # provider["_id"]),
        "thumbnail": create_random_b64_image(),
    }


# async
def create_request_dict():
    # await populate_collection("consumers", 1)
    # consumer = await get_random_document_from_collection("consumers")

    # await populate_collection("services", 1)
    # services = await get_random_document_from_collection("services")

    return {
        "consumerId": str(ObjectId()),  # consumer["_id"]),
        "serviceId": str(ObjectId()),  # services["_id"]),
        "date": datetime.now().isoformat(),
        "status": random.choice(["Pendente", "Aceito", "Recusado"]),
    }


def create_dict(collection_name):
    generators = {
        "providers": create_provider_dict,
        "consumers": create_consumer_dict,
        "services": create_service_dict,
        "requests": create_request_dict,
    }
    assert collection_name in generators.keys()
    return generators[collection_name]()


def get_model_from_collection(collection_name):
    models = {
        "providers": ProviderModel,
        "consumers": ConsumerModel,
        "services": ServiceModel,
        "requests": RequestModel,
    }
    assert collection_name in models.keys()
    return models[collection_name]


def get_update_model_from_collection(collection_name):
    models = {
        "providers": UpdateProviderModel,
        "consumers": UpdateConsumerModel,
        "services": UpdateServiceModel,
        "requests": UpdateRequestModel,
    }
    assert collection_name in models.keys()
    return models[collection_name]


async def populate_collection(collection_name, amount):
    commons = await common_parameters()
    result = await commons["db"]["providers"].insert_many(
        [create_dict(collection_name) for _ in range(amount)]
    )
    return [str(inserted_id) for inserted_id in result.inserted_ids]


async def clear_collection(collection_name):
    commons = await common_parameters()
    await commons["db"][collection_name].drop()
    await commons["db"].create_collection(collection_name)


async def get_random_document_from_collection(collection_name):
    commons = await common_parameters()
    pipe = [{"$sample": {"size": 1}}]
    docs = await commons["db"][collection_name].aggregate(pipe).to_list(None)
    return docs[0]
