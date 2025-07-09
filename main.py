import os
from functions.get_files_info import schema_get_files_info
from dotenv import load_dotenv
from google import genai
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

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
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

    print(response.text)

    print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")

    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
