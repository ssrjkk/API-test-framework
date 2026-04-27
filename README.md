# HH API Testing Framework

Профессиональный фреймворк для автоматизированного тестирования API hh.ru.

## Возможности

- 30+ готовых тестов (mock, contract, security)
- Валидация ответов через Pydantic v2 и JSON Schema
- Автоматический retry на сбои (5xx ошибки)
- Красивые HTML отчеты (Allure)
- Работа в Docker и Kubernetes
- Настроенный CI/CD (GitHub Actions)
- Покрытие кода (Codecov)

## Быстрый старт

```bash
git clone https://github.com/ssrjkk/hh-api-framework.git
cd hh-api-framework
pip install -r requirements.txt
pytest tests/ -v
```

## Пример использования

```python
from api.vacancies_api import VacanciesApi
from core.http_client import HTTPClient

client = HTTPClient(base_url="https://api.hh.ru")
api = VacanciesApi(client)

response = api.search(text="Python", per_page=10)
print(response.json())
```

## Структура тестов

| Тип | Количество | Назначение |
|-----|-----------|------------|
| Mock-тесты | 20 | Быстрая проверка логики без реального API |
| Contract тесты | 4 | Проверка соответствия ответов схеме |
| Security тесты | 7 | Маскировка данных, проверка HTTPS |

## Запуск тестов

```bash
# Все тесты
pytest tests/ -v

# Только mock-тесты (быстро)
pytest tests/test_mocks.py -v

# С Allure отчетом
pytest tests/ --alluredir=allure-results
allure serve allure-results

# В Docker
docker build -f docker/Dockerfile -t hh-tests .
docker run --rm hh-tests pytest tests/ -v
```

## CI/CD

Проект использует GitHub Actions:
- Автоматический запуск тестов при каждом коммите
- Генерация Allure отчетов
- Публикация покрытия кода в Codecov
- Проверка кода: ruff, black, mypy

Посмотреть статус: https://github.com/ssrjkk/hh-api-framework/actions

## Технологии

- Python 3.11+
- pytest 8.1+ (оркестрация тестов)
- requests 2.31+ (HTTP клиент)
- Pydantic 2.5+ (валидация данных)
- Allure (отчеты)
- Docker / Kubernetes (контейнеризация)

## Конфигурация

Настройка через .env файл или переменные окружения:

```
BASE_URL=https://api.hh.ru
TIMEOUT=10
MAX_RETRIES=3
LOG_LEVEL=INFO
```

## Разработка

```bash
# Установка dev-зависимостей
pip install -r requirements-dev.txt

# Проверка качества кода
ruff check .
black --check .
mypy api core models
```

## Автор

ssrjkk
- Telegram: @ssrjkk
- Email: ray013lefe@gmail.com
- GitHub: https://github.com/ssrjkk

## Лицензия

MIT License - свободное использование.
