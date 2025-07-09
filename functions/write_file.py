import os

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