from pydantic import BaseModel
from typing import List

class Recommendations(BaseModel):
    name: str
    description: str
    address: str
    category: str

class Response(BaseModel):
    city: str
    user_taste: str
    recommendations: Recommendations