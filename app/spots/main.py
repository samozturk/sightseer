from langchain.output_parsers import PydanticOutputParser

from spots.models import Recommendations, Response
from spots.prompt_utils import chain, format_preferences
from loguru import logger

# TODO; Get preferences as input and format as below
preferences = """They preferred Uttrecht over Amsterdam. They preferred s-Hertogenbosch over Eindhoven. They preferred Barcelona over Lisbon.
They preffered Belgrade over Zagreb. They preffered Barcelona over all other cities."""
city = "Istanbul"


def get_recommendations(preferences: list[dict[str, str]], city: str) -> Recommendations:
    preferences = format_preferences(preferences)
    input_data = {"preferences": preferences, "city": city}

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
    return my_response.dict()
