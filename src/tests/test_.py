import secrets
from bson import ObjectId, json_util
from ..controller.utils import common_parameters
from .utils import (
    clear_collection,
    populate_collection,
    create_dict,
    get_model_from_collection,
    get_update_model_from_collection,
    get_document_by_id,
)
import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "collection_name",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
def test_GIVEN_valid_document_request_body_WHEN_post_document_THEN_equivalent_document(  # noqa: E501
    client: TestClient, collection_name: str
):
    request_body = create_dict(collection_name)
    response = client.post(url=f"/{collection_name}", json=request_body)
    response_body = json_util.loads(response.json())

    get_model_from_collection(collection_name).parse_obj(response_body)
    del response_body["_id"]
    assert response.status_code == 201
    assert response_body == request_body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection_name",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_populated_documents_collection_WHEN_get_all_documents_THEN_equivalent_list(  # noqa: E501
    client: TestClient, collection_name: str
):
    await clear_collection(collection_name)
    await populate_collection(collection_name, 2)
    response = client.get(url=f"/{collection_name}")
    body = response.json()

    assert response.status_code == 200
    assert all(
        [
            get_model_from_collection(collection_name).parse_obj(obj)
            for obj in body
        ]
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection_name",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_empty_documents_collection_WHEN_get_all_documents_THEN_equivalent_list(  # noqa: E501
    client: TestClient, collection_name: str
):
    await clear_collection(collection_name)
    response = client.get(url=f"/{collection_name}")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection_name",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_valid_id_WHEN_get_single_document_THEN_equivalent_document(  # noqa: E501
    client: TestClient,
    collection_name,
):
    document_id, *_ = await populate_collection(collection_name, 1)
    response = client.get(url=f"/{collection_name}/{document_id}")
    body = response.json()

    assert response.status_code == 200

    get_model_from_collection(collection_name).parse_obj(body)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection_name",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_invalid_id_WHEN_get_single_document_THEN_422(  # noqa: E501
    client: TestClient, collection_name: str
):
    response = client.get(url=f"/{collection_name}/{secrets.token_urlsafe()}")
    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection_name",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_unknown_id_WHEN_get_single_document_THEN_404(  # noqa: E501
    client: TestClient, collection_name: str
):
    response = client.get(url=f"/{collection_name}/{ObjectId()}")
    assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection_name",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_valid_id_and_fully_updated_document_request_body_WHEN_put_document_THEN_equivalent_document(  # noqa: E501
    client: TestClient, collection_name: str
):
    document_id, *_ = await populate_collection(collection_name, 1)
    request_body = create_dict(collection_name)
    response = client.put(
        url=f"/{collection_name}/{document_id}", json=request_body
    )
    response_body = response.json()

    assert response.status_code == 200
    assert str(document_id) == response_body["_id"]

    get_model_from_collection(collection_name).parse_obj(response_body)
    del response_body["_id"]

    assert request_body == response_body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection_name",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_valid_id_and_partially_updated_document_request_body_WHEN_put_document_THEN_equivalent_document(  # noqa: E501
    client: TestClient, collection_name: str
):
    update_model = get_update_model_from_collection(collection_name)
    for kept_attr in update_model.__fields__.keys():
        document_id, *_ = await populate_collection(collection_name, 1)
        request_body = {
            k: v
            for k, v in create_dict(collection_name).items()
            if k != kept_attr
        }
        response = client.put(
            url=f"/{collection_name}/{document_id}", json=request_body
        )
        response_body = response.json()

        assert response.status_code == 200
        assert str(document_id) == response_body["_id"]

        get_model_from_collection(collection_name).parse_obj(response_body)
        del response_body["_id"]

        document = await get_document_by_id(collection_name, document_id)
        assert document[kept_attr] == response_body[kept_attr]
        assert request_body == {
            k: v for k, v in response_body.items() if k != kept_attr
        }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection_name",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_invalid_id_and_fully_updated_document_request_body_WHEN_put_document_THEN_422(  # noqa: E501
    client: TestClient, collection_name: str
):
    response = client.put(
        url=f"/{collection_name}/{secrets.token_urlsafe()}",
        json=create_dict(collection_name),
    )

    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection_name",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_unknown_id_and_fully_updated_document_request_body_WHEN_put_document_THEN_404(  # noqa: E501
    client: TestClient, collection_name: str
):
    response = client.put(
        url=f"/{collection_name}/{ObjectId()}",
        json=create_dict(collection_name),
    )

    assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection_name",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_valid_id_WHEN_delete_document_THEN_204(
    client: TestClient, collection_name: str
):
    document_id, *_ = await populate_collection(collection_name, 1)
    response = client.delete(url=f"/{collection_name}/{document_id}")

    assert response.status_code == 204

    commons = await common_parameters()
    deleted_document = await commons["db"][collection_name].find_one(
        {"_id": document_id}
    )
    assert deleted_document is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection_name",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_invalid_id_WHEN_delete_document_THEN_422(  # noqa: E501
    client: TestClient, collection_name: str
):
    response = client.delete(
        url=f"/{collection_name}/{secrets.token_urlsafe()}"
    )

    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection_name",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_unknown_id_WHEN_delete_document_THEN_404(  # noqa: E501
    client: TestClient, collection_name: str
):
    response = client.delete(url=f"/{collection_name}/{ObjectId()}")

    assert response.status_code == 404
