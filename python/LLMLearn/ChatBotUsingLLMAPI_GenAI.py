import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

chat = client.chats.create(
    model="gemini-3.5-flash-lite"
)

def chat_with_ai(user_message):
    response = chat.send_message(
        user_message)
    return response.text

while True:
    user_message = input("You: ")
    if user_message == "exit":
        break
    gen_ai_response = chat_with_ai(user_message)
    print(gen_ai_response)

# 1. Write a zero-shot prompt asking an LLM to classify a sentence's sentiment
# Need sentiment of these sentences, 1. The apllication UI needs to improve, 
# 2. Customer not easely understand this application UI, 
# 3. Customer likes the concept of this application development

# 2. Then rewrite it as a few-shot prompt with 3 examples.
# 1. The apllication UI needs to improve Sentiment:3/10, 2. Customer likes the concept of this application development Sentiment: 8/10, these are the examples, 
# Need sentiment of these sentences, I am  able to login application but the homepage landing tooks time from 10 to 20 seconds and also I am can  make payment and I don't see the invoice in the application itself

# 3. Design a system + user prompt pair that asks the model to extract structured JSON data from a piece of text of your choosing (a product review, an email, anything).