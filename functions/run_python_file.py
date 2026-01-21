import os
from google.genai import types
import subprocess
def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.join(abs_path,file_path)
        target_path = os.path.normpath(target_path)
        valid_target_path = os.path.commonpath([abs_path, target_path]) == abs_path
        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if (os.path.splitext(file_path)[1] != ".py") :
            return f'Error: "{file_path}" is not a Python file'
        command = ["python",target_path]
        if args is not None:
            command.extend(args)
        
        result = subprocess.run(
            command,
            cwd=abs_path,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python files in a specified file path relative to the working directory",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read file from, relative to the working directory (default is the working directory itself)",
            ),
            "args":types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional argument that execute with the intended python file",
            ),
            
        },
    ),
)
