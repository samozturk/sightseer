# Project: ss (Spot Suggester)

**Version:** 0.1.0

## Description

`ss` is a Python-based web service that provides personalized recommendations for spots (like cafes, bars, museums, hidden gems, etc.) within a specified city. It leverages user preferences, derived from comparisons between cities they've previously liked or disliked, to generate tailored suggestions using a Large Language Model (LLM). The goal is to offer non-touristy, local-like experiences.

The service is built using FastAPI for the web framework, LangChain for orchestrating the interaction with the LLM, and a Hugging Face Endpoint (specifically Mistral-7B-Instruct-v0.2) as the recommendation engine. Pydantic is used for data validation and modeling.

## Features

*   **Personalized Recommendations:** Generates spot suggestions based on user's inferred taste from city preferences.
*   **Focus on Hidden Gems:** Aims to suggest less common, non-touristy locations favored by locals.
*   **FastAPI Backend:** Provides a simple REST API endpoint for getting recommendations.
*   **LangChain Integration:** Uses LangChain to structure prompts, interact with the LLM, and parse the output.
*   **Hugging Face LLM:** Utilizes the Mistral-7B-Instruct-v0.2 model via Hugging Face Endpoints.
*   **Structured Output:** Returns recommendations in a well-defined JSON format using Pydantic models.
*   **Docker Support:** Includes `Dockerfile` and `.dockerignore` for easy containerization.

## How it Works

1.  **API Request:** The client sends a `POST` request to the `/recommendations` endpoint with a JSON payload containing a list of city pairs (e.g., `{"preferred": "Utrecht", "avoid": "Amsterdam"}`).
2.  **Preference Formatting:** The input city pairs are formatted into a natural language sentence describing the user's preferences (e.g., "They preferred Utrecht over Amsterdam, ...").
3.  **LLM Interaction:** The formatted preferences and the target city (currently hardcoded as "Istanbul") are sent to the Mistral-7B LLM via LangChain. The prompt guides the LLM to act as a local travel guide and suggest at least 10 hidden gems.
4.  **Response Parsing:** The LLM's response (expected in JSON format) is parsed and validated against the Pydantic `Response` model.
5.  **API Response:** The validated JSON containing the city name, a summary of the user's taste, and a list of recommended spots (with name, description, address, and category) is returned to the client.

## Project Structure

```
.
├── .dockerignore
├── .gitignore
├── .python-version       # Specifies Python version (e.g., 3.12)
├── Dockerfile            # Docker configuration
├── pyproject.toml        # Project metadata and dependencies (using uv)
├── README.md             # This file
├── uv.lock               # Lock file for dependencies
└── app/
    ├── main.py           # FastAPI application entry point and API endpoint definition
    └── spots/
        ├── main.py       # Core recommendation logic calling LangChain
        ├── models.py     # Pydantic models for API request/response and internal data
        ├── prompt_utils.py # LangChain prompt templates, LLM configuration, and chain setup
        └── demo.ipynb    # (Optional) Jupyter notebook for testing/demonstration
```

## Dependencies

Key dependencies include:

*   `fastapi`: Web framework
*   `uvicorn`: ASGI server
*   `langchain-community`, `langchain-huggingface`: LangChain components
*   `pydantic`: Data validation and settings management
*   `loguru`: Logging library

See `pyproject.toml` for the full list of dependencies.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ss
    ```
2.  **Install Python:** Ensure you have Python 3.12 or higher installed. You can use a tool like `pyenv` to manage Python versions.
3.  **Install Dependencies:** Use `uv` (recommended, based on `pyproject.toml` and `uv.lock`) or `pip`.
    ```bash
    # Using uv
    uv pip install -r requirements.txt # Or uv sync if pyproject.toml is fully configured

    # Or using pip (might need manual creation of requirements.txt)
    # pip install -r requirements.txt
    ```
4.  **Set Environment Variable:** The application requires an API token for the Hugging Face Hub. Set this as an environment variable:
    ```bash
    export HUGGINGFACEHUB_API_TOKEN='your_hugging_face_api_token'
    ```
    Replace `'your_hugging_face_api_token'` with your actual token.

## Running the Application

1.  **Start the FastAPI server:**
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    The `--reload` flag enables auto-reloading during development.

2.  The API will be available at `http://localhost:8000`.

## API Endpoint

### `POST /recommendations`

*   **Description:** Get spot recommendations for a city based on user preferences.
*   **Request Body:**
    ```json
    {
      "pairs": [
        {
          "preferred": "Utrecht",
          "avoid": "Amsterdam"
        },
        {
          "preferred": "s-Hertogenbosch",
          "avoid": "Eindhoven"
        }
      ]
    }
    ```
*   **Response Body (Success - 200 OK):**
    ```json
    {
      "city": "Istanbul", // Currently hardcoded
      "user_taste": "You seem to prefer cities with a strong historical character and perhaps a more relaxed atmosphere compared to larger, bustling metropolises.",
      "recommendations": [
        {
          "name": "Balat Sahaf",
          "description": "A charming second-hand bookstore nestled in the colorful streets of Balat, perfect for finding unique reads.",
          "address": "Balat Mahallesi, Vodina Cd. No:46, 34087 Fatih/İstanbul",
          "category": "Shop"
        },
        {
          "name": "Kadı Nimet Balıkçısı",
          "description": "Authentic fish restaurant in the Kadıköy market, known for its fresh mezes and daily catch.",
          "address": "Caferağa, Güneşli Bahçe Sk. No:26/A, 34710 Kadıköy/İstanbul",
          "category": "Restaurant"
        },
        // ... more recommendations
      ]
    }
    ```
*   **Response Body (Error):** If the LLM fails to generate valid JSON or another error occurs, an appropriate HTTP error (e.g., 500) might be returned.

## Docker

A `Dockerfile` is provided to build a container image for the application.

1.  **Build the image:**
    ```bash
    docker build -t ss-app .
    ```
2.  **Run the container:** Remember to pass the environment variable.
    ```bash
    docker run -d -p 8000:8000 -e HUGGINGFACEHUB_API_TOKEN='your_hugging_face_api_token' --name ss-container ss-app
    ```

## TODO / Potential Improvements

*   **Dynamic City Input:** Modify `app/main.py` to accept the target `city` as part of the API request instead of hardcoding "Istanbul".
*   **Dynamic Preferences:** Remove the hardcoded `preferences` variable in `app/spots/main.py` and rely solely on the API input.
*   **Error Handling:** Implement more robust error handling, especially for LLM failures or invalid responses.
*   **Model Selection:** Allow configuration or selection of different LLMs.
*   **Testing:** Add unit and integration tests.
*   **Refine Prompts:** Experiment with different prompt structures in `app/spots/prompt_utils.py` for potentially better results.
