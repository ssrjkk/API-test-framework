from pydantic import BaseModel


class BaseModelPydantic(BaseModel):
    model_config = {"extra": "ignore", "populate_by_name": True}
