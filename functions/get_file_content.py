import os

def get_file_content(working_directory, file_path):
    try:
        current_file = os.path.abspath(os.path.join(working_directory, file_path))
        if not current_file.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(current_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        MAX_CHARS = 10000
        with open(current_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        
        if len(file_content_string) < MAX_CHARS:
            return file_content_string
        return file_content_string + f' [...File "{file_path}" truncated at 10000 characters]'

    except Exception as e:
        return f'Error: {e}'