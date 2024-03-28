import os
from docx import Document
from ruaccent import RUAccent

def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def read_docx_file(file_path):
    doc = Document(file_path)
    return ' '.join([paragraph.text for paragraph in doc.paragraphs])

def process_text(text):
    accentizer = RUAccent()
    accentizer.load(omograph_model_size='', use_dictionary=True)
    text = accentizer.process_all(text)
    print(f"Текст с ударениями и ё: {text}")
    return text

def convert_file_to_text(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension == '.txt':
        text = read_txt_file(file_path)
    elif file_extension == '.docx':
        text = read_docx_file(file_path)
    else:
        print(f"Unsupported file format: {file_extension}")
        return
    return process_text(text)
