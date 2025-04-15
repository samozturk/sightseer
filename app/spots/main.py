from typing import List # Added import
from langchain.output_parsers import PydanticOutputParser

from spots.models import Recommendations, Response, CityPairResponse # Added CityPairResponse
from spots.prompt_utils import chain, format_preferences
from loguru import logger

# TODO; Get preferences as input and format as below
preferences = """They preferred Uttrecht over Amsterdam. They preferred s-Hertogenbosch over Eindhoven. They preferred Barcelona over Lisbon.
They preffered Belgrade over Zagreb. They preffered Barcelona over all other cities."""
city = "Istanbul"


def get_recommendations(preferences: List[CityPairResponse], city: str) -> Response: # Updated signature
    formatted_preferences_str = format_preferences(preferences) # Use new variable
    input_data = {"preferences": formatted_preferences_str, "city": city} # Use new variable

    # Run the chain
    response = chain.invoke(input_data)
    logger.debug(f"Response from chain: {response}")

    # Add check for None response
    if response is None:
        logger.error("Received None response from the LLM chain.")
        raise ValueError("LLM chain returned None, cannot proceed with parsing.")

    parser = PydanticOutputParser(pydantic_object=Response)
    logger.debug(f"Parser created: {parser.get_format_instructions()}")
    my_response = parser.parse(response)
    return my_response # Return the Response object directly
