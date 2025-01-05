import json
import traceback

def pretty_print_error(e):
    exception_data = {
        "type": type(e).__name__,
        "message": str(e),
        "traceback": traceback.format_exc()
    }
    pretty_exception = json.dumps(exception_data, indent=4)

    # print(pretty_exception)
    # print(traceback.format_exc())

    print(
        "\n ================================================= \n\n",
        traceback.format_exc(),
        "\n ================================================= \n",
    )
