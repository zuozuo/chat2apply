from pydantic import BaseModel

class Company(BaseModel):
    """Company profile"""

    name: str = ''
