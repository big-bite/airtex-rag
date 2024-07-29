import PyPDF2
import os
import re

def remove_filenames(text):
    # Regular expression to match lines containing ".pdf"
    pdf_pattern = r'.*\.pdf.*'
    print(re.findall(pdf_pattern, text))
    # Substitute matched lines with empty string
    cleaned_text = re.sub(pdf_pattern, '', text)
    return cleaned_text




def get_pdf_text(pdf_file):
    """
    Extract text from a given PDF file.

    Parameters:
    pdf_file (str): The path to the PDF file.

    Returns:
    str: The extracted text from the PDF.
    """
    try:
        with open(pdf_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            # Check for PDF encryption
            # if reader.isEncrypted:
            #     reader.decrypt('')  # Attempt to decrypt with an empty password

            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += remove_filenames(page.extract_text())


            return text
    except FileNotFoundError:
        return "The file was not found."
    except Exception as e:
        return f"An error occurred: {e}"
    

def list_pdf_files(directory):
    """
    List all PDF files in the given directory.

    Parameters:
    directory (str): The directory to search for PDF files.

    Returns:
    list: A list of PDF file names.
    """
    return [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
