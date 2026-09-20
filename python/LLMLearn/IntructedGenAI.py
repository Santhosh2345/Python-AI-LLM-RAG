from google import genai
from google.genai import types

client = genai.Client()

chat = client.chats.create(
    model="gemini-3.8-flash"
)

def chat_with_ai(user_message):
    response = chat.send_message(
        user_message,
        config = types.GenerateContentConfig(
            system_instruction = "You are a json language and code structure known person. Give resposne in json format"
        )
    )
    return response.text

while True:
    user_message = input("You: ")
    genai_response = chat_with_ai(user_message)

    if user_message == "exit":
        break

    print(f'GenAI response: {genai_response}')