from fastapi import File

from app.interfaces.file_parser import Fileparser



class FileParserImpl(Fileparser):
    def parse_file(self, file: File) -> list[str]:
        """
        Parse the given file and return the extracted criteria as a list of strings.

        :param file: The file content as bytes.
        :return: A list containing the extracted criteria.
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
            case "text/plain":
                # Handle plain text file parsing
                print("Parsing plain text file")
            case "text/docx":
                # Handle DOCX file parsing
                print("Parsing DOCX file")
            case _:
                raise ValueError(f"Unsupported file type: {file.content_type}")

        print("file name:", file.filename)
        print("file content type:", file.content_type)



        return [  "file name:", file.filename,  "file content type:", file.content_type,]
