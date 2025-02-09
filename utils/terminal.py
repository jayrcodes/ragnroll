from rich.console import Console
from rich.markdown import Markdown
import platform
import os

def clear_terminal():
    isMac = platform.system() == "Darwin"
    if isMac:
        os.system("clear")
    else:
        print("\033c", end="")

def print_stream(response):
    messages = []

    for chunk in response:
        print(chunk.choices[0].delta.content, end='', flush=True)

        if chunk.choices[0].delta.content:
            messages.append(chunk.choices[0].delta.content)

    return "".join(messages)

def print_markdown(markdown):
    markdown = Markdown(markdown)
    console = Console()
    console.print(markdown)