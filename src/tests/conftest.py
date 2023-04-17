# from mongomock_motor import AsyncMongoMockClient
# from ..model.utils import get_database
from ..main import app
from fastapi.testclient import TestClient
import pytest


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


# @pytest.fixture(scope="function")
# def valid_request_body_provider():
#     return create_provider_dict()

# @pytest.fixture(autouse=True)
# def mock_env_vars(monkeypatch):
#     monkeypatch.setenv(
#         'MONGODB_URL',
#         'mongodb+srv://user:hash@cluster.hash.mongodb.net/user?retryWrites=true&w=majority'
#     )


# def mock_get_database():
#     client = AsyncMongoMockClient()
#     return client['ipetsPlatform']


# def mock_common_parameters():
#     return {"db": mock_get_database()}


# @pytest_asyncio.fixture(autouse=True)
# async def override_common_parameters():
#     app.dependency_overrides[common_parameters] = mock_common_parameters


# @pytest.fixture(autouse=True)
# def set_environment_variables(monkeypatch):
#     monkeypatch.setenv('MONGODB_URL', 'MONGODB_URL')
#     # pass


# @pytest.fixture(autouse=True)
# def mock_asyncio_motor_client(monkeypatch):
#     monkeypatch.setattr(
#         'motor.motor_asyncio.AsyncIOMotorClient',
#         lambda: AsyncMongoMockClient()
#     )


# @pytest_asyncio.fixture(scope="function")
# # @patch(servers=(('server.example.com', 27017)))
# async def valid_id_provider():
#     commons = await common_parameters()
#     object = await commons['db']['providers'].insert_one(
#         create_provider_dict()
#     )
#     return object.inserted_id
