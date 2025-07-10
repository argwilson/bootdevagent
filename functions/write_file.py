import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        new_file = os.path.abspath(os.path.join(working_directory, file_path))
        if not new_file.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isdir(os.path.abspath(file_path)):
            os.makedirs(file_path)
        
        with open(new_file, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{new_file}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file at the file path with the content provided and outputs the file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of new file that has been written by the function, relative to the working directory.",
            ),
            "contents": types.Schema(
                type=types.Type.STRING,
                description="The contents of the file that has been written by the function, relative to the working directory."
            )
        },
    ),
)