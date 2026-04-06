"""
Тесты с HTTP моками для демонстрации навыков мокирования.

Использует библиотеку responses - более профессионально для API фреймворка.
"""

import allure
import responses
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import pytest
from api.vacancies_api import VacanciesApi
from core.http_client import HTTPClient


@pytest.fixture
def http_client_mock() -> HTTPClient:
    """HTTPClient без retry для тестов с моками"""
    client = HTTPClient(
        base_url="https://api.hh.ru",
        timeout=30,
        skip_throttle=True,
    )
    client.session.mount("https://", HTTPAdapter(max_retries=Retry(total=0)))
    return client


@responses.activate
def test_search_returns_empty_list(http_client_mock: HTTPClient) -> None:
    """Тест: API возвращает пустой список when нет результатов"""
    responses.add(
        responses.GET,
        "https://api.hh.ru/vacancies",
        json={"items": [], "found": 0, "pages": 0},
        status=200,
    )

    api = VacanciesApi(http_client_mock)
    with allure.step("Отправляем запрос поиска с несуществующим текстом"):
        response = api.search(text="xyznonexistent123")

    with allure.step("Проверяем статус ответа"):
        assert response.status_code == 200

    data = response.json()
    assert data["found"] == 0
    assert len(data["items"]) == 0


@responses.activate
def test_search_returns_vacancies(http_client_mock: HTTPClient) -> None:
    """Тест: поиск возвращает вакансии с правильной структурой"""
    responses.add(
        responses.GET,
        "https://api.hh.ru/vacancies",
        json={
            "items": [
                {
                    "id": "12345",
                    "name": "QA Engineer",
                    "salary": {"from": 100000, "to": 150000},
                    "area": {"id": "1", "name": "Москва"},
                }
            ],
            "found": 1,
            "pages": 1,
        },
        status=200,
    )

    api = VacanciesApi(http_client_mock)
    response = api.search(text="QA", area="1", per_page=10)

    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "QA Engineer"


@responses.activate
def test_server_error_500(http_client_mock: HTTPClient) -> None:
    """Тест: корректная обработка 500 ошибки сервера"""
    responses.add(
        responses.GET,
        "https://api.hh.ru/vacancies",
        json={"error": "Internal Server Error"},
        status=500,
    )

    api = VacanciesApi(http_client_mock)
    response = api.search(text="test")

    assert response.status_code == 500


@responses.activate
def test_rate_limited_429(http_client_mock: HTTPClient) -> None:
    """Тест: корректная обработка 429 Too Many Requests"""
    responses.add(
        responses.GET,
        "https://api.hh.ru/vacancies",
        json={"error": "Too Many Requests"},
        status=429,
    )

    api = VacanciesApi(http_client_mock)
    response = api.search(text="test")

    assert response.status_code == 429


@responses.activate
def test_vacancy_detail_not_found(http_client_mock: HTTPClient) -> None:
    """Тест: 404 при получении несуществующей вакансии"""
    responses.add(
        responses.GET,
        "https://api.hh.ru/vacancies/999999999",
        json={"error": "Vacancy not found"},
        status=404,
    )

    api = VacanciesApi(http_client_mock)
    response = api.get_by_id("999999999")

    assert response.status_code == 404


@responses.activate
def test_search_with_filters(http_client_mock: HTTPClient) -> None:
    """Тест: проверка что фильтры правильно передаются в URL"""
    responses.add(
        responses.GET,
        "https://api.hh.ru/vacancies",
        json={"items": [], "found": 0, "pages": 0},
        status=200,
    )

    api = VacanciesApi(http_client_mock)
    api.search(text="Python", area="1", per_page=20, experience="between1And3")

    request = responses.calls[0].request
    assert "text=Python" in request.url
    assert "area=1" in request.url
    assert "per_page=20" in request.url
    assert "experience=between1And3" in request.url
