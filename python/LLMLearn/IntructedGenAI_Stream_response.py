from google import genai
from google.genai import types, errors
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
config = types.GenerateContentConfig(
                    system_instruction = "You are an expert in JSON and code structure. Always respond in valid JSON format.",
                    max_output_tokens = 100,
                    automatic_function_calling = types.AutomaticFunctionCallingConfig(
                        disable = True
                    )
)

usage = None

def streaming_response_genai(user_message):
    try:
        stream = client.models.generate_content_stream(
                model="gemini-3.5-flash-lite",
                contents = user_message,
                config=config
        )

        print("GenAI response: ")
        
        for chunk in stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)

            if chunk.usage_metadata:
                global usage
                usage = chunk.usage_metadata
    
    except errors.APIError as e:
        if e.code == 429:
            print("Rate limit exceeded")

        elif e.code == 401:
            print("Authentication error")

        elif e.code == 403:
            print("Permission denied")

        elif e.code == 404:
            print("Model or resource not found")

        elif e.code == 500:
            print("Gemini server error")

        elif e.code == 503:
            print("Gemini service temporarily unavailable")
        
        else:
            print(f"API error {e.code}: {e.message}")

    except errors.ClientError as e:
        print(f'error code {e.code}')
        print(f'error message {e.message}')

while True:
    user_message = input("You: ")

    if user_message == "exit":
            break
    
    streaming_response_genai(user_message)

print(f'Input Token usage: {usage.prompt_token_count}')
print(f'Output token usage: {usage.candidates_token_count}')
print(f'Total token usage: {usage.total_token_count}')