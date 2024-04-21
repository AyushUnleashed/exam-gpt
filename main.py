import os

import requests
from google_dump import search_and_extract
from api.gpt_api import fetch_openai_response

def fetch_gpt_response(prompt: str):
    # make post request with gpt api & get output
    message = {'message': prompt}
    url = 'http://localhost:5001/chat'
    try:
        response = requests.post(url, json=message)
        if (response.status_code != 200):
            print(f"Response failed with status code: {response.status_code}")
            return None
        else:
            result = response.text
            return result
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

def generate_mk_notes_topic(topic_name, subject_name,module_path):
    # Create a directory for the module if it doesn't exist
    # module_dir = os.path.join(module_path, subject_name)
    module_dir = module_path
    if not os.path.exists(module_dir):
        os.makedirs(module_dir, exist_ok=True)
    # Generate the file name based on the topic
    import re
    # Clean the topic_name by removing invalid characters
    short_topic_name = re.sub(r'[\/:*?"<>|]', '_', topic_name)
    # Ensure the topic_name is not too long
    if len(short_topic_name) > 100:  # Adjust the maximum length as needed
        short_topic_name = short_topic_name[:100]

    file_name = f"{short_topic_name}.md"
    # Define the full file path
    file_path = os.path.join(module_dir, file_name)

    # Check if the file already exists
    if os.path.exists(file_path):
        print(f"Notes for '{short_topic_name}' already exist. Skipping.")
        return  # Skip generating notes if the file already exists
    prep(topic_name, subject_name,file_path)


def prep(topic_name, subject_name,file_path):
    # Fetch data about the topic
    dump, domain = search_and_extract(topic_name)
    # return
    print(f"Online Scrapping completed for topic:{topic_name}")
    # if dump == 'no':
    #     print(f"No data found for the topic {topic_name}")
    #     return
    #

    # base_prompt = f"Ignore all previous instructions, You are GPT Academy, an artificial intelligence with profound knowledge in field of {subject_name} subject & markdown code note making, Create comprehensive markdown code for notes for college exams. \
    #    IMP Note: Notes should be in proper markdown code format, provide markdown code, using H1,H2,H3, bold imp topics, using lists etc appropriately.\
    #        First portion should contain an overview of the topic, Start with Overview: .    Second portion should contain detailed explanation, Details: .\
    #            Note: if data is given below, you may use it as guide for making notes. but if it's not given use your profound knowledge in {subject_name}  \
    #             At last Give ShortNotes: condensed pointed version of the whole note that encompases key details that can be expanded to full notes. \
    #                 Short notes should contain  numbered lists, points, sub points, -> , imp. keywords.\
    #               Note: Use lists , numbered points, if using a highly technical term try to explain it too, remove unnecessary things like promotions if present in data\
    #                   Now analyse data &: ----------------\n {dump} \n ------------- \n generate notes, Give markdown code,  code with copy feature, not inbuilt "

    prompt =f"Generate Markdown notes based on : ----------------\n {topic_name} of subject: {subject_name} \n ------------- \n"
    base_response = fetch_openai_response(prompt)
    print('\n Waiting for response from AI')
    if base_response == None:
        print("Server is down")
        return

    # Assuming the overview ends at the first newline
    overview, detailed_explanation = base_response.split('\n', 1)
    print("Overview:", overview)
    print("Detailed Explanation:", detailed_explanation)

    # Saving the notes to a markdown file
    # file_name = f"{topic_name}_markdown"
    with open(file_path, 'w',encoding='utf-8') as f:
        f.write(f"Overview:\n{overview}\n")
        f.write(f"Detailed Explanation:\n{detailed_explanation}")

    from pyhtml2pdf import converter
    import os
    # importing the required module
    # import pdfkit
    #
    # # configuring pdfkit to point to our installation of wkhtmltopdf
    # config = pdfkit.configuration(wkhtmltopdf = r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    #
    # # converting html file to pdf file
    # pdfkit.from_file('sample.html', 'output.pdf', configuration = config)

if __name__ == "__main__":
    module_path = "generations/module 1"
    generate_mk_notes_topic(" Cloudsim","Cloud Computing",module_path)