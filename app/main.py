from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from spots.main import get_recommendations
from spots.models import Pairs, Response # Import Response model


# Initialize the FastAPI app
app = FastAPI()


# Endpoint to accept a dictionary of city pairs
@app.post("/recommendations", response_model=Response) # Change response_model to Response
def get_city_recommendations(preferences: Pairs):
    """
    Endpoint to get recommendations based on city pairs.
    """
    # Here you would typically call your recommendation logic
    # For now, we'll just return the received preferences
    return get_recommendations(preferences=preferences.pairs, city="Istanbul")

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
