import json
import traceback
from utils.chat_completions import chat_completion
from utils.terminal import clear_terminal, print_stream, print_markdown

def pretty_print_error(e):
    exception_data = {
        "type": type(e).__name__,
        "message": str(e),
        "traceback": traceback.format_exc()
    }
    pretty_exception = json.dumps(exception_data, indent=4)

    # print(pretty_exception)
    # print(traceback.format_exc())

    error = traceback.format_exc()

    markdown = f"- Raw Exception:\n\n```\n{error}\n```"

    print_markdown(markdown)

def simplify_error(error = None):
    if error:
        prompt = f"""
        Context:
        {error}

        Task:
        Explain the error in a single sentence.
        """

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]

        # chat completion but streaming
        response = chat_completion(messages, stream=True)

        clear_terminal()
        markdown = print_stream(response)
        clear_terminal()

        pretty_print_error(error)

        markdown = f"- AI Simplified Error:\n\n{markdown}"
        print_markdown(markdown)

def try_with_ai(function, *args, **kwargs):
    try:
        return function(*args, **kwargs)
    except Exception as e:
        simplify_error(e)
        exit()
