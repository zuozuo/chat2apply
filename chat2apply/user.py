from pydantic import BaseModel

class User(BaseModel):
    """User profile"""

    name: str = ''
    phone: str = ''
    email: str = ''
    prefered_locations: list[str] = []
    prefered_job_types: list[str] = []

    def as_json(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
        }
