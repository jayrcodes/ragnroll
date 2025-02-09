from utils.chat_completions import chat_completion
from utils.terminal import clear_terminal, print_stream, print_markdown
from utils.error import try_with_ai

def key_takeaways():
    def read_thread_messages():
        context = ""

        with open('data/slack_thread_messages.txt', 'r') as file:
            context = file.read()

        return context

    context = try_with_ai(read_thread_messages)

    prompt = f"""
    Context:
    {context}

    Task:
    first generate a title for the summary, and then
    give me key takeaways keep it short simple english and categorize them.
    and then provide at the end a possible action items.
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

    print_markdown(markdown)

    print("\n\n\n")


key_takeaways()
