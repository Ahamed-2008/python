import os
import json
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv

#loading environment variables
load_dotenv()

#getting API keys from environment variables
gemini_api = os.getenv("GEMINI_API_KEY")
openai_api = os.getenv("OPENAI_API_KEY")
claude_api = os.getenv("CLAUDE_API_KEY")

# Initialize clients for different LLM providers
gemini_client = OpenAI(api_key=gemini_api, base_url="https://generativelanguage.googleapis.com/v1beta/openai")
openai_client = OpenAI(api_key=openai_api)
claude_client = Anthropic(api_key=claude_api)

#Interact with Gemini
gemini_response = gemini_client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "user", "content": "Write a short poem about the sea."}
    ]
)
gemini_poem = gemini_response.choices[0].message.content
print("Gemini Poem:", gemini_poem)


#Interact with OpenAI
openai_response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Write a short poem about the sea."}
    ]
)
openai_poem = openai_response.choices[0].message.content
print("OpenAI Poem:", openai_poem)

poems = [gemini_poem, openai_poem]
models = ["Gemini", "OpenAI"]
zipped_poem = zip(models, poems)
zipped_poem_list = list(zipped_poem)

