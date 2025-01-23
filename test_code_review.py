import os
import time
import subprocess
from rich.console import Console
from rich.markdown import Markdown
from datetime import datetime
from utils.chat_completions import chat_completion
from utils.config import CODE_REVIEW_PROJECT_PATH, CODE_REVIEW_CURRENT_BRANCH, CODE_REVIEW_PRODUCTION_BRANCH

project_path = CODE_REVIEW_PROJECT_PATH
current_branch = CODE_REVIEW_CURRENT_BRANCH
production_branch = CODE_REVIEW_PRODUCTION_BRANCH

file_extension_regex = ".php"     
expert_in = "laravel php"

# file_extension_regex = '.vue|.js'
# expert_in = "javascript and vue"

git_changed_files = f"git diff --name-only {production_branch}..{current_branch} | grep -E '{file_extension_regex}'"

def get_files():
    output = subprocess.check_output(f"cd {project_path} && {git_changed_files}", shell=True)

    files = output.decode().strip().split("\n")

    return files


def file_changes(file_path):
    try:
        output = subprocess.check_output(
            f"cd {project_path} && git diff --ignore-space-change --ignore-all-space {production_branch}..{current_branch} -- {file_path} | cat",
            shell=True,
            stderr=subprocess.PIPE
        )
        # Use 'replace' error handler to substitute invalid characters
        return output.decode('utf-8', errors='replace')
    except subprocess.CalledProcessError:
        try:
            subprocess.check_output(
                f"cd {project_path} && git ls-tree -r {production_branch} --name-only -- {file_path}",
                shell=True,
                stderr=subprocess.PIPE
            )
            return "File deleted in current branch"
        except subprocess.CalledProcessError:
            return "New file added in current branch"

def get_files_with_length(file_paths):
    files = []

    for file_path in file_paths:
        files.append({
            "path": file_path,
            "length": len(file_changes(file_path))
        })

    files.sort(key=lambda x: x["length"], reverse=True)

    return files

def is_file_too_large_statistical(file_length, average_length, std_deviation, threshold=2):
    return file_length > (average_length + threshold * std_deviation)

def print_files_too_large_statistical():
    files = get_files_with_length(get_files())
    average_length = sum(file["length"] for file in files) / len(files)
    std_deviation = (sum((file["length"] - average_length) ** 2 for file in files) / len(files)) ** 0.5

    print("Unusually large files (statistical method):")
    for file in files:
        if is_file_too_large_statistical(file["length"], average_length, std_deviation):
            print(f"{file['path']}: {file['length']} chars (>{average_length:.0f} + {2}σ)")


def review_code(file_path):
    prompt = f"""
    Context:
    {file_changes(file_path)}
    """

    system = f"""
    dont review deleted code and if so, only say "Comment: " and then short message. Otherwise
    you are expert {expert_in} developer and perform a code review with format:
    Feedback:
    Security:
    """

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]

    try:
        start = time.time()
        # timestamp formatted
        print("Start time: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        response = chat_completion(messages, stream=False)
        # response = chat_completion(messages, stream=True)
        if response is None:
            print("Error: No response received from chat completion")
            return


        # print_stream(response)

        markdown_response = response.choices[0].message.content
        markdown = Markdown(markdown_response)
        console = Console()
        console.print(markdown)

        end = time.time()
        print("\nEnd time: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # include units
        print("Time taken: ", end - start, " seconds")

    except Exception as e:
        print(f"Error during code review: {str(e)}")

def print_stream(response):
    for chunk in response:
            if chunk and hasattr(chunk, 'choices') and chunk.choices and hasattr(chunk.choices[0], 'delta'):
                content = chunk.choices[0].delta.content
                if content is not None:
                    print(content, end="", flush=True)
            # else if chunks has attribute data
            elif hasattr(chunk, 'data'):
                print(chunk.data)

def review_files():
    files = get_files_with_length(get_files())
    for file in files:
        # exclude large file
        average_length = sum(file["length"] for file in files) / len(files)
        std_deviation = (sum((file["length"] - average_length) ** 2 for file in files) / len(files)) ** 0.5

        if is_file_too_large_statistical(file["length"], average_length, std_deviation):
            # print file too large with path!
            print(file["path"], "String length: " + str(file["length"]), " file is too large")
        else:
            # print(file["path"], "String length: " + str(file["length"]))

            print("================================\n")
            print(file["path"], "\n")
            review_code(file["path"])
            print("\n")

# review_code("app/Http/Controllers/Api/Hub/Scout/ScoutQueriesController.php")
# review_code("app/Services/Audience/AudienceService.php")

# print_files_too_large_statistical()

# print(
    # file_changes("app/Http/Controllers/Api/Hub/Scout/ScoutQueriesController.php")
#     # file_changes("app/Services/Audience/AudienceService.php")
# )

# for file_path in get_files():
#     print(file_path)

review_files()

exit()
