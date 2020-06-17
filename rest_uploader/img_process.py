import PyPDF2
import os
import tempfile
from uuid import uuid4
from PIL import Image
from pdf2image import convert_from_path
from pytesseract import image_to_string, TesseractError
import base64


class ImageProcessor:
    def __init__(self, language="eng"):
        self.set_language(language)
        self.TEMP_PATH = tempfile.gettempdir()
        print(f"Temp Path: {self.TEMP_PATH}")
        self.PREVIEWFILE = ""

    def set_language(self, language):
        self.LANGUAGE = language
        print(f"Language: {self.LANGUAGE}")

    def open_pdf(self, filename):
        try:
            pdfFileObject = open(filename, "rb")
            pdf_reader = PyPDF2.PdfFileReader(pdfFileObject, strict=False)
            return pdf_reader
        except PyPDF2.utils.PdfReadError:
            print("PDF not fully written - no EOF Marker")
            return None

    def pdf_valid(self, filename):
        if self.open_pdf(filename) is None:
            return False
        else:
            return True

    def pdf_page_to_image(self, filename, page_num=0):
        pages = convert_from_path(filename, 250)
        if page_num == 0:
            tempfile = f"{self.TEMP_PATH}/preview.png"
            self.PREVIEWFILE = tempfile
        else:
            tempfile = f"{self.TEMP_PATH}/{uuid4()}.png"
        pages[page_num].save(tempfile, "PNG")
        return tempfile

    def extract_text_from_pdf(self, filename):
        pdfReader = self.open_pdf(filename)
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
                if extracted_image != f"{self.TEMP_PATH}\preview.png":
                    os.remove(extracted_image)
        return text

    def extract_text_from_image(self, filename):
        try:
            text = image_to_string(Image.open(filename), lang=self.LANGUAGE)
        except TesseractError as e:
            text = "\nCheck Tesseract OCR Configuration\n"
            text += e.message
        return text

    def encode_image(self, filename, datatype):
        encoded = base64.b64encode(open(filename, "rb").read())
        img = f"data:{datatype};base64,{encoded.decode()}"
        return img

    def rotate_image(self, filename, degrees_counterclockwise):
        im = Image.open(filename)
        angle = degrees_counterclockwise
        out = im.rotate(angle, expand=True)
        # overwrite the file
        out.save(filename)
