from typing import Annotated

from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel


class CreateUserRequest(BaseModel):
    username: Annotated[str, CreationRule(regex=r'^[a-zA-Z0-9]{3-15}$')]
    password: Annotated[str, CreationRule(regex=r'^[a-z]{4}[A-Z]{3}[0-9]{2}[!$&]{1}{8-15}$')]
    role: Annotated[str, CreationRule(regex=r'^ROLE_USER')]