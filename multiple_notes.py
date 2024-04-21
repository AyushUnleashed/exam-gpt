import os
from main import generate_mk_notes_topic

def organize_syllabus(file_path,subject_name, output_folder):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_module = None

    for line in lines:
        # Check if the line contains 'Module' to identify module headers
        if line.startswith('Module'):
            # Extract the module name from the line
            module_name = line.strip().split(': ')[0]
            import re
            module_name = re.sub(r'[^a-zA-Z0-9_]', '', module_name).lower()
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
    subject_name = "Simulation & Modeling"
    syllabus_file = os.path.join("generations", "sim_syllabus_2.txt")  # Use os.path.join for the path
    output_folder = os.path.join("generations", "notes_new", subject_name)  # Use os.path.join for the path

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    organize_syllabus(syllabus_file,subject_name, output_folder)