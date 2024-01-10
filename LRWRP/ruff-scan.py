import os
import subprocess

def run_ruff(file_path):
    """Run Ruff on a single file and return the output."""
    result = subprocess.run(['ruff', file_path], capture_output=True, text=True)
    return result.stdout

def scan_directory(directory):
    """Scan a directory for .py files and run Ruff on each."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"Checking {file_path}")
                output = run_ruff(file_path)
                print(output)

# Replace 'your_project_directory' with the path to your project directory
your_project_directory = 'path/to/your/project'
scan_directory(your_project_directory)
