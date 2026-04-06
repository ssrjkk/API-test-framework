"""
Тесты с моками для демонстрации навыков мокирования.

Эти тесты используют unittest.mock для изоляции от реального API.
"""

from unittest.mock import MagicMock, patch

import pytest
from requests import Response

from api.vacancies_api import VacanciesApi
from core.http_client import HTTPClient


class TestVacanciesMocked:
    """Тесты с использованием моков"""

    @pytest.fixture
    def mock_response(self) -> MagicMock:
        response = MagicMock(spec=Response)
        response.status_code = 200
        response.json.return_value = {
            "items": [
                {
                    "id": "12345",
                    "name": "QA Engineer",
                    "salary": {"from": 100000, "to": 150000},
                    "area": {"id": "1", "name": "Москва"},
                    "employer": {"id": "1", "name": "Компания"},
                }
            ],
            "found": 1,
            "pages": 1,
        }
        return response

    def test_search_returns_mocked_data(self, mock_response: MagicMock) -> None:
        """Тест: проверка что API возвращает данные из мока"""
        mock_client = MagicMock(spec=HTTPClient)
        mock_client.get.return_value = mock_response

        api = VacanciesApi(mock_client)
        result = api.search(text="QA")

        assert result.status_code == 200
        data = result.json()
        assert data["found"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "QA Engineer"

    def test_search_handles_500_error(self) -> None:
        """Тест: проверка обработки 500 ошибки"""
        error_response = MagicMock(spec=Response)
        error_response.status_code = 500
        error_response.text = "Internal Server Error"

        mock_client = MagicMock(spec=HTTPClient)
        mock_client.get.return_value = error_response

        api = VacanciesApi(mock_client)
        result = api.search(text="test")

        assert result.status_code == 500

    def test_search_handles_timeout(self) -> None:
        """Тест: проверка обработки таймаута"""
        import requests

        mock_client = MagicMock(spec=HTTPClient)
        mock_client.get.side_effect = requests.exceptions.Timeout()

        api = VacanciesApi(mock_client)

        with pytest.raises(requests.exceptions.Timeout):
            api.search(text="test")

    def test_vacancy_detail_with_mock(self) -> None:
        """Тест: получение деталей вакансии через мок"""
        detail_response = MagicMock(spec=Response)
        detail_response.status_code = 200
        detail_response.json.return_value = {
            "id": "99999",
            "name": "Senior Python Developer",
            "description": "Описание вакансии",
            "salary": {"from": 200000, "to": 300000, "currency": "RUR"},
        }

        mock_client = MagicMock(spec=HTTPClient)
        mock_client.get.return_value = detail_response

        api = VacanciesApi(mock_client)
        result = api.get_by_id("99999")

        assert result.status_code == 200
        data = result.json()
        assert data["id"] == "99999"
        assert "salary" in data

    def test_search_with_filters(self) -> None:
        """Тест: проверка передачи фильтров"""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [], "found": 0, "pages": 0}

        mock_client = MagicMock(spec=HTTPClient)
        mock_client.get.return_value = mock_response

        api = VacanciesApi(mock_client)
        api.search(text="Python", area="1", per_page=20)

        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[0][0] == "/vacancies"
        assert call_args[1]["params"]["text"] == "Python"
        assert call_args[1]["params"]["area"] == "1"
        assert call_args[1]["params"]["per_page"] == 20
