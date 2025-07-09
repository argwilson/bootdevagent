import os
import subprocess

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