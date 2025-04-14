from pydantic import BaseModel, Field
from typing import List

class Recommendations(BaseModel):
    name: str = Field(description="name of the spot")
    description: str = Field(description="short description of the spot")
    address: str = Field(description="open address of the location")
    category: str = Field(description="category of the spot")

class Response(BaseModel):
    city: str = Field(description="name of the city")
    user_taste: str = Field(description="explain user’s taste and what they prefer in two sentences and use `You` as subject")
    recommendations: List[Recommendations] = Field(description="list of recommendations")

# Models for the API
class CityPairResponse(BaseModel):
    preferred: str
    avoid: str

class Pairs(BaseModel):
    pairs: List[CityPairResponse]