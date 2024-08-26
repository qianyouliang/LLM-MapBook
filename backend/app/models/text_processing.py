import PyPDF2
from io import BytesIO
import markdown
from docx import Document

class FileProcessor:
    def __init__(self):
        pass

    def extract_text_from_pdf(self, file):
        pdf_reader = PyPDF2.PdfReader(file)
        text_pages = []

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            text_pages.append(page_text)

        return text_pages

    def extract_text_from_txt(self, file):
        text = file.read().decode("utf-8")
        chunk_size = 5000
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    def extract_text_from_markdown(self, file):
        text = file.read().decode('utf-8')
        html = markdown.markdown(text)
        return [html]

    def extract_text_from_word(self, file):
        doc = Document(file)
        text_list = []
        for para in doc.paragraphs:
            text_list.append(para.text)
        return text_list

    def process_file(self, file, file_type):
        if file_type == 'pdf':
            return self.extract_text_from_pdf(file)
        elif file_type == 'txt':
            return self.extract_text_from_txt(file)
        elif file_type == 'md':
            return self.extract_text_from_markdown(file)
        elif file_type == 'docx':
            return self.extract_text_from_word(file)
        else:
            raise ValueError("Unsupported file type")