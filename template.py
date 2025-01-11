import os

# Define the project folder structure (without the root TextAnalyzer folder)
project_structure = {
    "data": {
        "raw": {},
        "processed": {}
    },
    "src": {
        "__init__.py": "",
        "main.py": "",
        "calculate_metrics.py": "",
        "data_extractor.py": "",
        "text_preprocessing.py": "",
        "utils.py": ""
    },
    "notebooks": {},
    "requirements.txt": "",
}

# Function to create the folder structure
def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # Create folder
            os.makedirs(path, exist_ok=True)
            # Recursively create subfolders/files
            create_structure(path, content)
        else:
            # Create file
            with open(path, 'w') as file:
                file.write(content)

# Specify the base path
base_path = os.getcwd()  # Current working directory
create_structure(base_path, project_structure)

print("Project structure created successfully!")
