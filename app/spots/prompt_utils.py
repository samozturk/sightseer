from typing import List # Added for type hinting
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from spots.models import Response, CityPairResponse
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.chains import LLMChain
from langchain_huggingface import HuggingFaceEndpoint
import os
from loguru import logger


SYSTEM = """You are a helpful local travel guide that always responds in valid JSON format.
            Help a customer to find the next bars, cafes, museums, coffee shops, shops, landmarks, remarkable or historical districts, local neigbourhoods, Breweries/Distilleries/Wineries, Local Markets, outdoor areas like parks and gardens, local events etc in their next travel based on their preferences. 
            Avoid popular spots and tourist traps; prefer hidden gems like a local guide would do and suggest at least 10 spots.
            Your response MUST be in valid JSON format. The JSON should be a single object with the following structure:

            EXAMPLE_FORMAT = ```json
            {{city: name of the city,

            user_taste: explain user’s taste and what they prefer in two sentences and use `You` as subject,
            recommendations: [
                {{name: example bar name, 
                description: short description of the spot, 
                address: open address of the location, 
                type: category of the spot}},
            """
HUMAN = """
    PREFERENCES: {preferences}
    CITY: {city}

    Your response MUST be in valid JSON format. The JSON should be a single object with the following structure:

    EXAMPLE_FORMAT = ```json
    {{city: name of the city,

    user_taste: explain user’s taste and what they prefer in two sentences,
    recommendations: [
        {{name: example bar name, 
        description: short description of the spot, 
        address: open address of the location, 
        category: category of the spot}},

…
    ```
    IMPORTANT: If, for any reason, you cannot create valid JSON, return ERROR_RESPONSE. Do not return any other text.

    Do not include any text outside of the JSON. Do your best to infer the user's tastes based on their previous city preferences and apply them to the provided city.
"""

REPO_ID = "mistralai/Mistral-7B-Instruct-v0.2"

HUGGINFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]

# Get SYSTEM and HUMAN templated strings and create the prompt template
system_template_prompt = SystemMessagePromptTemplate.from_template(SYSTEM)
human_template_prompt = HumanMessagePromptTemplate.from_template(
    HUMAN, input_variables=["preferences", "city"]
)
prompt_template = ChatPromptTemplate.from_messages(
    [system_template_prompt, human_template_prompt]
)
# Add logging for prompt template creation
logger.info("Creating system and human prompt templates.")
logger.debug(f"System template: {SYSTEM}")
logger.debug(f"Human template: {HUMAN}")

logger.info("Combining system and human templates into a chat prompt template.")
logger.debug(f"Prompt template: {prompt_template}")

# Define LLM
llm = HuggingFaceEndpoint(
    # repo_id=REPO_ID,
    model=REPO_ID,  # Explicitly set model as well
    max_new_tokens=4800,
    temperature=0.5,
    huggingfacehub_api_token=HUGGINFACEHUB_API_TOKEN,
    task="text-generation",  # Explicitly set the task
)

# Chain them together
chain = prompt_template | llm

def format_preferences(preferences: List[CityPairResponse]) -> str: # Updated type hint
    """
    Formats the preferences into a readable string.
    Args:
        preferences (List[CityPairResponse]): A list of CityPairResponse objects. # Updated docstring
    Returns:
        str: A formatted string of preferences.
    """

    base_str = "They preffered "
    formatted_str = ""
    for preference in preferences:
        formatted_str += f"{preference.preferred} over {preference.avoid}, " # Changed to attribute access
    end_str = base_str + formatted_str
    end_str = end_str[:-2] + "."
    logger.debug(f"Formatted preferences: {end_str}")
    return end_str
