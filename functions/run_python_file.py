import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    try:
        current_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not current_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(current_path):
            return f'Error: File "{file_path}" not found.'
        elif file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file.'
        
        try:
            result = subprocess.run(["python", current_path],capture_output=True, timeout=30)

            if result == None:
                return "No output produced."

            return(
                f"STDOUT: {result.stdout}",
                f"STDERR: {result.stderr}"
            )

        except subprocess.CalledProcessError as e:
            return f"Command failed with return code {e.returncode}"

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Will run a file as a python file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python file which has been executed.",
            ),
        },
    ),
)