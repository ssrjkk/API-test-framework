from models.base_model import BaseModelPydantic
from models.vacancy import Vacancy, VacancySearchResponse, Salary
from models.area import AreaModel
from models.dictionary import DictionaryItem, DictionariesResponse

__all__ = [
    "BaseModelPydantic",
    "Vacancy",
    "VacancySearchResponse",
    "Salary",
    "AreaModel",
    "DictionaryItem",
    "DictionariesResponse",
]
