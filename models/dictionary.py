from pydantic import BaseModel
from typing import Dict, List, Any


class DictionaryItem(BaseModel):
    model_config = {"extra": "ignore", "populate_by_name": True}

    id: str
    name: str


class DictionariesResponse(BaseModel):
    model_config = {"extra": "ignore", "populate_by_name": True}

    vacancy_type: List[DictionaryItem] = []
    experience: List[DictionaryItem] = []
    employment: List[DictionaryItem] = []
    schedule: List[DictionaryItem] = []
    language: List[DictionaryItem] = []
    professional_role: List[DictionaryItem] = []
    employer_type: List[DictionaryItem] = []
    org_type: List[DictionaryItem] = []
    education_level: List[DictionaryItem] = []
