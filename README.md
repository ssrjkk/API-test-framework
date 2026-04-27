# 🚀 HH API Testing Framework

> **Production-ready API testing framework for hh.ru**  
> Python + pytest + Pydantic + Allure + Docker/K8s + GitHub Actions CI

[![CI Status](https://github.com/ssrjkk/hh-api-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/ssrjkk/hh-api-framework/actions)
[![Codecov](https://codecov.io/gh/ssrjkk/hh-api-framework/branch/main/graph/badge.svg)](https://codecov.io/gh/ssrjkk/hh-api-framework)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![pytest](https://img.shields.io/badge/pytest-8.1+-blueviolet.svg)](https://pytest.org/)
[![Pydantic](https://img.shields.io/badge/pydantic-2.5+-green.svg)](https://pydantic-docs.helpmanual.io/)

---

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| **Total Tests** | 20+ (mocked) |
| **Test Coverage** | 85%+ |
| **CI/CD** | GitHub Actions |
| **Reporting** | Allure + Codecov |
| **Docker Ready** | ✅ |
| **K8s Ready** | ✅ |

---

## 🎯 Features

- ✅ **20+ API Tests** - Comprehensive test coverage
- ✅ **Mock-based Testing** - Fast, reliable, no external dependencies
- ✅ **Allure Reports** - Beautiful HTML test reports with screenshots
- ✅ **Pydantic v2** - Type-safe API response validation
- ✅ **Retry Logic** - Automatic retry on 5xx errors
- ✅ **Docker Support** - Containerized test execution
- ✅ **Kubernetes Ready** - Deploy tests to K8s clusters
- ✅ **GitHub Actions CI** - Automated testing on every push
- ✅ **Code Coverage** - Integrated with Codecov
- ✅ **Multiple Test Types** - Unit, integration, smoke, performance

---

## 🏗 Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         Tests (tests/)                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │  Vacancies  │ │   Areas     │ │ Dictionaries│ │ Mocks   │ │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └────┬────┘ │
└─────────┼───────────────┼───────────────┼──────────────┼────────┘
          │               │               │              │
          ▼               ▼               ▼              ▼
┌──────────────────────────────────────────────────────────────────┐
│                     API Layer (api/)                             │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ VacanciesApi  │  AreasApi  │  DictionariesApi  │ BaseApi  │ │
│  └─────────────────────────────────────────────────────────────┘ │
└────────────────────┬─────────────────────────────────────────────┘
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
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│                  Validators & Models                             │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │ Validators/ │  │   Models/    │  │  Fixtures/          │  │
│  │ - Response  │  │ - Vacancy    │  │ - http_client       │  │
│  │ - Schema    │  │ - Area       │  │ - vacancies_api     │  │
│  └─────────────┘  └──────────────┘  └─────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Responsibility | Isolation |
|-------|----------------|-----------|
| **Tests** | Test scenarios | Doesn't know about HTTP |
| **API** | Endpoint abstraction | Only knows about models |
| **Core** | HTTP communication | Only knows how to make HTTP requests |
| **Validators** | Response validation | Doesn't know about API |
| **Models** | Data typing | Pure DTOs |

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/ssrjkk/hh-api-framework.git
cd hh-api-framework
pip install -r requirements.txt
```

### 2. Run Tests

```bash
# All mock tests (fast, no external API needed)
pytest tests/test_mocks.py -v

# With Allure report
pytest tests/test_mocks.py --alluredir=allure-results
allure serve allure-results

# With coverage
pytest tests/test_mocks.py --cov=api --cov=core --cov=models --cov-report=html
```

### 3. Run via Docker

```bash
# Build image
docker build -f docker/Dockerfile -t api-tests .

# Run tests in container
docker run --rm api-tests pytest tests/test_mocks.py -v
```

---

## 📚 Test Structure

### Test Categories

| Category | File | Tests | Description |
|----------|------|-------|-------------|
| **Vacancies Search** | `test_mocks.py` | 5 | Search, pagination, filters |
| **Vacancy Details** | `test_mocks.py` | 3 | Get by ID, similar vacancies |
| **Areas** | `test_mocks.py` | 3 | List, by ID, regions |
| **Dictionaries** | `test_mocks.py` | 2 | All dicts, by name |
| **Error Handling** | `test_mocks.py` | 4 | 400, 403, 404, 429, 500 |
| **Response Validator** | `test_mocks.py` | 3 | Status, keys, json_path |

### Test Example

```python
@responses.activate
@allure.title("Поиск возвращает вакансии с правильной структурой")
def test_search_returns_vacancies(self, http_client_mock: HTTPClient) -> None:
    responses.add(
        responses.GET,
        "https://api.hh.ru/vacancies",
        json={"items": [{"id": "12345", "name": "QA Engineer"}]},
        status=200,
    )
    
    api = VacanciesApi(http_client_mock)
    response = api.search(text="QA", area="1", per_page=10)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "QA Engineer"
```

---

## 🛠 Technology Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Testing Framework** | pytest 8.1+ | Test orchestration |
| **HTTP Client** | requests 2.31+ | HTTP client with session pooling |
| **Data Validation** | pydantic 2.5+ | Response validation & models |
| **Retry Logic** | tenacity 8.2+ | Retry on transient failures |
| **Reporting** | allure-pytest 2.13+ | HTML reports with attachments |
| **CI/CD** | GitHub Actions | Automated testing |
| **Containers** | Docker, K8s | Reproducible environments |

### Development Tools

| Tool | Version | Purpose |
|------|---------|---------|
| **Linter** | ruff 0.1+ | Fast Python linter |
| **Formatter** | black 23.12+ | Code formatting |
| **Type Checker** | mypy 1.8+ | Static type checking |
| **Coverage** | pytest-cov 4.1+ | Code coverage measurement |

---

## 📋 API Coverage

### Vacancies API (`/vacancies`)

| Method | Endpoint | Description | Tests |
|--------|-----------|-------------|-------|
| GET | `/vacancies` | Search vacancies | ✅ |
| GET | `/vacancies/{id}` | Get vacancy by ID | ✅ |
| GET | `/vacancies/{id}/similar_vacancies` | Similar vacancies | ✅ |

**Parameters Tested:**
- `text` - Search query
- `area` - Region ID
- `per_page` - Results per page
- `page` - Page number
- `experience` - Experience level
- `employment` - Employment type
- `salary` - Salary filter
- `currency` - Currency code

### Areas API (`/areas`)

| Method | Endpoint | Description | Tests |
|--------|-----------|-------------|-------|
| GET | `/areas` | Get all areas | ✅ |
| GET | `/areas/{id}` | Get area by ID | ✅ |
| GET | `/metro_areas/{id}` | Get metro areas | ⏳ |
| GET | `/areas?type=region` | Get regions | ✅ |

### Dictionaries API (`/dictionaries`)

| Method | Endpoint | Description | Tests |
|--------|-----------|-------------|-------|
| GET | `/dictionaries` | Get all dictionaries | ✅ |
| GET | `/dictionaries/{name}` | Get dictionary by name | ✅ |

**Dictionaries Covered:**
- `experience` - Experience levels
- `employment` - Employment types
- `schedule` - Work schedules
- `education` - Education levels
- `currency` - Currency codes

---

## 🎨 Allure Reports

### View Reports Locally

```bash
# Run tests with Allure
pytest tests/test_mocks.py --alluredir=allure-results

# Serve report (opens in browser)
allure serve allure-results

# Generate static report
allure generate allure-results -o allure-report --clean
```

### CI Allure Report

The framework automatically generates and deploys Allure reports to GitHub Pages on every push to `main`.

**View latest report:** https://ssrjkk.github.io/hh-api-framework/allure/

---

## 🐳 Docker Usage

### Build Images

```bash
# Main test image
docker build -f docker/Dockerfile -t hh-api-tests .

# Linter image
docker build -f docker/Dockerfile.test -t hh-api-lint .
```

### Run Tests in Container

```bash
# Simple run
docker run --rm hh-api-tests pytest tests/test_mocks.py -v

# With mounted reports
docker run --rm \
  -v $(pwd)/allure-results:/app/allure-results \
  hh-api-tests \
  pytest tests/test_mocks.py --alluredir=/app/allure-results
```

### Docker Compose

```bash
# All services
docker-compose -f docker/docker-compose.yml up

# Only tests
docker-compose -f docker/docker-compose.yml up tests

# Only linters
docker-compose -f docker/docker-compose.yml up lint
```

---

## ☸️ Kubernetes Deployment

### Prerequisites

```bash
# Create namespace (optional)
kubectl create namespace api-tests

# Configure secrets
cp k8s/secret.example.yaml k8s/secret.yaml
# Edit secret.yaml with real values
```

### Deploy

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check status
kubectl get pods -l app=api-tests

# View logs
kubectl logs -l app=api-tests -f
```

### Configuration via K8s

All settings are externalized to ConfigMap and Secret:

```yaml
# configmap.yaml
data:
  ENV: "prod"
  BASE_URL: "https://api.hh.ru"
  TIMEOUT: "10"
  MAX_RETRIES: "3"
  LOG_LEVEL: "INFO"
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENV` | `prod` | Environment (prod/dev/test) |
| `BASE_URL` | `https://api.hh.ru` | API base URL |
| `TIMEOUT` | `10` | Request timeout (seconds) |
| `MAX_RETRIES` | `3` | Max retry attempts |
| `RETRY_DELAY` | `1.0` | Delay between retries (seconds) |
| `LOG_LEVEL` | `INFO` | Logging level |

### pytest.ini

```ini
[pytest]
testpaths = tests
markers =
    api: API tests
    integration: Integration tests
    smoke: Smoke tests
    slow: Slow tests
```

---

## 🎯 CI/CD Pipeline

### GitHub Actions Workflow

```
on: [push, pull_request]
  └── jobs:
      ├── lint           # ruff, black, mypy
      ├── test (3.11)   # pytest + Allure
      ├── allure-report  # Generate & deploy Allure
      └── coverage      # pytest --cov + Codecov
```

### Pipeline Stages

| Stage | Tool | What it checks |
|-------|------|----------------|
| **Lint** | ruff | PEP8, imports, naming |
| **Format** | black | Code formatting |
| **Types** | mypy | Type hints correctness |
| **Test** | pytest | All mock tests |
| **Report** | Allure | HTML test report |
| **Coverage** | pytest-cov | Code coverage |

### Badges

- ✅ Linting passed
- ✅ Tests passed
- ✅ Allure report generated
- ✅ Coverage uploaded

---

## 📊 Code Coverage

Current coverage: **85%+**

### Generate Coverage Report

```bash
# Terminal report
pytest tests/test_mocks.py --cov=api --cov=core --cov=models --cov-report=term-missing

# HTML report
pytest tests/test_mocks.py --cov=api --cov=core --cov=models --cov-report=html
open htmlcov/index.html

# XML for CI
pytest tests/test_mocks.py --cov=api --cov=core --cov=models --cov-report=xml
```

---

## 🧪 Testing Patterns

### 1. Mock-based Testing

Using `responses` library to mock HTTP calls:

```python
@responses.activate
def test_search_returns_vacancies():
    responses.add(
        responses.GET,
        "https://api.hh.ru/vacancies",
        json={"items": [...]},
        status=200,
    )
    # Test code here
```

### 2. Response Validation

Fluent DSL for response validation:

```python
ResponseValidator(response) \
    .status(200) \
    .has_keys(["id", "name", "employer"]) \
    .json_path("items", lambda x: len(x) > 0) \
    .response_time_under(3000) \
    .raise_if_errors()
```

### 3. Pydantic Models

Type-safe response parsing:

```python
vacancy = Vacancy.model_validate(response.json())
assert isinstance(vacancy.id, str)
assert isinstance(vacancy.name, str)
```

---

## 📁 Project Structure

```
hh-api-framework/
├── api/                          # API Layer
│   ├── base_api.py               # Base class with HTTP methods
│   ├── vacancies_api.py          # /vacancies endpoints
│   ├── areas_api.py              # /areas endpoints
│   └── dictionaries_api.py       # /dictionaries endpoints
│
├── core/                         # Core components
│   ├── http_client.py            # requests.Session + retry
│   ├── config.py                 # Config from env vars
│   └── retry.py                  # tenacity decorators
│
├── models/                       # Pydantic models
│   ├── vacancy.py                # Vacancy, VacancySearchResponse
│   ├── area.py                   # AreaModel
│   └── dictionary.py             # DictionariesResponse
│
├── validators/                   # Response validators
│   ├── response_validator.py     # Fluent DSL
│   └── schema_validator.py       # JSON Schema validation
│
├── tests/                        # Test scenarios
│   ├── test_mocks.py             # Mock-based tests (20+ tests)
│   ├── test_vacancies.py         # Live API tests
│   ├── test_areas.py             # Live API tests
│   ├── test_dictionaries.py      # Live API tests
│   ├── test_integration.py       # Integration tests
│   └── test_smoke.py             # Smoke tests
│
├── fixtures/                     # Pytest fixtures
│   ├── api_fixtures.py           # http_client, vacancies_api
│   └── data_fixtures.py         # Test data loader
│
├── docker/                       # Docker files
│   ├── Dockerfile               # Main image
│   ├── Dockerfile.test          # Linter image
│   └── docker-compose.yml       # Local orchestration
│
├── k8s/                         # Kubernetes manifests
│   ├── configmap.yaml           # Configuration
│   ├── deployment.yaml          # Deployment
│   └── secret.example.yaml      # Secret template
│
├── .github/workflows/            # CI/CD
│   └── ci.yml                   # GitHub Actions workflow
│
├── requirements.txt              # Runtime dependencies
├── requirements-dev.txt          # Dev dependencies
├── pyproject.toml               # Project configuration
└── README.md                    # This file
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run linters
ruff check .
black --check .

# Run type checker
mypy api core models validators

# Run tests
pytest tests/test_mocks.py -v
```

---

## 📞 Contact

- **Telegram**: [@ssrjkk](https://t.me/ssrjkk)
- **Email**: ray013lefe@gmail.com
- **GitHub**: [ssrjkk](https://github.com/ssrjkk)
- **Project**: [hh-api-framework](https://github.com/ssrjkk/hh-api-framework)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [HeadHunter API Documentation](https://github.com/hhru/api)
- [pytest Documentation](https://docs.pytest.org/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Allure Framework](https://docs.qameta.io/allure/)

---

## 📈 Changelog

### [Unreleased]
- ✅ Added 20+ mock-based tests
- ✅ Integrated Allure reporting in CI
- ✅ Added comprehensive README
- ✅ Fixed CI issues with hh.ru API 403 errors

### [Initial Release]
- ✅ Basic framework structure
- ✅ Vacancies, Areas, Dictionaries API support
- ✅ Docker and K8s support
- ✅ GitHub Actions CI

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/ssrjkk">ssrjkk</a>
</p>
