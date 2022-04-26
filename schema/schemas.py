"""
Pydantic schema validation
"""

from pydantic import BaseModel


class UserValidator:
    """Pydantic User validation class"""

    username: str
