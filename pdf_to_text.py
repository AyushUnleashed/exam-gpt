import os
import PyPDF2

class FileNotFound(Exception):
    pass

def convert_pdf_to_text(pdf_filename):
    # Check if the file exists
    if not os.path.exists(pdf_filename):
        raise FileNotFound(f"The file '{pdf_filename}' does not exist.")

    try:
        # Open the PDF file
        pdf_file = open(pdf_filename, 'rb')

        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to store the text
        text = ""

        # Loop through each page in the PDF and extract text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        # Call the function to save the text to a text file
        save_text_to_file(pdf_filename, text)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pdf_file.close()

def save_text_to_file(pdf_filename, text):
    # Create the "generations" folder if it doesn't exist
    if not os.path.exists("generations"):
        os.makedirs("generations")

    # Create a text file with the same name as the PDF in the "generations" folder
    txt_filename = os.path.join("generations", os.path.splitext(os.path.basename(pdf_filename))[0] + ".txt")
    with open(txt_filename, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)
    print(f"Text extracted and saved to '{txt_filename}'.")

def main():
    # Input PDF file name
    pdf_filename = "generations/ir_pyq.pdf"
    # Extract text from the PDF
    convert_pdf_to_text(pdf_filename)

if __name__ == "__main__":
    main()
