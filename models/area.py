from pydantic import BaseModel
from typing import Optional, List


class AreaModel(BaseModel):
    model_config = {"extra": "ignore", "populate_by_name": True}

    id: str
    name: str
    parent_id: Optional[str] = None
    areas: List["AreaModel"] = []
    url: Optional[str] = None


AreaModel.model_rebuild()
