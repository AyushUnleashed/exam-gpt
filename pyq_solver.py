import os
from main import generate_mk_notes_topic

def organize_pyq(file_path,subject_name, output_folder):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_module = None

    for line in lines:
        # Check if the line contains 'Module' to identify module headers
        if line.startswith('Module'):
            # Extract the module name from the line
            module_name = line.strip().split(': ')[0]
            # Remove any non-alphanumeric characters and convert to lowercase
            import re
            module_name = re.sub(r'[^a-zA-Z0-9_]', '', module_name).lower()
            # if module_name == "":
            #     module_name = line.strip().split(': ')[0]

            current_module = module_name
            print("\nModule found:",module_name)


            # Create a folder for the module inside the output folder
            module_folder = os.path.join(output_folder, current_module)
            if not os.path.exists(module_folder):
                os.makedirs(module_folder,exist_ok=True)

        # Check if a module has been identified and the line is not empty
        elif current_module and line.strip():
            # Clean the line by removing leading/trailing spaces and newline characters
            topic_name = line.strip()
            print("Making notes for ",topic_name)
            # Call the function to generate notes for the topic


            generate_mk_notes_topic(topic_name,subject_name, module_folder)


if __name__ == "__main__":
    from api.prompts import SUBJECT_NAME
    pyq_file = "generations/syllabus/pyq_data_mining_2018.txt" # Use os.path.join for the path
    year = "2018"
    output_folder = os.path.join("generations", "PYQ", f"{SUBJECT_NAME}_{year}")  # Use os.path.join for the path

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    organize_pyq(pyq_file,SUBJECT_NAME, output_folder)