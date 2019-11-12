import PyPDF2
from unidecode import unidecode
from PIL import Image
from pdf2image import convert_from_path
from pytesseract import image_to_string
from .settings import TEMP_PATH


def pdf_valid(filename):
    try:
        pdfFileObject = open(filename, "rb")
        PyPDF2.PdfFileReader(pdfFileObject)
        return True
    except PyPDF2.utils.PdfReadError:
        print("PDF not fully written - no EOF Marker")
        return False


def pdf_page_to_image(filename):
    pages = convert_from_path(filename, 250)
    tempfile = TEMP_PATH + "pdfpreview.png"
    pages[0].save(tempfile, "PNG")
    return tempfile


def extract_text_from_pdf(filename):
    pdfFileObject = open(filename, "rb")
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    count = pdfReader.numPages
    text = "\n<!---\n"
    for i in range(count):
        page = pdfReader.getPage(i)
        text += page.extractText()
        text += "\n-->\n"
    return unidecode(text)


def extract_text_from_image(filename):
    text = "\n<!---\n"
    text += image_to_string(Image.open(filename), lang="eng")
    text += "\n-->\n"
    return unidecode(text)
