"""
Pydantic schema validation
"""

from pydantic import BaseModel


class UserValidator(BaseModel):
    """Pydantic User validation class"""

    username: str
