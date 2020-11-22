import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os
import io
import base64

plt.switch_backend('agg')

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


def get_pages(pdf_file):
    pages = convert_from_path(pdf_file, 500, poppler_path=r'C:\poppler-20.11.0\bin')
    return pages

def pdf_to_image(pdf_file):
    global total_pages
    # Store all the pages of the PDF in a variable
    pages = get_pages(pdf_file)

    # Counter to store images of each page of PDF to image
    image_counter = 1

    # Iterate through all the pages stored above
    for page in pages:
        filename = "static/Docs/page_"+str(image_counter)+".jpg"
        # Save the image of the page in system
        page.save(filename, 'JPEG')
        # Increment the counter to update filename
        image_counter = image_counter + 1
    total_pages = image_counter
    return image_counter


def get_text(pdf_file):
    result_text = ""
    for i in range(1, pdf_to_image(pdf_file)):
        filename = "static/Docs/page_" + str(i) + ".jpg"

        # Recognize the text as string in image using pytesserct
        text = str((pytesseract.image_to_string(Image.open(filename))))
        text = text.replace('-\n', '')
        # Finally, write the processed text to the file.
        result_text += text

    tokens = word_tokenize(result_text)
    punctuations = ["(", ")", ";", ",", ",", "{", "}", "[", "]"]
    wordstops = stopwords.words('english')
    keywords = [word.lower() for word in tokens if not word in wordstops and not word in punctuations]
    return keywords

def get_pie_chart(pdf_file):
    plt.clf()
    data = pd.read_csv("static/Datasets/domaines.csv", delimiter=',', quotechar='"', encoding="utf8")
    domaines = []
    for d in data:
        domaines.append(d)

    dict_data={domaine: [] for domaine in domaines}
    for domain in domaines:
        dict_data
    for elt in get_text(pdf_file):
        for domain in domaines:

            if elt in data[domain].values.tolist() and elt not in dict_data[domain]:
                dict_data[domain].append(elt)
    name = [domain for domain in domaines]
    data = [len(dict_data[x]) for x in domaines]
    plt.title("Compatibilité des compétences")
    plt.pie(data,  labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
    plt.axis('equal')

    io_buf = io.BytesIO()
    plt.savefig(io_buf, format='png')
    io_buf.seek(0)
    image_str = base64.b64encode(io_buf.getvalue())
    io_buf.close()
    remove_used_files(pdf_file)
    return str(image_str, 'utf-8')

def remove_used_files(pdf_file):
    for i in range(1, total_pages):
        os.remove("static/Docs/page_" + str(i) + ".jpg")

    os.remove(pdf_file)
