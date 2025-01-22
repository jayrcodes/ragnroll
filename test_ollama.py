from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from utils.config import OLLAMA_MODEL

template = """Question: {question}

Answer: Let's think step by step."""

prompt = ChatPromptTemplate.from_template(template)

def chat(user_query):
    model = OllamaLLM(model=OLLAMA_MODEL)

    chain = prompt | model

    result = chain.invoke({"question": user_query})

    print(result)

def chat_stream(user_query):
    model = OllamaLLM(model=OLLAMA_MODEL, stream=True)

    chain = prompt | model

    result = chain.invoke({"question": user_query})

    for chunk in result:
        print(chunk, end="", flush=True)

def main():
    user_query = """

    Using laravel php, use tdd

    Implement api that can handle stripe and chargebee

    """;

    # chat(user_query)

    chat_stream(user_query)

main()