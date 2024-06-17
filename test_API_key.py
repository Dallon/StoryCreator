import logging
from openai import OpenAI

#small script to make sure that your openAI api key works

def setup_openai_client(api_key: str):
    client = OpenAI(api_key=api_key)
    return client

def test_openai_key(client):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Hello, how are you?",
                }
            ],
            model="gpt-4o",
            max_tokens=5
        )
        print("API Key is working! Response:")
        print(response.choices[0].message.content.strip())
    except Exception as e:
        logging.error(f"Error during API call: {e}")
        print("There was an error with the API Key or request:")
        print(e)

if __name__ == "__main__":
    # Replace 'your-api-key' with your actual OpenAI API key
    api_key = 'your-api-key'
    client = setup_openai_client(api_key)
    test_openai_key(client)
