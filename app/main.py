from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

# Initialize the FastAPI app
app = FastAPI()

# Define the Pydantic model for the response
class CityPairResponse(BaseModel):
    city1: str
    city2: str

# Endpoint to accept a dictionary of city pairs
@app.post("/city-pairs/", response_model=Dict[str, CityPairResponse])
def get_city_pairs(city_pairs: Dict[str, Dict[str, str]]):
    


# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)