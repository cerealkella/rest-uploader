import PyPDF2
import os
import tempfile
from uuid import uuid4
from PIL import Image
from pdf2image import convert_from_path
from pytesseract import image_to_string, TesseractError


TEMP_PATH = tempfile.gettempdir()

def set_language(language):
    global LANGUAGE
    LANGUAGE = language


def set_temp_path():
    global TEMP_PATH
    TEMP_PATH = tempfile.gettempdir()
    print(f"Temp Path: {TEMP_PATH}")


def open_pdf(filename):
    try:
        pdfFileObject = open(filename, "rb")
        pdf_reader = PyPDF2.PdfFileReader(pdfFileObject, strict=False)
        return pdf_reader
    except PyPDF2.utils.PdfReadError:
        print("PDF not fully written - no EOF Marker")
        return None


def pdf_valid(filename):
    if open_pdf(filename) is None:
        return False
    else:
        return True


def pdf_page_to_image(filename, page_num=0):
    global TEMP_PATH
    pages = convert_from_path(filename, 250)
    if page_num == 0:
        tempfile = f"{TEMP_PATH}\preview.png"
    else:
        tempfile = f"{TEMP_PATH}\{uuid4()}.png"
    pages[page_num].save(tempfile, "PNG")
    return tempfile


def extract_text_from_pdf(filename):
    global TEMP_PATH
    pdfReader = open_pdf(filename)
    count = pdfReader.numPages
    text = ""
    for i in range(count):
        text += f"\n\n***PAGE {i+1} of {count}*** \n\n"
        page = pdfReader.getPage(i)
        embedded_text = page.extractText()
        # if embedded PDF text is minimal or does not exist,
        # run OCR the images extracted from the PDF
        if len(embedded_text) >= 100:
            text += embedded_text
        else:
            extracted_image = pdf_page_to_image(filename, i)
            text += extract_text_from_image(extracted_image)
            if extracted_image != f"{TEMP_PATH}\preview.png":
                os.remove(extracted_image)
    return text


def extract_text_from_image(filename):
    try:
        text = image_to_string(Image.open(filename), lang=LANGUAGE)
    except TesseractError as e:
        text = "\nCheck Tesseract OCR Configuration\n"
        text += e.message
    return text
