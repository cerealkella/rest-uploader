import PyPDF2
import sys
import io
from unidecode import unidecode
from PIL import Image
from pdf2image import convert_from_path
from pytesseract import image_to_string
from settings import TEMP_PATH

# sys.stdout = open('output.md', 'wt')


def pdf_valid(filename):
    pdfFileObject = open(filename, 'rb')
    try:
        pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
        return True
    except PdfReadError:
        print("PDF not fully written")
        return False


def pdf_page_to_image(filename):
    pages = convert_from_path(filename, 250)
    tempfile = TEMP_PATH + "pdfpreview.png"
    pages[0].save(tempfile, "PNG")
    return tempfile


def extract_text_from_pdf(filename):
    pdfFileObject = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    count = pdfReader.numPages
    for i in range(count):
        page = pdfReader.getPage(i)
        text = "\n<!---\n"
        text += page.extractText()
        text += "\n-->\n"
    return unidecode(text)


def extract_text_from_image(filename):
    text = "\n<!---\n"
    text += image_to_string(Image.open(filename), lang="eng")
    text += "\n-->\n"
    return unidecode(text)


# pdf_page_to_image(filename)
# print(extract_text_from_image("out.png"))
