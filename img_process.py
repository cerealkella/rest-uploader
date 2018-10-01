import PyPDF2
import sys
import io
from unidecode import unidecode
from PIL import Image
from pdf2image import convert_from_path
from pytesseract import image_to_string


# sys.stdout = open('output.md', 'wt')


def pdf_page_to_image(filename):
    pages = convert_from_path(filename, 250)
    pages[0].save("out.png", "PNG")


def extract_text_from_pdf(filename):
    pdfFileObject = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    count = pdfReader.numPages
    for i in range(count):
        page = pdfReader.getPage(i)
        text = ("<!---")
        text += (page.extractText())
        text += ("-->")
    return unidecode(text)


def extract_text_from_image(filename):
    text = ("<!---")
    text += image_to_string(Image.open(filename), lang="eng")
    text += ("-->")
    return unidecode(text)


# pdf_page_to_image(filename)
# print(extract_text_from_image("out.png"))
