from fastapi import File
from pypdf import PdfReader
from docx  import Document
from app.interfaces.file_parser import Fileparser



class FileParserImpl(Fileparser):
    async def parse_file(self, file: File) -> str:
        """
        Parse the given file and return the extracted content as a string.
        This method supports PDF, plain text, and DOCX files.
        :param file: The file object containing the content to be parsed.
        :return: A string containing the extracted content.
        Raises ValueError if the file is invalid or unsupported.
        Raises ValueError if the file does not have a valid filename or content type.
        """

        if not file:
            raise ValueError("No file provided")
        if not hasattr(file, 'filename') or not hasattr(file, 'content_type') or not hasattr(file, 'file'):
            raise ValueError("Invalid file object provided")

        if not file.filename or not file.content_type:
            raise ValueError("File must have a valid filename and content type")

        content:str = ""
        match file.content_type:
            case "application/pdf":
                # Handle PDF file parsing
                print("Parsing PDF file")
                content = self._parse_pdf(file)
            case "text/plain":
                # Handle plain text file parsing
                print("Parsing plain text file")
                content = file.file.read().decode('utf-8')
            case "text/docx":
                # Handle DOCX file parsing
                print("Parsing DOCX file")
                content = self._parse_docx(file)
            case _:
                if file.filename.endswith(".docx"):
                    print("Parsing DOCX file based on filename")
                    content = self._parse_docx(file)
                else:
                    raise ValueError(f"Unsupported file type: {file.content_type}")

        print("file name:", file.filename)
        print("file content type:", file.content_type)
        return content

    @staticmethod
    def _parse_pdf(file: File) -> str:
        # Implement PDF parsing logic here
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
        # Implement DOCX parsing logic here
        doc = Document(file.file)
        text_content = []
        for para in doc.paragraphs:
            if para.text:
                text_content.append(para.text)
        doc_content = "\n".join(text_content)
        return doc_content

