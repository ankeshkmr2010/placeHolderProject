from docx import Document
from fastapi import File
from pypdf import PdfReader

from app.interfaces.file_parser import Fileparser


class FileParserImpl(Fileparser):
    """
    Implementation of the Fileparser interface for handling file parsing.
    This class provides methods to parse files of different formats, including PDF, plain text, and DOCX.
    """

    async def parse_file(self, file: File) -> str:
        """
        Parse the content of the provided file based on its type.

        :param file: The file object to be parsed. Must have valid filename and content type.
        :return: The extracted content of the file as a string.
        :raises ValueError: If the file is invalid or unsupported.
        """
        if not file:
            raise ValueError("No file provided")
        if not hasattr(file, 'filename') or not hasattr(file, 'content_type') or not hasattr(file, 'file'):
            raise ValueError("Invalid file object provided")

        if not file.filename or not file.content_type:
            raise ValueError("File must have a valid filename and content type")

        match file.content_type:
            case "application/pdf":
                # Handle PDF file parsing
                print("Parsing PDF file")
                content = self._parse_pdf(file)
            case "text/plain":
                # Handle plain text file parsing
                print("Parsing plain text file")
                content = file.file.read().decode('utf-8')
            case _:
                if file.filename.endswith(".docx"):
                    print("Parsing DOCX file based on filename")
                    content = self._parse_docx(file)
                else:
                    raise ValueError(f"Unsupported file type: {file.content_type}")

        # print("file name:", file.filename)
        # print("file content type:", file.content_type)
        return content

    @staticmethod
    def _parse_pdf(file: File) -> str:
        """
        Parse the content of a PDF file.

        :param file: The PDF file object to be parsed.
        :return: The extracted text content of the PDF file as a string.
        """
        pdf_reader = PdfReader(file.file)
        text_content = []
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)
        page_content = "\n".join(text_content)
        return page_content

    @staticmethod
    def _parse_docx(file: File) -> str:
        """
        Parse the content of a DOCX file.

        :param file: The DOCX file object to be parsed.
        :return: The extracted text content of the DOCX file as a string.
        """
        doc = Document(file.file)
        text_content = []
        for para in doc.paragraphs:
            if para.text:
                text_content.append(para.text)
        doc_content = "\n".join(text_content)
        return doc_content