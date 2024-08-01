import PyPDF2
import os
import re
import pytesseract
from pdf2image import convert_from_path
from PIL import Image


# /usr/bin/tesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


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


def get_text_from_pdf_image(pdf_file):
    """
    Extract text from a given PDF file using OCR.

    Parameters:
    pdf_file (str): The path to the PDF file.

    Returns:
    str: The extracted text from the PDF.
    """
    try:
        pages = convert_from_path(pdf_file, 600)
        text_data = ''
        for i, page in enumerate(pages):
            # save the image of the page
            # page.save(f'temp{i}.jpg', 'JPEG')
            text = pytesseract.image_to_string(page)
            text_data += remove_filenames(text) + '\n'
        return text_data
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
    files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
    # removing .pdf extension
    files = [f[:-4] for f in files]
    return files
