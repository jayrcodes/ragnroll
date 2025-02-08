from utils.chat_completions import chat_completion
from rich.console import Console
from rich.markdown import Markdown

def clear_terminal():
    print("\033c", end="")
    print("\n\n\n")

def key_takeaways():
    # read data/slack_thread_messages.txt
    with open('data/slack_thread_messages.txt', 'r') as file:
        context = file.read()

    prompt = f"""
    Context:
    {context}

    Task:
    give me key takeaways keep it short simple english and categorize them.
    and then provide at the end a possible action items.
    """

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]

    # chat completion but streaming
    response = chat_completion(messages, stream=True)

    response_messages = []

    clear_terminal()

    for chunk in response:
        print(chunk.choices[0].delta.content, end='', flush=True)

        if chunk.choices[0].delta.content:
            response_messages.append(chunk.choices[0].delta.content)

    clear_terminal()

    markdown = "".join(response_messages)
    
    # parse using console makedown
    markdown = Markdown(markdown)
    console = Console()
    console.print(markdown)

    print("\n\n\n")


key_takeaways()
