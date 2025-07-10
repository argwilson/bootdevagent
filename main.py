import os
from tabnanny import verbose
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from dotenv import load_dotenv
from google import genai
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function
from google.genai import types
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    if len(sys.argv) <= 1:
        print("Usage: python main.py <prompt>")
        sys.exit(1)
    prompt = " ".join(sys.argv[1:])

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Run/Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    if "--verbose" in sys.argv:
        function_call_result = call_function(response.function_calls[0], verbose=True)

        if function_call_result.parts[0].function_response.response is None:
            raise Exception("Error: no response from call_function")

        print(f"-> {function_call_result.parts[0].function_response.response}")

    else:
        function_call_result = call_function(response.function_calls[0])
        if function_call_result.parts[0].function_response.response is None:
            raise Exception("Error: no response from call_function")

if __name__ == "__main__":
    main()
