from pypdf import PdfReader
import os, json
from google import genai
from google.genai import types, errors
from pathlib import Path

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
prompt = None

path = "python/LLMLearn/PDFExtract/sample_invoice.pdf"
OUTPUT_PATH = Path("invoice_data.json")

# 1. This is the pdf reading function that extracts text from the PDF and creates a prompt for the LLM to extract structured data.
def read_pdf(path):
    reader = PdfReader(path)
    invoice_text = "\n".join(page.extract_text() for page in reader.pages)
    global prompt
    prompt = f"""
        Extract the following fields from this invoice:
        - invoice_number
        - total_amount
        - due_date in YYYY-MM-DD format
        - Wireless Keyboard

        Rules:
        - Use only information present in the invoice.
        - Do not invent missing values.
        - If a required field is missing or unclear, do not
        call the save tool. Explain what is missing.

        Invoice text:
        {invoice_text}
        """
    return prompt

# 2. This is the REAL Python function/tool implementation
def save_invoice_data(invoice_number: str, total_amount: float, due_date: str, wireless_keyboard: str) -> dict:
    """Save extracted invoice fields into a JSON file.

    Args:
        invoice_number: Invoice number from the document.
        total_amount: Total invoice amount.
        due_date: Due date in YYYY-MM-DD format.
    """

    invoice_data = {
        "invoice_number": invoice_number,
        "total_amount": total_amount,
        "due_date": due_date,
        "wireless_keyboard": wireless_keyboard
    }

     # Load existing records, if any
    if OUTPUT_PATH.exists():
        with OUTPUT_PATH.open("r", encoding="utf-8") as file:
            invoices = json.load(file)
    else:
        invoices = []

    # Save the new invoice
    invoices.append(invoice_data)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(invoices, file, indent=4)

    print("\nInvoice data saved successfully!")

    return {
        "status": "success",
        "saved_data": invoices
    }

# 3. This is the function that streams the response from the LLM and calls the save_invoice_data tool if the required fields are extracted successfully.
def streaming_response_genai():
    try:
        prompt = read_pdf(path)

        chat = client.chats.create(
            model="gemini-3.5-flash-lite",
            config=types.GenerateContentConfig(
                tools=[save_invoice_data],
                max_output_tokens=200,
                temperature=0,
                automatic_function_calling=(
                    types.AutomaticFunctionCallingConfig(
                    disable=False
                    )
                )
            )
        )

        print("GenAI response: ")
        
        for chunk in chat.send_message_stream(prompt):
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

# 4. Call the streaming_response_genai function to extract structured data from the PDF and save it to a JSON file.
streaming_response_genai()