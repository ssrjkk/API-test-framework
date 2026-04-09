# API Testing Framework By ssrjkk

[![CI](https://github.com/ssrjkk/API-test-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/ssrjkk/API-test-framework/actions)
[![codecov](https://codecov.io/gh/ssrjkk/API-test-framework/branch/main/graph/badge.svg)](https://codecov.io/gh/ssrjkk/API-test-framework)

Мой фреймворк для тестирования API на Python. QA фреймворк: pytest + requests + Pydantic + retry логика + Docker + GitHub Actions CI/CD

## Тестируемые API

- [hh.ru](https://api.hh.ru) - поиск вакансий, регионы, справочники

> Архитектура системы тестирования, а не набор тестов.

## Стек технологий

| Компонент | Технология | Назначение |
|-----------|------------|------------|
| Тесты | pytest 8.1 | Оркестрация и маркировка тестов |
| HTTP | requests 2.31 | HTTP клиент с session pooling |
| Типизация | pydantic 2.5 | Валидация ответов и моделей данных |
| Retry | tenacity 8.2 | Retry логика при временных сбоях |
| Отчеты | allure-pytest 2.13 | HTML отчеты с деталями执行 |
| CI/CD | GitHub Actions | Автоматизация проверок |
| Контейнеры | Docker, K8s | Воспроизводимое окружение |

---

## Архитектура системы

```
┌──────────────────────────────────────────────────────────────────┐
│                         Тесты (tests/)                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │  Vacancies  │ │   Areas     │ │ Dictionaries│ │Integration  │ │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ │
└─────────┼───────────────┼───────────────┼───────────────┼────────┘
          │               │               │               │
          ▼               ▼               ▼               ▼
┌──────────────────────────────────────────────────────────────────┐
│                     API Layer (api/)                             │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ VacanciesApi  │  AreasApi  │  DictionariesApi  │ BaseApi    │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Тесты НЕ вызывают HTTP клиент напрямую                          │
│  Все обращения идут через API классы                             │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                   Core Layer (core/)                             │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              HTTPClient (requests.Session)                  │ │
│  │  - Connection pooling                                       │ │
│  │  - Automatic retry на 5xx (urllib3 Retry)                   │ │
│  │  - Configurable timeouts                                    │ │
│  │  - Request/response logging                                 │ │
│  └─────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                      Внешний API (hh.ru)                         │
└──────────────────────────────────────────────────────────────────┘

┌─────────────┐    ┌─────────────┐    ┌────────────────┐
│ Validators/ │    │   Models/   │    │  Fixtures/     │
│             │    │             │    │                │
│ - Response  │    │ - Vacancy   │    │ - http_client  │
│ - Schema    │    │ - Area      │    │ - vacancies_api│
│             │    │ - Dictionary│    │ - areas_api    │ 
└─────────────┘    └─────────────┘    └────────────────┘


### Слои абстракции

| Слой | Назначение | Изоляция |
|------|------------|----------|
| **Tests** | Описание тестовых сценариев | Не знает про HTTP |
| **API** | Инкапсуляция endpoint'ов | Знает только про модели |
| **Core** | Низкоуровневое взаимодействие | Умеет только HTTP |
| **Validators** | Проверка контрактов | Не знает про API |
| **Models** | Типизация данных | Чистые DTO |

### Принципы

1. **Тесты не знают про HTTP** - вызывают только API методы
2. **Endpoint'ы в одном месте** - `VacanciesApi.ENDPOINT = "/vacancies"`
3. **Валидация через DSL** - читаемый fluent интерфейс
4. **Retry на 5xx** - автоматический, прозрачный для тестов
5. **Конфиг через env vars** - никаких hardcoded значений

---

## Структура проекта

``
api-testing-framework/
├── core/                       # Базовые компоненты фреймворка
│   ├── http_client.py          # requests.Session + retry + logging
│   ├── config.py               # dataclass Config из env vars
│   └── retry.py                # tenacity декораторы
│
├── api/                        # API слой (абстракция над HTTP)
│   ├── base_api.py             # Базовый класс с get/post/put/delete
│   ├── vacancies_api.py        # /vacancies endpoints
│   ├── areas_api.py            # /areas endpoints
│   └── dictionaries_api.py     # /dictionaries endpoints
│
├── models/                     # Pydantic модели (DTO)
│   ├── vacancy.py              # Vacancy, VacancySearchResponse
│   ├── area.py                 # AreaModel
│   └── dictionary.py           # DictionariesResponse
│
├── validators/                  # Валидаторы ответов
│   ├── response_validator.py   # Fluent DSL .status().has_key().json_path()
│   └── schema_validator.py     # JSON Schema validation
│
├── tests/                      # Тестовые сценарии
│   ├── test_vacancies.py       # Поиск, детали, фильтры, производительность
│   ├── test_areas.py           # Список, поиск, ID
│   ├── test_dictionaries.py     # Справочники
│   ├── test_integration.py      # Кросс-API сценарии
│   └── test_smoke.py           # Быстрые smoke тесты
│
├── fixtures/                    # Pytest fixtures
│   ├── api_fixtures.py         # http_client, vacancies_api, areas_api
│   └── data_fixtures.py        # Загрузка test_data.json
│
├── data/                        # Тестовые данные
│   └── test_data.json          # IDs регионов, поисковые запросы
│
├── utils/                       # Утилиты
│   └── logger.py               # Настроенный логгер
│
├── docker/                      # Docker файлы
│   ├── Dockerfile              # Основной образ
│   ├── Dockerfile.test         # Образ с линтерами
│   ├── docker-compose.yml      # Локальный запуск
│   └── entrypoint.sh           # Точка входа
│
├── k8s/                        # Kubernetes манифесты
│   ├── configmap.yaml          # Конфигурация
│   ├── deployment.yaml          # Deployment
│   ├── service.yaml            # Service
│   └── secret.example.yaml     # Пример секретов
│
├── .github/workflows/          # CI/CD
│   └── ci.yml                 # Линт → Типы → Тесты → Coverage
│
├── conftest.py                # Глобальные fixtures
├── pytest.ini                 # Конфигурация pytest
├── pyproject.toml             # Зависимости и инструменты
├── requirements.txt           # Pip dependencies
└── .env.example               # Пример переменных окружения
```

---

## Локальный запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка окружения

```bash
cp .env.example .env
# Отредактируйте .env при необходимости
```

### 3. Запуск тестов

```bash
# Все тесты
pytest tests/ -v

# Только smoke
pytest tests/ -v -m smoke

# Только интеграционные
pytest tests/ -v -m integration

# Параллельное выполнение
pytest tests/ -v -n auto

# Конкретный файл
pytest tests/test_vacancies.py -v

# С покрытием
pytest tests/ --cov=api --cov=core --cov=models --cov-report=html
```

### 4. Проверка качества кода

```bash
# Ruff (линтер)
ruff check .

# Black (форматтер)
black --check .

# MyPy (типы)
mypy api core models validators
```

---

## Docker запуск

### Сборка образа

```bash
# Основной образ для тестов
docker build -f docker/Dockerfile -t api-tests .

# Образ с линтерами
docker build -f docker/Dockerfile.test -t api-tests-lint .
```

### Запуск через docker-compose

```bash
# Все сервисы
docker-compose -f docker/docker-compose.yml up

# Только тесты
docker-compose -f docker/docker-compose.yml up tests

# Только линтеры
docker-compose -f docker/docker-compose.yml up lint

# Параллельные тесты
docker-compose -f docker/docker-compose.yml up tests-parallel

# Просмотр логов
docker-compose -f docker/docker-compose.yml up --abort-on-container-exit
```

### Запуск тестов в контейнере

```bash
# Интерактивный режим
docker run --rm -it -e ENV=prod api-tests /bin/bash

# Директивный запуск
docker run --rm \
  -e ENV=prod \
  -e BASE_URL=https://api.hh.ru \
  api-tests \
  pytest tests/ -v

# С пробросом отчетов
docker run --rm \
  -v $(pwd)/reports:/app/reports \
  api-tests \
  pytest tests/ -v --alluredir=/app/reports
```

---

## Kubernetes запуск

### Подготовка

```bash
# Создайте namespace (опционально)
kubectl create namespace api-tests

# Отредактируйте секреты
cp k8s/secret.example.yaml k8s/secret.yaml
# Добавьте реальные значения в secret.yaml
```

### Применение манифестов

```bash
# Порядок применения важен!
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Или все сразу
kubectl apply -f k8s/
```

### Проверка статуса

```bash
# Статус pods
kubectl get pods -l app=api-tests

# Логи
kubectl logs -l app=api-tests -f

# Описание deployment
kubectl describe deployment api-tests
```

### Удаление

```bash
kubectl delete -f k8s/
```

### Конфигурация через K8s

Все настройки вынесены в ConfigMap и Secret:

```yaml
# configmap.yaml
data:
  ENV: "prod"
  BASE_URL: "https://api.hh.ru"
  TIMEOUT: "10"
  MAX_RETRIES: "3"
  LOG_LEVEL: "INFO"
```

Тесты читают из переменных окружения - никаких hardcoded значений.

---

## CI/CD пайплайн

### GitHub Actions Workflow

```yaml
on: [push, pull_request]
  └── jobs:
      ├── lint           # ruff, black
      ├── typecheck      # mypy
      ├── test (3.11)    # pytest
      ├── test (3.12)    # pytest
      ├── test-smoke     # pytest -m smoke
      └── coverage       # pytest --cov
```

### Запуск локально (act)

```bash
# Установка act
# brew install act

# Запуск workflow
act -W .github/workflows/ci.yml
```

### Этапы CI

| Этап | Инструмент | Что проверяет |
|------|------------|---------------|
| **Lint** | ruff | PEP8, imports, naming |
| **Format** | black | Code formatting |
| **Types** | mypy | Type hints correctness |
| **Test 3.11** | pytest | Все тесты на Python 3.11 |
| **Test 3.12** | pytest | Все тесты на Python 3.12 |
| **Smoke** | pytest -m smoke | Быстрые критические тесты |
| **Coverage** | pytest-cov | Покрытие кода |

### Артефакты

После каждого запуска сохраняются:
- `report.xml` - JUnit XML для интеграции с CI
- `.pytest_cache` - кэш для анализа падений
- `coverage.xml` - покрытие для SonarQube/Codecov

---

## API слой (пример)

### Тест не знает про HTTP

```python
# Плохо - тест знает про endpoint
def test_search(client):
    response = client.get("/vacancies", params={"text": "QA"})
    assert response.status_code == 200

# Хорошо - тест работает с абстракцией
def test_search(vacancies_api):
    response = vacancies_api.search(text="QA")
    assert response.status_code == 200
```

### VacanciesApi

```python
class VacanciesApi(BaseApi):
    ENDPOINT = "/vacancies"

    def search(self, text, area=None, per_page=10, ...):
        params = {"per_page": per_page, ...}
        if text:
            params["text"] = text
        return self.get(self.ENDPOINT, params=params)

    def get_by_id(self, vacancy_id):
        return self.get(f"{self.ENDPOINT}/{vacancy_id}")
```

---

## Валидация ответов

### Fluent DSL

```python
ResponseValidator(response) \
    .status(200) \
    .has_keys(["id", "name", "employer"]) \
    .json_path("items", lambda x: len(x) > 0) \
    .json_path("found", lambda x: x >= 0) \
    .response_time_under(3000) \
    .raise_if_errors()
```

### Модели

```python
# Парсинг в Pydantic модель
vacancy = ResponseValidator(response).model(Vacancy)

# Типизированные поля
assert isinstance(vacancy.id, str)
assert isinstance(vacancy.name, str)
```

---

## Тестируемые сценарии

### Vacancies API
- Поиск вакансий с параметрами
- Получение деталей по ID
- Фильтры: опыт, занятость, регион, зарплата
- Пагинация (per_page, page)
- Обработка 404 для несуществующих ID
- Производительность (<3s)

### Areas API
- Список всех регионов
- Поиск конкретных (Россия, СПб)
- Получение по ID
- Вложенная структура (страна -> город)

### Dictionaries API
- Справочники: опыт, занятость, график
- Структура значений (id, name)
- Применение ID из справочников в фильтрах

### Интеграция
- Search -> Detail (согласованность данных)
- Areas -> Vacancies (использование ID из справочников)
- Dictionaries -> Filters (комбинированные фильтры)

---

## Конфигурация

### Переменные окружения

| Переменная | По умолчанию | Описание |
|------------|--------------|---------|
| `ENV` | prod | Окружение |
| `BASE_URL` | https://api.hh.ru | Базовый URL API |
| `TIMEOUT` | 10 | Таймаут запроса (сек) |
| `MAX_RETRIES` | 3 | Число повторных попыток |
| `RETRY_DELAY` | 1.0 | Задержка между retry (сек) |
| `LOG_LEVEL` | INFO | Уровень логирования |

### pytest.ini

```ini
[pytest]
testpaths = tests
markers =
    api: API тесты
    integration: Интеграционные тесты
    smoke: Быстрые smoke тесты
    slow: Медленные тесты
```

---

## Быстрые ссылки

| Задача | Команда |
|--------|---------|
| Установить | `pip install -r requirements.txt` |
| Тесты | `pytest tests/ -v` |
| Smoke | `pytest tests/ -v -m smoke` |
| Docker тесты | `docker-compose -f docker/docker-compose.yml up tests` |
| Линт | `ruff check . && black --check .` |
| Типы | `mypy api core models validators` |
| K8s apply | `kubectl apply -f k8s/` |


## Contacts
- Telegram: @ssrjkk
- Email: ray013lefe@gmail.com
- GitHub: https://github.com/ssrjkk
