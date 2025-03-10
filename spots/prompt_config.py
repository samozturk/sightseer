from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from models import Response
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.chains import LLMChain
from langchain_huggingface import HuggingFaceEndpoint
import os

parser = JsonOutputParser(pydantic_object=Response)



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


def create_travel_guide_prompt(system=SYSTEM, human=HUMAN):
    """ Returns a ChatPromptTemplate object to be formatted with user input.
    """
    system_template_prompt = SystemMessagePromptTemplate.from_template(system)
    human_template_prompt = HumanMessagePromptTemplate.from_template(human)
    prompt = ChatPromptTemplate.from_messages([
        system_template_prompt,
        human_template_prompt
        ]
    )
    prompt = prompt.partial(format_instructions=parser.get_format_instructions())
    return prompt

# print(create_travel_guide_prompt())

# prompt_template = create_travel_guide_prompt()
def create_travel_guide_chain():
    # Create the JSON parser
    parser = JsonOutputParser(pydantic_object=Response)
    
    # Create the prompt template
    prompt = create_travel_guide_prompt()
    
    # Initialize HuggingFace endpoint
    HUGGINFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]
    # repo_id = "meta-llama/Llama-3.2-3B-Instruct"
    repo_id = "meta-llama/Llama-3.3-70B-Instruct"

    llm = HuggingFaceEndpoint(
        repo_id=repo_id,
        max_new_tokens=4096,
        temperature=0.5,
        huggingfacehub_api_token=HUGGINFACEHUB_API_TOKEN,
    )
    # Create the chain
    chain = prompt | llm | parser

    return chain


# Prepare the input variables
preferences = """They preferred Uttrecht over Amsterdam. They preferred s-Hertogenbosch over Eindhoven. They preferred Barcelona over Lisbon. 
They preffered Belgrade over Zagreb. They preffered Barcelona over all other cities."""
city = "Istanbul"

def get_travel_recommendations(chain, preferences, city):
    response = chain.invoke({
        "preferences": preferences,
        "city": city
    })
    return response

print(get_travel_recommendations(create_travel_guide_chain(), preferences, city))