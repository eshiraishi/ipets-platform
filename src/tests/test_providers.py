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


@pytest.mark.parametrize(
    "collection",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
def test_GIVEN_valid_document_request_body_WHEN_post_document_THEN_equivalent_document(  # noqa: E501
    client, collection
):
    request_body = create_dict(collection)
    response = client.post(url=f"/{collection}", json=request_body)
    response_body = json_util.loads(response.json())

    get_model_from_collection(collection).parse_obj(response_body)
    del response_body["_id"]
    assert response.status_code == 201
    assert response_body == request_body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_populated_documents_collection_WHEN_get_all_documents_THEN_equivalent_list(  # noqa: E501
    client, collection
):
    await clear_collection(collection)
    await populate_collection(collection, 2)
    response = client.get(url=f"/{collection}")
    body = response.json()

    assert response.status_code == 200
    assert all(
        [get_model_from_collection(collection).parse_obj(obj) for obj in body]
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_empty_documents_collection_WHEN_get_all_documents_THEN_equivalent_list(  # noqa: E501
    client, collection
):
    await clear_collection(collection)
    response = client.get(url=f"/{collection}")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_valid_id_WHEN_get_single_document_THEN_equivalent_document(  # noqa: E501
    client,
    collection,
):
    document_ids = await populate_collection(collection, 1)
    response = client.get(url=f"/{collection}/{document_ids[0]}")
    body = response.json()

    assert response.status_code == 200

    get_model_from_collection(collection).parse_obj(body)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_invalid_id_WHEN_get_single_document_THEN_422(  # noqa: E501
    client, collection
):
    response = client.get(url=f"/{collection}/{secrets.token_urlsafe()}")
    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_unknown_id_WHEN_get_single_document_THEN_404(  # noqa: E501
    client, collection
):
    response = client.get(url=f"/{collection}/{ObjectId()}")
    assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_valid_id_and_fully_updated_document_request_body_WHEN_put_document_THEN_equivalent_document(  # noqa: E501
    client, collection
):
    document_ids = await populate_collection(collection, 1)
    request_body = create_dict(collection)
    response = client.put(
        url=f"/{collection}/{document_ids[0]}", json=request_body
    )
    response_body = response.json()

    assert response.status_code == 200
    assert str(document_ids[0]) == response_body["_id"]

    get_model_from_collection(collection).parse_obj(response_body)
    del response_body["_id"]

    assert request_body == response_body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_valid_id_and_partially_updated_document_request_body_WHEN_put_document_THEN_equivalent_document(  # noqa: E501
    client, collection
):
    update_model = get_update_model_from_collection(collection)
    for kept_attr in update_model.__fields__.keys():
        document_ids = await populate_collection(collection, 1)
        request_body = {
            k: v for k, v in create_dict(collection).items() if k != kept_attr
        }
        response = client.put(
            url=f"/{collection}/{document_ids[0]}", json=request_body
        )
        response_body = response.json()

        assert response.status_code == 200
        assert str(document_ids[0]) == response_body["_id"]

        get_model_from_collection(collection).parse_obj(response_body)
        del response_body["_id"]

        document = await get_document_by_id(collection, document_ids[0])
        assert document[kept_attr] == response_body[kept_attr]
        assert request_body == {
            k: v for k, v in response_body.items() if k != kept_attr
        }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_invalid_id_and_fully_updated_document_request_body_WHEN_put_document_THEN_422(  # noqa: E501
    client, collection
):
    response = client.put(
        url=f"/{collection}/{secrets.token_urlsafe()}",
        json=create_dict(collection),
    )

    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_unknown_id_and_fully_updated_document_request_body_WHEN_put_document_THEN_404(  # noqa: E501
    client, collection
):
    response = client.put(
        url=f"/{collection}/{ObjectId()}", json=create_dict(collection)
    )

    assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_valid_id_WHEN_delete_document_THEN_204(
    client, collection
):
    document_ids = await populate_collection(collection, 1)
    response = client.delete(url=f"/{collection}/{document_ids[0]}")

    assert response.status_code == 204

    commons = await common_parameters()
    deleted_document = await commons["db"][collection].find_one(
        {"_id": document_ids[0]}
    )
    assert deleted_document is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_invalid_id_WHEN_delete_document_THEN_422(  # noqa: E501
    client, collection
):
    response = client.delete(url=f"/{collection}/{secrets.token_urlsafe()}")

    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "collection",
    [
        "providers",
        "consumers",
        "services",
        "requests",
    ],
)
async def test_GIVEN_unknown_id_WHEN_delete_document_THEN_404(  # noqa: E501
    client, collection
):
    response = client.delete(url=f"/{collection}/{ObjectId()}")

    assert response.status_code == 404
