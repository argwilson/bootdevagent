import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    try:
        current_directory = os.path.abspath(os.path.join(working_directory, directory))
        if not current_directory.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(current_directory):
            return f'Error: "{directory}" is not a directory'

        def file_format(file_name):
            file_path = os.path.join(current_directory, file_name)
            return f" - {file_name}: file_size={os.path.getsize(file_path)}, is_dir={os.path.isdir(file_path)}"

        for file in os.listdir(current_directory):
            print(file_format(file))
        
    
    except Exception as e:
        return f'Error: {e}'

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

