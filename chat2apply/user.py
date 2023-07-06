from pydantic import BaseModel

class User(BaseModel):
    """User profile"""

    phone: str
    email: str
    prefered_locations: list[str]
    prefered_job_types: list[str]
