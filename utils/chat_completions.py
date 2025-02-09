# Example: reuse your existing OpenAI setup
from openai import OpenAI
from utils.config import ENDPOINT, MODEL

# Point to the local server
client = OpenAI(base_url=ENDPOINT, api_key="lm-studio")

def chat_completion(messages, stream=False):
    return client.chat.completions.create(
        model=MODEL,
        stream=stream,
        messages=messages,
        temperature=0.7,
        timeout=2.0
    )
