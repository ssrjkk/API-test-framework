import pytest
from typing import Generator, cast

from core.http_client import HTTPClient
from api.vacancies_api import VacanciesApi
from api.areas_api import AreasApi
from api.dictionaries_api import DictionariesApi
from fixtures.data_fixtures import TEST_DATA


@pytest.fixture(scope="session")
def http_client() -> Generator[HTTPClient, None, None]:
    client = HTTPClient()
    yield client
    client.close()


@pytest.fixture(scope="session")
def vacancies_api(http_client: HTTPClient) -> VacanciesApi:
    return VacanciesApi(http_client)


@pytest.fixture(scope="session")
def areas_api(http_client: HTTPClient) -> AreasApi:
    return AreasApi(http_client)


@pytest.fixture(scope="session")
def dictionaries_api(http_client: HTTPClient) -> DictionariesApi:
    return DictionariesApi(http_client)


@pytest.fixture(scope="session")
def test_data() -> dict:
    return TEST_DATA


@pytest.fixture
def valid_search_queries() -> list[str]:
    return cast(list[str], TEST_DATA["search_queries"]["valid"])


@pytest.fixture
def known_areas() -> dict[str, str]:
    return cast(dict[str, str], TEST_DATA["areas"])
