from pydantic import BaseModel

class Job(BaseModel):
    """User profile"""

    title: str = ''
    description: str = ''
    location: str = ''
    company_name: str = ''
