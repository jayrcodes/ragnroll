import json
import traceback
from utils.chat_completions import chat_completion
from utils.terminal import clear_terminal, print_stream, print_markdown
import pydash
from utils.config import ENABLE_TRY_CATCH_AI

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

        response = chat_completion(messages, stream=True)

        clear_terminal()
        markdown = print_stream(response)
        clear_terminal()

        pretty_print_error(error)

        markdown = f"- AI Simplified Error:\n\n{markdown}"
        print_markdown(markdown)

def short_traceback(e):
    tb = traceback.format_exception(type(e), e, e.__traceback__)
    return "".join(tb[-3:])

def try_catch(function, *args, **kwargs):
    try:
        response = function(*args, **kwargs)
        return [response, None]
    except Exception as e:

        if ENABLE_TRY_CATCH_AI:
            simplify_error(e)
        else:
            text = short_traceback(e)
            markdown = f"- Shorter Error:\n\n```\n{text}\n```"
            print_markdown(markdown)

        return [None, e]

def print_exit_if_error(e = None):
    if e:
        print("\n")
        print(e)
        exit()
