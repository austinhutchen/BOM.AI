import os
import subprocess
from PyPDF2 import PdfFileReader
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load Llama2 model and tokenizer
model_name = "EleutherAI/gpt-neo-2.7B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_response(prompt, max_length=50):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output = model.generate(input_ids, max_length=max_length, num_return_sequences=1)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

def upload_pdf_to_server(pdf_path, server_url):
    try:
        # Upload the PDF file to the server using curl
        subprocess.run(["curl", "-X", "POST", "-F", f"file=@{pdf_path}", server_url])
        print(f"Uploaded {pdf_path} to {server_url}")
    except Exception as e:
        print(f"Error uploading PDF: {e}")

def handle_pdf(pdf_path):
    # Example: Read metadata from the PDF
    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PdfFileReader(pdf_file)
            metadata = pdf_reader.getDocumentInfo()
            print(f"Title: {metadata.title}")
            print(f"Author: {metadata.author}")
            print(f"Creation Date: {metadata.created}")
    except Exception as e:
        print(f"Error reading metadata: {e}")

# Set the PDF file path
pdf_file_path = "my_pdf.pdf"

# Upload the PDF to a server (replace with your server URL)
upload_pdf_to_server(pdf_file_path, "https://example.com/upload")

# Handle the PDF
handle_pdf(pdf_file_path)

# Initialize the chatbot
print("Chatbot: Hello! How can I assist you today?")

# Chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Chatbot: Goodbye!")
        break
    response = generate_response(user_input)
    print(f"Chatbot: {response}")

