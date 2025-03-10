
from huggingface_hub import InferenceClient
from prompt_config import  create_travel_guide_prompt


def main():
    # Initialize the client
    client = InferenceClient(
        provider="together"
    )
    # Create the chat prompt template
    prompt_template = create_travel_guide_prompt()


    # Prepare the input variables
    preferences = """They preferred Uttrecht over Amsterdam. They preferred s-Hertogenbosch over Eindhoven. They preferred Barcelona over Lisbon. 
    They preffered Belgrade over Zagreb. They preffered Barcelona over all other cities."""
    city = "Istanbul"

    # Format the messages
    messages = prompt_template.format_messages(preferences=preferences, city=city)

    # # Make the API call
    # completion = client.chat.completions.create(
    #     model="deepseek-ai/DeepSeek-R1", 
    #     messages=[{"role": msg.type, "content": msg.content} for msg in messages],
    #     max_tokens=10000,
    #     temperature=0.1
    # )

    # Make the API call
    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct", 
        messages=[{"role": msg.type, "content": msg.content} for msg in messages],
        max_tokens=4096,
        temperature=0.5
    )
    print(completion.choices[0].message)
    # print(completion.choices[0].message)
    # # Write the completion to a file
    # with open("response.txt", "w") as f:
    #     f.write(completion.choices[0].message.content)

if __name__ == "__main__":
    main()